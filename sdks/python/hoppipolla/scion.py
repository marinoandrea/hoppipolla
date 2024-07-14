import subprocess

from .errors import HoppipollaScionError


def ping(address: str, sequence: str, n_packets: int) -> bool:
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

    Raises
    ------
    `HoppipollaScionError`
        If the invocation of `scion ping` fails for any reason

    Returns
    -------
    `bool`
        Whether the ping was successful
    """
    executable = "scion ping"
    options = f"-C {n_packets} --sequence {sequence}"
    command = f"{executable} {address} {options}"

    process = subprocess.run(command)

    if process.returncode != 0:
        raise HoppipollaScionError(process.stderr.decode())

    return True
