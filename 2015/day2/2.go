// Day 2 (2015) - 2.py - I was told there would be no math
// https://adventofcode.com/2015/day/2
package main

import (
	"strconv"
	"strings"
	"aoc/utils"
)


func one_box_area(l int, w int, h int) int {
	return 2 * (l * w + w * h + h * l) + utils.Min(l*w, utils.Min(w*h, h*l))
}


func one_ribbon(l int, w int, h int) int {
	return  2 * utils.Min((l + w), utils.Min((w + h), (h + l))) + l * w * h
}


func part1(data string) int {
	total := 0
	for _, line := range strings.Split(data, "\n") {
		dims := make([]int, 3)
		for i, dim := range strings.Split(line, "x") {
			d, err := strconv.Atoi(dim)
			if err != nil {
				panic(err)
			}
			dims[i] = d
		}
		total += one_box_area(dims[0], dims[1], dims[2])	
	}
	return total
}


func part2(data string) int {
	total := 0
	for _, line := range strings.Split(data, "\n") {
		dims := make([]int, 3)
		for i, dim := range strings.Split(line, "x") {
			d, err := strconv.Atoi(dim)
			if err != nil {
				panic(err)
			}
			dims[i] = d
		}
		total += one_ribbon(dims[0], dims[1], dims[2])	
	}
	return total
}


func main() {
	utils.ProblemSetUp(part1, part2)
}
