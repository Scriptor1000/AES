from key_schedule import KeySchedule
from state import State
from helpers import xor_bytes


def add_round_key(state: State, key_schedule: KeySchedule, round_count: int) -> State:
    new_columns = []
    for i, column in enumerate(state.get_columns()):
        new_columns.append(xor_bytes(column, key_schedule[round_count * 4 + i].value))
    state.set_columns(new_columns)
    return state
