package main


import (
	"crypto/md5"
	"fmt"
	"strings"
	"aoc/utils"
)


func mine(key string, difficulty int) int {
	for i := 0; ; i++ {
		hash := hash(fmt.Sprintf("%s%d", key, i))[:difficulty]
		if hash == strings.Repeat("0", difficulty) {
			return i
		}
	}
}


func hash(s string) string {
	return fmt.Sprintf("%x", md5.Sum([]byte(s)))
}


func part1(data string) int {
	key := strings.TrimRight(data, "\n") 
	return mine(key, 5)
}


func part2(data string) int {
	key := strings.TrimRight(data, "\n") 
	return mine(key, 6)
}


func main() {
	utils.ProblemSetUp(part1, part2)
}