import os
import subprocess


def get_sciond_base_url(target: str) -> str:
    scion_home = os.getenv("HOPPIPOLLA_SCION_HOME", None)
    if scion_home is None:
        raise RuntimeError("'HOPPIPOLLA_SCION_HOME' not specified")
    process = subprocess.run([f"{scion_home}/scion.sh", "sciond-addr", target])
    return str(process.stdout).strip()
