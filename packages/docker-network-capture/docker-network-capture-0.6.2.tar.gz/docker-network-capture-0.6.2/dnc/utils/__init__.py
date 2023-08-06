from ctypes import CDLL
from os import O_RDONLY, open as os_open, dup as os_dup, close
from string import printable
from contextlib import contextmanager


def drop_privileges(uid_name='nobody', gid_name='nobody'):
    import os, pwd, grp

    if os.getuid() != 0:
        # We're not root so, like, whatever dude
        return

    # Get the uid/gid from the name
    running_uid = pwd.getpwnam(uid_name).pw_uid
    running_gid = grp.getgrnam(gid_name).gr_gid

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setgid(running_gid)
    os.setuid(running_uid)

    # Ensure a very conservative umask
    old_umask = os.umask(0o77)


@contextmanager
def dup_close(*args):
    """ Duplicate a bunch of FDs and close them afterwards """
    def _dup_close(fd):
        d = os_dup(fd)
        close(fd)
        return d

    duped = [_dup_close(f) for f in args]
    try:
        yield duped
    finally:
        for d in duped:
            close(d)


def net_ns(pid):
    """ Set the network namespace of current process to the net namespace of the given `pid` """
    libc = CDLL('libc.so.6')
    fd = os_open('/proc/{}/ns/net'.format(pid), O_RDONLY)
    libc.setns(fd, 0)
    del libc


def filtered(seq):
    """ Filter the input sequence """
    return list(filter(None, seq))


def is_tcpdump_header(contents):
    """ Determine whether `contents` contains a tcpdump/pcap header"""
    if len(contents) < 4:
        return False
    return contents[:4] == b'\xd4\xc3\xb2\xa1'


def has_flag(val, flag):
    """ Check for presence of binary `flag` in `val` """
    return val & flag == flag


def extend_buf(buf, size=16):
    """ Make sure the buffer is at least `size` long """
    num = size - len(buf)
    return buf + [" "] * num


def format_buffer(buf):
    """ Format the buffer in a similar way as `hexdump -C` does """
    output = "  00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15"
    output += "\n+-------------------------------------------------+----------------+\n| "
    cnt = 0
    line_buffer = []
    break_it = False
    for c in buf:
        if chr(c) in printable and c >= 32:
            line_buffer.append(chr(c))
        else:
            line_buffer.append('.')
        output += hex(c)[2:].zfill(2).upper() + ' '
        cnt += 1
        if cnt == 16:
            cnt = 0
            output += "|{}|".format("".join(line_buffer))
            output += '\n| '
            line_buffer = []
            break_it = True
    if line_buffer:
        last = output.rfind('\n')
        pad = 51 - (len(output) - last)
        output += (" " * pad) + "|{}|".format("".join(extend_buf(line_buffer)))
        output += '\n'
    if output[-2:] == '| ' and break_it:
        output = output[:-2]
    output += "+-------------------------------------------------+----------------+"
    return output
