pub(crate) fn multiply(a: u8, b: u8) -> u8 {
    const MOD: [bool; 9] = [true, true, false, true, true, false, false, false, true];
    to_u8(modulo(multiplication(a, b), MOD))
}

fn multiplication(a: u8, b: u8) -> [bool; 16] {
    let mut m = [false; 16];
    let a = to_bits(a);
    let b = to_bits(b);
    for i in 0..8 {
        if a[i] {
            for j in 0..8 {
                if b[j] {
                    m[i + j] = !m[i + j]
                }
            }
        }
    }
    m
}

fn modulo(a: [bool; 16], div: [bool; 9]) -> [bool; 8] {
    let max_true = get_last_true(&a);
    let mut res = [false; 16];
    if let Some(max) = max_true {
        if max < 8 {
            a[0..8].try_into().unwrap()
        } else {
            for i in (0..max + 1).rev() {
                res[i] = if max - i < 9 { a[i] != div[i + 8 - max] } else { a[i] };
            }
            modulo(res, div)
        }
    } else {
      [false; 8]
    }
}

fn get_last_true(bits: &[bool; 16]) -> Option<usize> {
    let mut res = 17;
    for i in 0..16 {
        if bits[i] {
            res = i;
        }
    }
    if res < 17 {
        Some(res)
    } else {
        None
    }
}

fn to_bits(input: u8) -> [bool; 8] {
    let mut bits = [false; 8];
    for i in 0..8 {
        bits[i] = ((input >> i) & 1) != 0;
    }
    bits
}

fn to_u8(input: [bool; 8]) -> u8 {
    let mut num = 0;
    for (index, &bit) in input.iter().enumerate() {
        if bit {
            num |= 1 << index;
        }
    }
    num
}