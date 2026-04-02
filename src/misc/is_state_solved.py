
from src.MapState.State import State


def is_state_solved(state: State) -> bool:
    """ Checks if a state is solved """
    for zone in state.zones:
        if not zone.is_end and len(zone.drones) != 0:
            return False
    return True
