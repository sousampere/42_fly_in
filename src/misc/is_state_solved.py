
from src.MapState.State import State


def is_state_solved(state: State) -> bool:
    for zone in state.zones:
        if not zone.is_end and len(zone.drones) != 0:
            return False
    return True
