from key_schedule import KeySchedule
from state import State
from helpers import _xor_bytes


def add_round_key(state: State, key_schedule: KeySchedule, round: int) -> State:
    new_columns = []
    for i, column in enumerate(state.get_columns()):
        new_columns.append(_xor_bytes(column, key_schedule[round * 4 + i]))
    state.set_columns(new_columns)
    return state
