use std::collections::{HashMap, HashSet, VecDeque};

fn read_into_graph(s: &str) -> HashMap<u32, Vec<u32>> {
    let mut graph: HashMap<u32, Vec<u32>> = HashMap::new();
    s.trim().lines().for_each(
        |line| match line.split(" <-> ").collect::<Vec<&str>>()[..] {
            [pipe, str_conn, ..] => {
                let pipe = pipe.trim().parse().expect("should be int");
                let conns = str_conn
                    .split(",")
                    .map(|c| c.trim().parse().expect("expected int"))
                    .collect();
                graph.insert(pipe, conns);
            }
            [s] => panic!("unexpected input {s:?}"),
            _ => panic!("unexpected input"),
        },
    );
    graph
}

fn bfs(start: u32, graph: &HashMap<u32, Vec<u32>>) -> HashSet<u32> {
    let mut seen = HashSet::new();
    let mut queue = VecDeque::from([start]);
    while let Some(visit) = queue.pop_front() {
        if seen.contains(&visit) {
            continue;
        }
        seen.insert(visit);

        // add neighbors
        for &neighbor in &graph[&visit] {
            if !seen.contains(&neighbor) {
                queue.push_back(neighbor);
            }
        }
    }
    seen
}

pub fn part1(s: &str) -> String {
    let graph = read_into_graph(s);
    let group = bfs(0, &graph);
    return format!("Part 1: {}", group.len());
}

pub fn part2(s: &str) -> String {
    let graph = read_into_graph(s);
    let mut nodes: HashSet<_> = graph.keys().copied().collect();
    let mut group_count = 0;
    while let Some(&start) = nodes.iter().next() {
        nodes.remove(&start);
        // vist it's whole group
        let group = bfs(start, &graph);
        // remove it's group from set
        nodes = &nodes - &group;
        // increment
        group_count += 1;
    }
    return format!("Part 2: {}", group_count);
}

#[cfg(test)]
mod tests {
    use super::*;

    const EX: &str = "
    0 <-> 2
    1 <-> 1
    2 <-> 0, 3, 4
    3 <-> 2, 4
    4 <-> 2, 3, 6
    5 <-> 6
    6 <-> 4, 5
    ";

    #[test]
    fn p1_ex1() {
        assert_eq!(part1(EX), "Part 1: 6");
    }

    #[test]
    fn p2_ex1() {
        assert_eq!(part2(EX), "Part 2: 2");
    }
}
