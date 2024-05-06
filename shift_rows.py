from state import State


def shift_rows(state: State):
    new_rows = []
    for i, row in enumerate(state.get_rows()):
        new_rows.append(row[i:] + row[:i])
    state.set_rows(new_rows)
    return state


def inv_shift_rows(state: State):
    new_rows = []
    for i, row in enumerate(state.get_rows()):
        new_rows.append(row[-i:] + row[:-i])
    state.set_rows(new_rows)
    return state
