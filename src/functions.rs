use crate::helpers::{INV_S_BOX, S_BOX};

pub fn sub_bytes(state: &mut [u8; 16]) {
    for byte in state.iter_mut() {
        *byte = S_BOX[*byte as usize];
    }
}

pub fn inv_sub_bytes(state: &mut [u8; 16]) {
    for byte in state.iter_mut() {
        *byte = INV_S_BOX[*byte as usize];
    }
}

pub fn shift_rows(state: &mut [u8; 16]) {
    for i in 1..4 {
        let row = [state[i], state[i + 4], state[i + 8], state[i + 12]];
        state[i] = row[i];
        state[i + 4] = row[(i + 1) % 4];
        state[i + 8] = row[(i + 2) % 4];
        state[i + 12] = row[(i + 3) % 4];
    }
}

pub fn inv_shift_rows(state: &mut [u8; 16]) {
    for i in 1..4 {
        let row = [state[i], state[i + 4], state[i + 8], state[i + 12]];
        state[i] = row[4 - i];
        state[i + 4] = row[(5 - i) % 4];
        state[i + 8] = row[(6 - i) % 4];
        state[i + 12] = row[(7 - i) % 4];
    }
}

pub fn add_round_key(state: &mut [u8; 16], key: &[[u8; 4]; 4]) {
    for i in 0..16 {
        state[i] ^= key[i / 4][i % 4];
    }
}


pub fn mix_columns(state: &mut [u8; 16]) {
    let mut matrix = [2u8, 3, 1, 1];
    matrix_multiplication(state, &mut matrix);
}

pub fn inv_mix_columns(state: &mut [u8; 16]) {
    let mut matrix = [0x0eu8, 0x0b, 0x0d, 0x09];
    matrix_multiplication(state, &mut matrix);
}

fn matrix_multiplication(state: &mut [u8; 16], matrix: &mut [u8; 4]) {
    for c in 0..4 {
        let column: [u8; 4] = state[c * 4..(c + 1) * 4].try_into().unwrap();
        let mut result = [0u8; 4];
        for r in 0..4 {
            for i in 0..4 {
                result[r] ^= crate::galois_field::multiply(column[i], matrix[i]);
            }
            update_matrix(matrix);
        }
        state[c * 4..(c + 1) * 4].copy_from_slice(&result);
    }
}


fn update_matrix(matrix: &mut [u8; 4]) {
    *matrix = [matrix[3], matrix[0], matrix[1], matrix[2]];
}