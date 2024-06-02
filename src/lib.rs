mod helpers;
mod functions;
mod galois_field;
mod aes_key;
mod tests;

fn cipher(state: &mut [u8; 16], key: aes_key::Key) {
    let expanded = aes_key::key_expansion(key);
    let rounds;
    match expanded {
        aes_key::Expanded::Key128(_) => {
            rounds = 10;
        }
        aes_key::Expanded::Key192(_) => {
            rounds = 12;
        }
        aes_key::Expanded::Key256(_) => {
            rounds = 14;
        }
    }
    functions::add_round_key(state, &expanded[0]);
    for i in 1..rounds {
        functions::sub_bytes(state);
        functions::shift_rows(state);
        functions::mix_columns(state);
        functions::add_round_key(state, &expanded[i]);
    }
    functions::sub_bytes(state);
    functions::shift_rows(state);
    functions::add_round_key(state, &expanded[rounds]);
}

fn inv_cipher(state: &mut [u8; 16], key: aes_key::Key) {
    let expanded = aes_key::key_expansion(key);
    let rounds;
    match expanded {
        aes_key::Expanded::Key128(_) => {
            rounds = 10;
        }
        aes_key::Expanded::Key192(_) => {
            rounds = 12;
        }
        aes_key::Expanded::Key256(_) => {
            rounds = 14;
        }
    }
    functions::add_round_key(state, &expanded[rounds]);
    for i in (1..rounds).rev() {
        functions::inv_shift_rows(state);
        functions::inv_sub_bytes(state);
        functions::add_round_key(state, &expanded[i]);
        functions::inv_mix_columns(state);
    }
    functions::inv_shift_rows(state);
    functions::inv_sub_bytes(state);
    functions::add_round_key(state, &expanded[0]);
}
