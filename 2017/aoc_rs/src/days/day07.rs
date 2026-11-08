use std::collections::HashMap;

#[derive(PartialEq, Eq, Hash, Debug)]
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

pub fn part1(s: &str) -> String {
    let graph = build_adjacency(s);
    // find node with no-one pointing at it?
    // look at 'holding' values and increment each of those node?
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
    return format!("Part 1: {}", root[0].name);
}

pub fn part2(_: &str) -> String {
    return "Part 2: 0".to_string();
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
}
