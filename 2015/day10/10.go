package main

import (
	"aoc/utils"
	"fmt"
	"strings"
)

func look_and_say(s string) string {
	var sb strings.Builder
	count := 1
	for i := 1; i <= len(s); i++ {
		if i >= len(s) || s[i] != s[i-1] {
			sb.WriteString(fmt.Sprintf("%d%c", count, s[i-1]))
			count = 1
			continue
		}
		count += 1
	}
	return sb.String()
}

func part1(data string) int {
	start_string := "1321131112"
	for i := 0; i < 40; i++ {
		start_string = look_and_say(start_string)
	}
	return len(start_string)
}

func part2(data string) int {
	start_string := "1321131112"
	for i := 0; i < 50; i++ {
		start_string = look_and_say(start_string)
	}
	return len(start_string)
}

func main() {
	utils.ProblemSetUp(part1, part2)
}
