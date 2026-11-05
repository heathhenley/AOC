use std::collections::HashMap;

fn is_anagram(a: &str, b: &str) -> bool {
    let mut ht = HashMap::new();
    for c in a.chars() {
        let freq = ht.get(&c).unwrap_or(&0);
        ht.insert(c, freq + 1);
    }
    for c in b.chars() {
        if !ht.contains_key(&c) {
            return false;
        }
        let freq = ht[&c] - 1;
        if freq < 0 {
            return false;
        }
        ht.insert(c, freq);
    }
    !ht.iter().any(|(_, &freq)| freq > 0)
}

fn no_repeat_words(pass_phrase: &[&str]) -> bool {
    let mut ht = HashMap::new();
    for &word in pass_phrase.iter() {
        if ht.contains_key(word) {
            return false;
        }
        ht.insert(word, 1);
    }
    true
}

fn no_anagrams(pass_phrase: &[&str]) -> bool {
    let n = pass_phrase.len();
    for i in 0..n {
        for j in (i + 1)..n {
            if is_anagram(pass_phrase[i], pass_phrase[j]) {
                return false;
            }
        }
    }
    true
}

pub fn part1(s: &str) -> String {
    let res = s
        .lines()
        .map(|line| line.split_whitespace().collect::<Vec<&str>>())
        .filter(|p| no_repeat_words(p))
        .count();
    return format!("Part 1: {res}");
}

pub fn part2(s: &str) -> String {
    let res = s
        .lines()
        .map(|line| line.split_whitespace().collect::<Vec<&str>>())
        .filter(|p| no_repeat_words(p))
        .filter(|p| no_anagrams(p))
        .count();
    return format!("Part 2: {res}");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_ex() {
        assert_eq!(
            part1(
                "aa bb cc dd ee
                aa bb cc dd aa
                aa bb cc dd aaa"
            ),
            "Part 1: 2"
        );
    }

    #[test]
    fn p2_anagram() {
        assert_eq!(is_anagram("abc", "def"), false);
        assert_eq!(is_anagram("abc", "aaa"), false);
        assert_eq!(is_anagram("abc", "cba"), true);
    }

    #[test]
    fn p2_ex() {
        assert_eq!(
            part2(
                "abcde xyz ecdab
                iiii oiii ooii oooi oooo
                oiii ioii iioi iiio"
            ),
            "Part 2: 1"
        );
    }
}
