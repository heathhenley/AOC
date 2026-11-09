use std::collections::HashMap;

#[derive(PartialEq, Eq, Hash, Debug, Clone)]
struct Node {
    name: String,
    weight: i32,
    //holding: Option<Vec<Box<Node>>>,
}

fn parse_weight(w: &str) -> i32 {
    w.strip_prefix("(")
        .expect("parse error expected '('")
        .strip_suffix(")")
        .expect("parse error, expected ')'")
        .parse()
        .expect("expected int")
}

fn parse_node(s: &str) -> Node {
    let s: Vec<&str> = s.split_whitespace().collect();
    let (name, weight_st) = (s[0], s[1]);
    Node {
        name: name.to_string(),
        weight: parse_weight(weight_st),
    }
}

fn parse_holding(h: &str) -> Vec<&str> {
    h.split(", ").collect()
}

fn build_adjacency(s: &str) -> HashMap<Node, Vec<&str>> {
    let mut graph: HashMap<Node, Vec<&str>> = HashMap::new();
    s.trim().lines().for_each(|line| {
        let res: Vec<&str> = line.split("->").collect();
        match res.len() {
            1 => {
                let node = parse_node(res[0]);
                if !graph.contains_key(&node) {
                    graph.insert(node, Vec::new());
                }
            }
            2 => {
                let node = parse_node(res[0]);
                let holding = parse_holding(res[1].trim());
                graph.insert(node, holding);
            }
            _ => panic!("unexpected size after parsing line"),
        }
    });
    graph
}

fn total_weight(node: &Node, graph: &HashMap<Node, Vec<&str>>) -> i32 {
    node.weight
        + graph
            .get(&node)
            .expect("node should be in graph...")
            .iter()
            .fold(0, |acc, &n| {
                let node = graph
                    .keys()
                    .find(|k| k.name == n)
                    .expect("node missing from graph");
                total_weight(&node, graph) + acc
            })
}

fn find_root(graph: &HashMap<Node, Vec<&str>>) -> Node {
    let mut incident = HashMap::new();
    graph.iter().for_each(|(_, holding)| {
        for &v in holding {
            if let Some(v) = incident.get_mut(v) {
                *v += 1;
                continue;
            }
            incident.insert(v, 1);
        }
    });
    let root: Vec<_> = graph
        .keys()
        .filter(|&k| !incident.contains_key(&k.name.as_str()))
        .collect();
    if root.len() == 0 {
        panic!("no roots...")
    }
    if root.len() > 1 {
        panic!("too many roots, something is wonky")
    }
    root[0].clone()
}

fn check(node: &Node, graph: &HashMap<Node, Vec<&str>>) -> Option<i32> {
    let children: Vec<&Node> = graph[node]
        .iter()
        .map(|&n| {
            graph
                .keys()
                .find(|k| k.name == n)
                .expect("node missing from graph")
        })
        .collect();
    let ws: Vec<i32> = children.iter().map(|c| total_weight(c, graph)).collect();
    // try each index, find the one which only matches itself
    let odd = (0..ws.len()).find(|&i| ws.iter().filter(|&&w| w == ws[i]).count() == 1)?;
    let target = ws[(odd + 1) % ws.len()];
    if let Some(fix) = check(children[odd], graph) {
        return Some(fix);
    }
    Some(children[odd].weight + target - ws[odd])
}

pub fn part1(s: &str) -> String {
    let graph = build_adjacency(s);
    return format!("Part 1: {}", find_root(&graph).name);
}

pub fn part2(s: &str) -> String {
    let graph = build_adjacency(s);
    let root = find_root(&graph);
    let diff = check(&root, &graph).unwrap();
    return format!("Part 2: {}", diff);
}

#[cfg(test)]
mod tests {
    use super::*;

    const EX1: &str = "
    pbga (66)
    xhth (57)
    ebii (61)
    havc (66)
    ktlj (57)
    fwft (72) -> ktlj, cntj, xhth
    qoyq (66)
    padx (45) -> pbga, havc, qoyq
    tknk (41) -> ugml, padx, fwft
    jptl (61)
    ugml (68) -> gyxo, ebii, jptl
    gyxo (61)
    cntj (57)
    ";

    #[test]
    fn p1_ex1() {
        assert_eq!(part1(EX1), "Part 1: tknk");
    }

    #[test]
    fn p2_ex1() {
        assert_eq!(part2(EX1), "Part 2: 60");
    }
}
