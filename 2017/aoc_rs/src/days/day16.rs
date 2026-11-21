use std::collections::HashMap;

fn spin(ch: &Vec<char>, s: u32) -> Vec<char> {
    let n = ch.len() as u32;
    let start = n as u32 - s;
    let mut new_char = ch.clone();
    for i in 0..n {
        let idx = (start + i) % n;
        new_char[i as usize] = ch[idx as usize];
    }
    new_char
}

fn dance(prog: String, s: &str) -> String {
    // todo - fix unwraps, just being lazy, not super interested in this problem - mostly typing
    let mut chars = prog.chars().collect::<Vec<char>>();
    s.trim().split(",").for_each(|mv| match mv.split_at(1) {
        ("s", n) => {
            let n: u32 = n.parse().expect("spin needs");
            chars = spin(&chars, n);
        }
        ("x", rest) => {
            let idx = rest.find("/").expect("expected a / in x move");
            let (a, b): (usize, usize) = (
                rest[0..idx].parse().unwrap(),
                rest[idx + 1..].parse().unwrap(),
            );
            (chars[a], chars[b]) = (chars[b], chars[a]);
        }
        ("p", rest) => {
            let idx = rest.find("/").expect("expected a / in p move");
            let (a, b) = (&rest[0..idx], &rest[idx + 1..]);
            let i = chars.iter().position(|&v| v.to_string() == a).unwrap();
            let j = chars.iter().position(|&v| v.to_string() == b).unwrap();
            chars[i] = b.parse().unwrap();
            chars[j] = a.parse().unwrap();
        }
        _ => panic!("unexpected input"),
    });
    chars.iter().collect()
}

pub fn part1(s: &str) -> String {
    let res = dance("abcdefghijklmnop".to_string(), s);
    return format!("Part 1: {}", res);
}

fn find_cycle_period(prog: String, s: &str) -> Option<u32> {
    let mut memo = HashMap::new();
    let mut prog = prog;
    for i in 0..1_000_000_000 {
        if memo.contains_key(&prog) {
            return Some(i);
        }
        memo.insert(prog.clone(), i);
        prog = dance(prog, s);
    }
    None
}

fn dance_n(prog: String, s: &str, n: u32) -> String {
    let mut prog = prog;
    for _ in 0..n {
        prog = dance(prog, s);
    }
    prog
}

pub fn part2(s: &str) -> String {
    let prog = "abcdefghijklmnop".to_string();
    let period = find_cycle_period(prog.clone(), s).unwrap();
    let idx = 1_000_000_000 % period;
    let res = dance_n(prog, s, idx);
    return format!("Part 2: {}", res);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_ex1() {
        assert_eq!(dance("abcde".to_string(), "s1,x3/4,pe/b"), "baedc");
    }
}
