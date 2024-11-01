package main

import (
	"fmt"
	"strings"
	"time"

	"aoc/utils"
)

func makeFancyString(s string) string {
	if len(s) < 3 {
		return s
	}
	var sb strings.Builder
	sb.WriteString(s[:2])
	for i := 2; i < len(s); i++ {
		if s[i] != s[i-1] || s[i] != s[i-2] {
			sb.WriteByte(s[i])
		}
	}
	return sb.String()
}


// Why is this so bad? Is it copying the string every time?
func makeFancyStringBAD(s string) string {
	if len(s) < 3 {
		return s
	}

	out := s[:2]
	for i := 2; i < len(s); i++ {
		if s[i] != s[i-1] || s[i] != s[i-2] {
			out += string(s[i])
		}
	}
	return out
}


// a couple test cases
var testCases = []struct {
	input  string
	output string
}{
	{"leeetcode", "leetcode"},
	{"aaabaaaa", "aabaa"},
	{"aab", "aab"},
	{"a", "a"},
	{"ab", "ab"},
}

func main() {
	// the super long string
	lines := strings.Split(utils.ReadFile("misc/LC/long_string.txt"), "\n")
	in := lines[0]
	out := lines[1]
	fmt.Println("Long string length:", len(in))

	// test the function with the normal test cases
	start := time.Now()
	for _, v := range testCases {
		if makeFancyString(v.input) != v.output {
			println("Test failed")
		}
	}
	elapsed := time.Since(start)
	fmt.Printf("'Good way' execution time: %0.5f\n", elapsed.Seconds())

	// the long string
	start = time.Now()
	if makeFancyString(in) != out {
		println("Test failed")
	}
	elapsed = time.Since(start)
	fmt.Printf(
		"'Good way' execution time (Long string): %0.5f\n", elapsed.Seconds())

	// test the function with the normal test cases
	start = time.Now()
	for _, v := range testCases {
		if makeFancyStringBAD(v.input) != v.output {
			println("Test failed")
		}
	}
	elapsed = time.Since(start)
	fmt.Printf("'Bad way' execution time: %0.5f\n", elapsed.Seconds())

	// the long string
	start = time.Now()
	if makeFancyStringBAD(in) != out {
		println("Test failed")
	}
	elapsed = time.Since(start)
	fmt.Printf(
		"'Bad way' execution time (Long string): %0.5f\n", elapsed.Seconds())
	

}
