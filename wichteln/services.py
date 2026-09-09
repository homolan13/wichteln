import random
from pathlib import Path

import yaml

from wichteln.models import Config


def load_yaml(fpath: str):
    with open(Path(fpath), 'r') as f:
        config = Config.model_validate(yaml.safe_load(f))
    return config


def save_yaml(fpath: str, assignments: dict[str, str]):
    with open(Path(fpath), 'w') as f:
        yaml.safe_dump(assignments, f, sort_keys=False)


def send_email(giver: str, receiver: str, email_config: dict):
    """
    Send an email to the giver with the receiver's name.

    Args:
        giver (str): The name of the participant who is giving the gift.
        receiver (str): The name of the participant who is receiving the gift.
        email_config (dict): Configuration for sending emails.

    Returns:
        None
    """
    pass


def draw(participants: list[str], constraints: dict[str, list[str]], seed: int | None = None) -> dict[str, str]:
    """
    Generate a constraint satisfaction problem (CSP) for the Secret Santa problem.

    Args:
        participants (list[str]): List of participant names.
        constraints (dict[str, list[str]]): Dictionary mapping participant names to lists of participants they cannot 
        draw.

    Returns:
        dict: A dictionary containing the draw results.
    """
    rng = random.Random(seed)

    domains = {
        giver: [
            receiver 
            for receiver in participants 
            if receiver != giver and receiver not in constraints.get(giver, [])
        ] for giver in participants
    }

    assignment = {}

    def solve() -> bool:
        if len(assignment) == len(participants):
            return True

        # Heuristic: Choose the giver with the fewest available receivers first, reduces unnecessary search
        giver = min(
            (g for g in participants if g not in assignment),
            key=lambda g: len(domains[g])
        )

        rng.shuffle(domains[giver])

        for receiver in domains[giver]:
            if receiver not in assignment.values():
                assignment[giver] = receiver
                if solve():
                    return True
                del assignment[giver]

        return False

    if not solve():
        raise ValueError('No valid assignment found.')

    return assignment


