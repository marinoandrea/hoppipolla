import subprocess

from .errors import HoppipollaScionError


def ping(
    address: str,
    sequence: str,
    n_packets: int,
    sciond_address: str = "127.0.0.1:30255",
    timeout_ms: int = 5000
) -> bool:
    """
    Test connectivity to a remote SCION host using SCMP echo packets

    Wrapper for https://scion.docs.anapaya.net/en/latest/command/scion/scion_ping.html.

    Parameters
    ----------
    address: `str`
        The SCION address to ping in the form ISD-AS,IP

    sequence: `str`
        Space separated list of hop predicates in the form ISD-AS#IF,IF

    n_packets: `int`
        Number of SCMP echo packets to send (defaults to 1)

    sciond_address: `str`
        Address for the SCION daemon service (defaults to "127.0.0.1:30255")

    timeout_ms: `int`
        Timeout for the ping request expressed in milliseconds.

    Raises
    ------
    `HoppipollaScionError`
        If the invocation of `scion ping` fails for any reason

    Returns
    -------
    `bool`
        Whether the ping was successful
    """
    command = [
        "scion", "ping", address,
        "-c", str(n_packets),
        "--sequence", sequence,
        "--sciond", sciond_address,
        "--timeout", f"{timeout_ms}ms"
    ]

    process = subprocess.run(command)

    if process.returncode != 0:
        raise HoppipollaScionError(process.stderr)

    return True
