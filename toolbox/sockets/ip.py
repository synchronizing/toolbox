import socket


def is_ip(host: str) -> bool:
    """
    Checks if the host is an IP address.

    Args:
        host: The hostname to check.

    Returns:
        ``True`` if the host is an IP address, ``False`` otherwise.
    """
    try:
        socket.inet_aton(host)
        return True
    except socket.error:
        return False
