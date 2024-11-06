// Day 8 of Advent of Code 2015 - https://adventofcode.com/2015/day/8
package main

import (
	"aoc/utils"
	"fmt"
	"regexp"
	"strings"
)

var _ = fmt.Println

func unescape_string(s string) string {
	// Replace all escape sequences with a single character 'X' and return the
	// resulting string (don't care about the actual character, just the length).
	s = strings.Trim(s, "\"")
	s = regexp.MustCompile(`\\x[0-9a-f]{2}`).ReplaceAllString(s, "X")
	s = regexp.MustCompile(`\\.`).ReplaceAllString(s, "X")
	return s
}

func escape_string(s string) string {
	// Replace all backslashes
	s = strings.ReplaceAll(s, "\\", "\\\\")
	// Replace all double quotes
	s = strings.ReplaceAll(s, "\"", "\\\"")
	// Replace all hex escape sequences
	s = regexp.MustCompile(`\\x[0-9a-f]{2}`).ReplaceAllString(s, "\\xAA")
	return "\"" + s +  "\""
}

func part1(data string) int {
	count := 0
	for _, line := range strings.Split(data, "\n") {
		count += len(line) - len(unescape_string(line))
	}
	return count
}

func part2(data string) int {
	count := 0
	for _, line := range strings.Split(data, "\n") {
		fmt.Println(line, escape_string(line))
		count += len(escape_string(line)) - len(line)
	}
	return count
}

func main() {
	utils.ProblemSetUp(part1, part2)
}
