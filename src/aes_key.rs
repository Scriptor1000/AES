use std::fmt::{Debug, Formatter};
use std::ops::Index;

pub enum Key {
    Key128([u8; 16]),
    Key192([u8; 24]),
    Key256([u8; 32]),
}

pub enum Expanded {
    Key128([[u8; 4]; 11 * 4]),
    Key192([[u8; 4]; 13 * 4]),
    Key256([[u8; 4]; 15 * 4]),
}

pub fn key_expansion(key: Key) -> Expanded {
    let round_count: usize;
    let key_length: usize;
    let mut expanded = [[0; 4]; 15 * 4];
    match key {
        Key::Key128(key) => {
            round_count = 10;
            key_length = 4;
            for i in 0..4 {
                expanded[i] = [key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]];
            }
        }
        Key::Key192(key) => {
            round_count = 12;
            key_length = 6;
            for i in 0..6 {
                expanded[i] = [key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]];
            }
        }
        Key::Key256(key) => {
            round_count = 14;
            key_length = 8;
            for i in 0..8 {
                expanded[i] = [key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]];
            }
        }
    }
    for i in key_length..(round_count + 1) * 4 {
        let mut temp: [u8; 4] = expanded[i - 1];
        if i % key_length == 0 {
            rot_word(&mut temp);
            sub_word(&mut temp);
            xor_word(&mut temp, &crate::helpers::ROUND_CONSTANTS[i / key_length - 1])
        } else if key_length > 6 && i % key_length == 4 {
            sub_word(&mut temp);
        }
        xor_word(&mut temp, &expanded[i - key_length]);
        expanded[i] = temp
    }
    match key {
        Key::Key128(_) => {
            Expanded::Key128(expanded[0..11 * 4].try_into().unwrap())
        }
        Key::Key192(_) => {
            Expanded::Key192(expanded[0..13 * 4].try_into().unwrap())
        }
        Key::Key256(_) => {
            Expanded::Key256(expanded[0..15 * 4].try_into().unwrap())
        }
    }
}

fn sub_word(word: &mut [u8; 4]) {
    for byte in word.iter_mut() {
        *byte = crate::helpers::S_BOX[*byte as usize];
    }
}

fn rot_word(word: &mut [u8; 4]) {
    word.rotate_left(1);
}

fn xor_word(word: &mut [u8; 4], constant: &[u8; 4]) {
    for i in 0..4 {
        word[i] ^= constant[i];
    }
}

impl PartialEq for Expanded {
    fn eq(&self, other: &Self) -> bool {
        match self {
            Expanded::Key128(own_key) => {
                match other {
                    Expanded::Key128(other) => { other == own_key }
                    Expanded::Key192(_) => { false }
                    Expanded::Key256(_) => { false }
                }
            }
            Expanded::Key192(own_key) => {
                match other {
                    Expanded::Key128(_) => { false }
                    Expanded::Key192(other) => { other == own_key }
                    Expanded::Key256(_) => { false }
                }
            }
            Expanded::Key256(own_key) => {
                match other {
                    Expanded::Key128(_) => { false }
                    Expanded::Key192(_) => { false }
                    Expanded::Key256(other) => { other == own_key }
                }
            }
        }
    }

    fn ne(&self, other: &Self) -> bool {
        !(self == other)
    }
}

impl Debug for Expanded {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            Expanded::Key128(key) => {
                let mut formated = String::new();
                for i in 0..11 * 4 {
                    for j in 0..4 {
                        formated.push_str(&format!("{:02X}", key[i][j]));
                    }
                    formated.push('-');
                }
                write!(f, "{}", formated)
            }
            Expanded::Key192(key) => {
                let mut formated = String::new();
                for i in 0..13 * 4 {
                    for j in 0..4 {
                        formated.push_str(&format!("{:02X}", key[i][j]));
                    }
                    formated.push('-');
                }
                write!(f, "{}", formated)
            }
            Expanded::Key256(key) => {
                let mut formated = String::new();
                for i in 0..15 * 4 {
                    for j in 0..4 {
                        formated.push_str(&format!("{:02X}", key[i][j]));
                    }
                    formated.push('-');
                }
                write!(f, "{}", formated)
            }
        }
    }
}

impl Index<usize> for Expanded {
    type Output = [[u8; 4]; 4];

    fn index(&self, index: usize) -> &Self::Output {
        match self {
            Expanded::Key128(w) => {
                if 0 <= index && index <= 10
                { w[index * 4..(index + 1) * 4].try_into().unwrap() } else { &[[0; 4]; 4] }
            }
            Expanded::Key192(w) => {
                if 0 <= index && index <= 12
                { w[index * 4..(index + 1) * 4].try_into().unwrap() } else { &[[0; 4]; 4] }
            }
            Expanded::Key256(w) => {
                if 0 <= index && index <= 14
                { w[index * 4..(index + 1) * 4].try_into().unwrap() } else { &[[0; 4]; 4] }
            }
        }
    }
}
