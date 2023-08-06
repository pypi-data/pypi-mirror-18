"""
:mod:`~rcluster.pmkutils` collects the functions used to interact with remote
AWS servers using :py:class:`paramiko.client.SSHClient` and
:py:class:`paramiko.sftp_client.SFTPClient` objects.
"""

import os
import stat
import paramiko
from time import sleep
from queue import Queue
from threading import Thread
from logging import getLogger


def _unix_path(*args):
    """Most handle UNIX pathing, not vice versa, enforce standard

    :param args: Arbitrary list of directories/files to connect
    :type args: string
    :return:
    :rtype: string
    """
    return os.path.join(*args).replace('\\', '/')


def _walk_files(gen):
    """
    Take a generator yielding root, dirs, files (as from os.walk()) and return a
    list of all files.

    :param gen: Generator yielding root, dirs, files (as from os.walk())
    :type gen: generator
    :return: Fully qualified file paths
    :rtype: list of strings
    """
    all_files = []
    for root, dirs, files in gen:
        for fn in files:
            all_files.append(_unix_path(root, fn))
    return all_files


def _open_sftp(client):
    """
    Open and return. If connection denied due to too many active connections,
    try again until successful.

    :param client: Connected :py:class:`paramiko.client.SSHClient` object
    :return: A connected :py:class:`paramiko.sftp_client.SFTPClient`
    """
    try:
        return client.open_sftp()
    except paramiko.ssh_exception.ChannelException as e:
        if 'Administratively prohibited' in str(e):
            sleep(1)
            return _open_sftp(client)
        else:
            raise e


def _pmk_mover(func, client, file_tuples, threaded, thread_cap):
    """

    :param func: :py:class:`paramiko.sftp_client.SFTPClient.put`
    :param client:
    :param file_tuples:
    :param threaded:
    :return: None
    """
    file_queue = Queue()
    for tup in file_tuples:
        file_queue.put(tup)
    if threaded:
        jobs = []
        for job in range(min(len(file_tuples), thread_cap)):
            job = Thread(target=func,
                         kwargs={"client": client, "file_queue": file_queue})
            job.start()
            jobs.append(job)
        for job in jobs:
            while job.is_alive():
                sleep(1)
    else:
        func(client, file_queue)


def _pmk_put(client, file_queue):
    """

    :param client:
    :param file_queue:
    :return:
    """
    log = getLogger(__name__)
    sftp_conn = _open_sftp(client)
    while not file_queue.empty():
        source_fn, target_fn = file_queue.get()
        try:
            sftp_conn.mkdir(os.path.dirname(target_fn))
        except OSError:
            pass
        log.debug("Sending %s to %s", source_fn, target_fn)
        sftp_conn.put(source_fn, target_fn)
        file_queue.task_done()
    sftp_conn.close()


def _pmk_get(client, file_queue):
    """

    :param client:
    :param file_queue:
    :return:
    """
    log = getLogger(__name__)
    sftp_conn = _open_sftp(client)
    while not file_queue.empty():
        source_fn, target_fn = file_queue.get()
        os.makedirs(os.path.dirname(target_fn), exist_ok=True)
        log.debug("Sending %s to %s", source_fn, target_fn)
        sftp_conn.get(source_fn, target_fn)
        file_queue.task_done()
    sftp_conn.close()


def _pmk_keepalive(client, interval):
    """

    :param client:
    :param interval:
    :return:
    """
    def keepalive(client):
        while True:
            sleep(interval)
            try:
                client.exec_command("echo 'beep'")
            except paramiko.ssh_exception.SSHException as e:
                if "SSH session not active" in e.args:
                    return
                else:
                    raise e

    Thread(target=keepalive, args=(client,)).start()


def pmk_connect(host, key_path, username='ubuntu', keepalive=False,
                interval=30):
    """
    Create SSH connection to host, retrying on failure.

    :param host: The address of the remote server
    :param key_path: The location of the key pair file
    :param username: The username to access on the remote server
    :param keepalive:
    :param interval:
    :return: Connected :py:class:`paramiko.client.SSHClient` class object
    """
    log = getLogger(__name__)
    log.debug('Connecting to %s@%s using key %s', username, host, key_path)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
    try:
        log.debug('Connecting to host %s', host)
        k = paramiko.RSAKey.from_private_key_file(key_path)
        client.connect(hostname=host, username=username, pkey=k)
        if keepalive:
            _pmk_keepalive(client, interval)
        return client
    except (TimeoutError, ConnectionRefusedError,
            paramiko.ssh_exception.NoValidConnectionsError) as err:
        log.debug('OS error: %s', err)
        sleep(15)
        return pmk_connect(host, key_path, username)
    except Exception as err:
        log.error('Connection failed, unexpected error:', err)
        raise err


def pmk_cmd(client, call, **kwargs):
    """Issue command over SSH, treat execution failure as program failure.

    :param client: :py:class:`paramiko.client.SSHClient` class object
    :param call: String of shell command to be executed
    :param kwargs: Additional keyword parameters to exec_command()
    :return: Values returned to stdout
    :rtype: list of strings
    """
    log = getLogger(__name__)
    log.debug('Issuing "%s"', call)
    stdin, stdout, stderr = client.exec_command(call, **kwargs)
    lines = []
    for line in iter(lambda: stdout.readline(2048), ""):
        log.debug(line.encode('utf-8'))
        lines += line
    exit_status = stdout.channel.recv_exit_status()
    if exit_status:
        text = ''.join(stderr.readlines()).encode('utf-8')
        log.error(text)
        raise Exception(text)
    return lines


def cpu_count(client):
    """
    Given a :py:class:`paramiko.client.SSHClient` object, return the remote's
    CPU count.

    :param client: :py:class:`paramiko.client.SSHClient` class object
    :return: The number of physical CPUs on the remote instance
    :rtype: integer
    """
    cpus = pmk_cmd(client, r'cat /proc/cpuinfo | grep processor | wc -l')
    cpus = int(''.join([char for char in cpus if not char == r"\n"]))
    return cpus


def pmk_walk(sftp_conn, root):
    """paramiko os.walk() equivalent.

    :param sftp_conn: :py:class:`paramiko.sftp_client.SFTPClient` object
    :param root: Remote directory targeted
    :return: A generator of root, dirs, files
    :rtype: generator
    """
    files = []
    dirs = []
    for f in sftp_conn.listdir_attr(root):
        if stat.S_ISDIR(f.st_mode):
            dirs.append(f.filename)
        else:
            files.append(f.filename)
    yield root, dirs, files
    for folder in dirs:
        for x in pmk_walk(sftp_conn, _unix_path(root, folder)):
            yield x


def pmk_put(client, sources, target, threaded=True, thread_cap=10):
    """
    Copy local files to remote target. Directories are copied recursively when
    provided as the source. Will do nothing if source does not exist.

    :param client: :py:class:`paramiko.client.SSHClient` object
    :param sources: The local data source
    :param target: The remote data destination
    :param threaded:
    :param thread_cap: The maximum numbers of SFTP transfers to attempt; default
        is 10 (as SSH's `MaxSessions` default)
    :return: None
    """
    send_files = []
    if not type(sources) is list:
        sources = [sources]
    for source in sources:
        if os.path.isfile(source):
            target_fn = _unix_path(target, os.path.basename(source))
            send_files.append((source, target_fn))
        if os.path.isdir(source):
            for source_fn in _walk_files(os.walk(source)):
                target_fn = _unix_path(target,
                                       os.path.relpath(source_fn, source))
                send_files.append((source_fn, target_fn))
    _pmk_mover(_pmk_put, client=client, file_tuples=send_files,
               threaded=threaded, thread_cap=thread_cap)


def pmk_get(client, sources, target, threaded=True, thread_cap=10):
    """
    Copy local files to remote target. Directories are copied recursively when
    provided as the source. Will do nothing if source does not exist.

    :param client: :py:class:`paramiko.client.SSHClient` object
    :param sources: The local data source
    :param target: The remote data destination
    :param threaded:
    :param thread_cap: The maximum numbers of SFTP transfers to attempt; default
        is 10 (as SSH's `MaxSessions` default)
    :return: None
    """
    sftp_conn = client.open_sftp()
    get_files = []
    if not type(sources) is list:
        sources = [sources]
    for source in sources:
        try:
            stat_mode = sftp_conn.lstat(source).st_mode
            if stat.S_ISREG(stat_mode):
                get_files.append((source, target))
            if stat.S_ISDIR(stat_mode):
                for source_fn in _walk_files(pmk_walk(sftp_conn, source)):
                    target_fn = os.path.join(target,
                                             os.path.relpath(source_fn, source))
                    get_files.append((source_fn, target_fn))
        except IOError as e:
            if not 'No such file' in str(e):
                raise e
    _pmk_mover(_pmk_get, client=client, file_tuples=get_files,
               threaded=threaded, thread_cap=thread_cap)
