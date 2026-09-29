"""Faults injected on purpose, each with the undo that removes it.

fill_network_pool reproduces B2: Docker networks named like leaked AlpaSim
runs until `docker network create` fails. environment.py counts them as
AlpaSim networks, so CLEANUP_ENV removes them.
"""

import subprocess

from environment import NETWORK_SUFFIX

MAX_FAKE_NETWORKS = 256


def fill_network_pool() -> list[str]:
    created = []
    for index in range(MAX_FAKE_NETWORKS):
        name = f"fault_{index}{NETWORK_SUFFIX}"
        proc = subprocess.run(
            ["docker", "network", "create", name], capture_output=True, check=False
        )
        if proc.returncode != 0:
            return created
        created.append(name)
    raise RuntimeError(f"pool still not full after {MAX_FAKE_NETWORKS} networks")


def remove_networks(names: list[str]) -> None:
    for name in names:
        subprocess.run(
            ["docker", "network", "rm", name], capture_output=True, check=False
        )
