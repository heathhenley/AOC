package main


import (
	"strings"
	"aoc/utils"
)


func has_double_letter(s string) bool {
	for i := 1; i < len(s); i++ {
		if s[i] == s[i-1] {
			return true
		}
	}
	return false
}


func has_vowels(s string) bool {
	vowels := "aeiou"
	count := 0
	for _, c := range s {
		if strings.Contains(vowels, string(c)) {
			count++
		}
	}
	return count >= 3
}


func no_bad_strings(s string) bool {
	bad_strings := []string{"ab", "cd", "pq", "xy"}
	for _, bs := range bad_strings {
		if strings.Contains(s, bs) {
			return false
		}
	}
	return true
}


func has_letter_sandwich(s string) bool {
	// aaa, xyx, efe,...
	if len(s) < 3 {
		return false // not enough letters for a sandwich
	}
	for i := 1; i < len(s)-1; i++ {
		if s[i-1] == s[i+1] {
			return true
		}
	}
	return false
}


func has_double_pair(s string) bool {
	// if there are two non-overlapping pairs of letters
	if len(s) < 4 {
		return false
	}
	for i := 0; i < len(s)-2; i++ {
		if strings.Contains(s[i+2:], s[i:i+2]) {
			return true
		}
	}
	return false
}


func is_nice_part1(s string) bool {
	return has_double_letter(s) && has_vowels(s) && no_bad_strings(s)
}


func is_nice_part2(s string) bool {
	return has_double_pair(s) && has_letter_sandwich(s)
}


func part1(data string) int {
	return utils.Reduce(
		strings.Split(data, "\n"),
		func(accum int, cur string) int {
			if is_nice_part1(cur) {
				return accum + 1
			}
			return accum
		}, 0)
}


func part2(data string) int {
	return utils.Reduce(
		strings.Split(data, "\n"),
		func(accum int, cur string) int {
			if is_nice_part2(cur) {
				return accum + 1
			}
			return accum
		}, 0)
}


func main() {
	utils.ProblemSetUp(part1, part2)
}