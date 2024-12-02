package main

import (
	"aoc/utils"
	"math"
	"sort"
	"strconv"
	"strings"
)

func parseLine(line string) (int, int) {
	s := strings.Split(line, "   ")
	l, err := strconv.Atoi(s[0])
	if err != nil {
		panic(err)
	}
	r, err := strconv.Atoi(s[1])
	if err != nil {
		panic(err)
	}
	return l, r
}

func getFreqMap(intArr []int) map[int]int {
	freqMap := make(map[int]int)
	for _, val := range intArr {
		freqMap[val]++
	}
	return freqMap
}

func part1(data string) int {
	lines := strings.Split(data, "\n")
	leftArr := make([]int, len(lines))
	rightArr := make([]int, len(lines))
	for idx, line := range lines {
		l, r := parseLine(line)
		leftArr[idx] = l
		rightArr[idx] = r
	}
	sort.Ints(leftArr)
	sort.Ints(rightArr)
	diff_sum := 0
	for idx, l := range leftArr {
		diff_sum += int(math.Abs(float64(rightArr[idx] - l)))
	}
	return diff_sum
}

func part2(data string) int {
	lines := strings.Split(data, "\n")
	leftArr := make([]int, len(lines))
	rightArr := make([]int, len(lines))
	for idx, line := range lines {
		l, r := parseLine(line)
		leftArr[idx] = l
		rightArr[idx] = r
	}
	freqMap := getFreqMap(rightArr)
	score := 0
	for _, l := range leftArr {
		score += l * freqMap[l]
	}
	return score
}

func main() {
	utils.ProblemSetUp(part1, part2)
}
