package main


import (
	"strings"
	"aoc/utils"
)


// map the symbols to directions
var directions = map[string][]int{
	"^": {0, 1},
	"v": {0, -1},
	">": {1, 0},
	"<": {-1, 0},
}

var MOVE_SANTA = 0



func process_moves(moves string) int {
	visited := make(map[[2]int]bool)
	current := [2]int{0, 0}
	visited[current] = true
	for _, direction := range moves {
		current[0] += directions[string(direction)][0]
		current[1] += directions[string(direction)][1]
		visited[current] = true
	}
	return len(visited)
}


func process_moves_part_2(moves string) int {
	visited := make(map[[2]int]bool)
	current_santa := [2]int{0, 0}
	current_robot := [2]int{0, 0}
	visited[current_santa] = true
	for idx, direction := range moves {
		if idx % 2 == 0 {
			current_santa[0] += directions[string(direction)][0]
			current_santa[1] += directions[string(direction)][1]
			visited[current_santa] = true
		} else {
			current_robot[0] += directions[string(direction)][0]
			current_robot[1] += directions[string(direction)][1]
			visited[current_robot] = true
		} 
	}
	return len(visited)
}


func part1(data string) int {
	return utils.Reduce(
		strings.Split(data, "\n"),
		func(accum int, cur string) int {
			return accum + process_moves(cur)
		}, 0)
}


func part2(data string) int {
	return utils.Reduce(
		strings.Split(data, "\n"),
		func(accum int, cur string) int {
			return accum + process_moves_part_2(cur)
		}, 0)
}

func main() {
	utils.ProblemSetUp(part1, part2)
}