package main

import (
	"fmt"
	"math"
	"math/rand"
	"time"
	"sync"
)

func closestEdge(x, y float64) string {
	distances := map[string]float64{
		"bottom": y,
		"top":    1 - y,
		"left":   x,
		"right":  1 - x,
	}
	closest := "bottom"
	minDistance := distances[closest]
	for edge, distance := range distances {
		if distance < minDistance {
			closest = edge
			minDistance = distance
		}
	}
	return closest
}

func simulate(n int) float64 {
	counter := 0
	for i := 0; i < n; i++ {
		// random numbers for x1, y1, x2, y2
		x1 := rand.Float64()
		y1 := rand.Float64()
		x2 := rand.Float64()
		y2 := rand.Float64()

		numer_term := math.Pow(x1, 2) + math.Pow(y1, 2) - math.Pow(x2, 2) - math.Pow(y2, 2)
		denom_term_x := 2 * (x1 - x2)
		denom_term_y := 2 * (y1 - y2)

		// find the closest edge of the square to point 1
		switch closestEdge(x1, y1) {
		case "bottom":
			check := numer_term / denom_term_x
			if check < 0 || check > 1 {
				continue
			}
			counter += 1
		case "top":
			check := (numer_term - 2*(y1-y2)) / denom_term_x
			if check < 0 || check > 1 {
				continue
			}
			counter += 1
		case "left":
			check := numer_term / denom_term_y
			if check < 0 || check > 1 {
				continue
			}
			counter += 1
		case "right":
			check := (numer_term - 2*(x1-x2)) / denom_term_y
			if check < 0 || check > 1 {
				continue
			}
			counter += 1
		}
	}
	return float64(counter) / float64(n)
}

func main() {
	n := 100_000_000
	repeats := 10
	numWorkers := 10

	results := make(chan float64, numWorkers)
	var wg sync.WaitGroup

	start := time.Now()

	for w := 0; w < numWorkers; w++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			fmt.Printf("Worker %d started\n", workerID)
			for j := 0; j < repeats/numWorkers; j++ {
				results <- simulate(n)
			}
		  fmt.Printf("Worker %d finished\n", workerID)
		}(w)
	}

	go func() {
		wg.Wait()
		close(results)
	}()

	sum := 0.0
	sum2 := 0.0
	count := 0
	for result := range results {
		sum += result
		sum2 += math.Pow(result, 2)
		count++
		fmt.Printf("%d: %.10f\n", count, result)
	}

	elapsed := time.Since(start)
	fmt.Printf("Total execution time: %0.5f\n", elapsed.Seconds())

	// stats calculation
	mean := sum / float64(repeats)
	variance := sum2/float64(repeats) - math.Pow(mean, 2)
	fmt.Printf("Mean: %0.10f\n", mean)
	fmt.Printf("Variance: %0.10f\n", variance)
	fmt.Printf("Standard deviation: %0.10f\n", math.Sqrt(variance))
	fmt.Printf("Confidence interval: [%0.10f, %0.10f]\n",
		mean-1.96*math.Sqrt(variance/float64(repeats)),
		mean+1.96*math.Sqrt(variance/float64(repeats)))
}
