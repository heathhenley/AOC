use std::collections::{HashSet, VecDeque, vec_deque};

use crate::days::day10::knot_hash;
use hex;

pub fn part1(s: &str) -> String {
    let res = (0..128).fold(0, |ones, i| {
        let hash = knot_hash(format!("{}-{}", s.trim(), i).as_str());
        // don't remember hamming weight and don't fell like looking it up
        // literally make the binary string and count ones
        hex::decode(hash)
            .expect("failed to decode, input probably wrong")
            .into_iter()
            .fold(String::new(), |bin_str, d| format!("{}{:08b}", bin_str, d))
            .chars()
            .fold(0, |acc, c| {
                if c == '1' {
                    return acc + 1;
                }
                acc
            })
            + ones
    });
    return format!("Part 1: {}", res);
}

fn input_to_grid(s: &str) -> (i32, Vec<Vec<bool>>) {
    // make the grid
    let mut grid: Vec<Vec<bool>> = vec![vec![false; 128]; 128];
    let mut occupied = 0;
    (0..128).for_each(|i| {
        let hash = knot_hash(format!("{}-{}", s.trim(), i).as_str());
        hex::decode(hash)
            .expect("failed to decode, input probably wrong")
            .into_iter()
            .fold(String::new(), |bin_str, d| format!("{}{:08b}", bin_str, d))
            .chars()
            .enumerate()
            .for_each(|(j, c)| {
                grid[i][j] = c == '1';
                if c == '1' {
                    occupied += 1;
                }
            })
    });
    (occupied, grid)
}

fn print_grid(grid: &Vec<Vec<bool>>) {
    grid.iter().for_each(|row| {
        row.iter().for_each(|cell| {
            if *cell {
                print!("#");
            } else {
                print!(".");
            }
        });
        println!("");
    });
}

fn find_new_grid(grid: &Vec<Vec<bool>>, seen: &HashSet<(usize, usize)>) -> Option<(usize, usize)> {
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            if grid[i][j] && !seen.contains(&(i, j)) {
                return Some((i, j));
            }
        }
    }
    None
}

fn get_neighbors((i, j): (usize, usize), n: i32, m: i32) -> Vec<(usize, usize)> {
    //no diags
    vec![(1, 0), (-1, 0), (0, 1), (0, -1)]
        .iter()
        .map(|(di, dj)| (i as i32 + di, j as i32 + dj))
        .filter(|(x, y)| (*x >= 0 && *x < n) && (*y >= 0 && *y < m))
        .map(|(x, y)| (x as usize, y as usize))
        .collect::<Vec<(usize, usize)>>()
}

pub fn part2(s: &str) -> String {
    let (total, grid) = input_to_grid(s);
    //print_grid(&grid);
    let mut seen = HashSet::new();
    let mut group_count = 0;
    let n = grid.len() as i32;
    while seen.len() < (total as usize) {
        // find a 1 we haven't seen
        let (i, j) =
            find_new_grid(&grid, &seen).expect("unexpected state, no unexplored grids left");
        let mut queue = VecDeque::new();
        queue.push_back((i, j));
        seen.insert((i, j));
        group_count += 1;
        // follow neighbors, track seen, thats a group
        while let Some((i, j)) = queue.pop_back() {
            get_neighbors((i, j), n, n).iter().for_each(|(ni, nj)| {
                if grid[*ni][*nj] && !seen.contains(&(*ni, *nj)) {
                    queue.push_back((*ni, *nj));
                    seen.insert((*ni, *nj));
                }
            });
        }
    }
    return format!("Part 2: {}", group_count);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1_ex1() {
        assert_eq!(part1("flqrgnkx"), "Part 1: 8108");
    }

    #[test]
    fn p2_ex1() {
        assert_eq!(part2("flqrgnkx"), "Part 2: 1242");
    }
}
