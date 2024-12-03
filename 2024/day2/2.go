package main

import (
	"aoc/utils"
	"math"
	"strconv"
	"strings"
)

func isGoodLevel(level []int) bool {
	for i := range level {
		if i == 0 {
			continue
		}
		d := level[i] - level[i-1]
		if math.Abs(float64(d)) > 3 || math.Abs(float64(d)) == 0 {
			return false
		}
	}
	return isIncreasing(level) || isDecreasing(level)
}

func isIncreasing(level []int) bool {
	for i := range level {
		if i == 0 {
			continue
		}
		if level[i] < level[i-1] {
			return false
		}
	}
	return true
}

func isDecreasing(level []int) bool {
	for i := range level {
		if i == 0 {
			continue
		}
		if level[i] > level[i-1] {
			return false
		}
	}
	return true
}

func isGoodLevelWithRemoval(level []int) bool {
	// this is on^2 but it's small enough to not matter
	if isGoodLevel(level) {
		return true
	}
	for i := range level {
		// remove element and check if it is good without it
		levelCopy := make([]int, len(level))
		copy(levelCopy, level)
		levelCopy = append(levelCopy[:i], levelCopy[i+1:]...)
		if isGoodLevel(levelCopy) {
			return true
		}
	}
	return false
}

func toInt(s string) int { 
	i, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return i
}

func part1(data string) int {
	// I know this isn't very go'idomatic but I like it so idc
	return utils.Reduce(
		strings.Split(data, "\n"), func(acc int, line string) int {
			level := utils.Map(strings.Split(line, " "), toInt)
			if isGoodLevel(level) {
				return acc + 1;
			}
			return acc
		}, 0)
}

func part2(data string) int {
	return utils.Reduce(
		strings.Split(data, "\n"), func(acc int, line string) int {
			level := utils.Map(strings.Split(line, " "), toInt)
			if isGoodLevelWithRemoval(level) {
				return acc + 1;
			}
			return acc
		}, 0)
}

func main() {
	utils.ProblemSetUp(part1, part2)
}
