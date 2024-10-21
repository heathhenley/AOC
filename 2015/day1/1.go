// Description: Day 1: Not Quite Lisp
// https://adventofcode.com/2015/day/1
package main

import (
	"aoc/utils"
)


func part1(data string) int {
	floorMap := map[rune]int{'(': 1, ')': -1}
	return utils.Reduce([]rune(data), func(accum int, cur rune) int {
		return accum + floorMap[cur]
	}, 0)
}


func part2(data string) int {
	floorMap := map[rune]int{'(': 1, ')': -1}
	floor := 0
	for i, c := range data {
		floor += floorMap[c]
		if floor == -1 {
			return i + 1
		}
	}
	panic("Basement not found in input")
}


func main() {
	utils.ProblemSetUp(part1, part2)
}