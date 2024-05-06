from add_roundkey import add_round_key
from key_schedule import KeySchedule
from mix_columns import mix_columns, inv_mix_columns
from shift_rows import shift_rows, inv_shift_rows
from state import State
from sub_bytes import sub_bytes, inv_sub_bytes


def cipher(block: bytes, round_count: int, key_schedule: KeySchedule) -> bytes:
    state = State(block)
    state = add_round_key(state, key_schedule, 0)
    for i in range(1, round_count):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, key_schedule, i)
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key_schedule, round_count)
    return state.value


def inv_cipher(block: bytes, round_count: int, key_schedule: KeySchedule) -> bytes:
    state = State(block)
    state = add_round_key(state, key_schedule, round_count)
    for i in range(round_count - 1, 0, -1):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, key_schedule, i)
        state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    state = add_round_key(state, key_schedule, 0)
    return state.value
