use std::collections::HashMap;

#[derive(Debug)]
enum Op {
    Inc,
    Dec,
}

#[derive(Debug)]
enum BinOp {
    Gt,
    Lt,
    Ge,
    Le,
    Eq,
    Neq,
}

#[derive(Debug)]
struct Condition {
    left: String,
    op: BinOp,
    right: i32,
}

#[derive(Debug)]
struct Instruction {
    reg: String,
    op: Op,
    val: i32,
    condition: Condition,
}

fn parse_op(s: &str) -> Op {
    match s {
        "dec" => Op::Dec,
        "inc" => Op::Inc,
        _ => panic!("unsupported op {s}"),
    }
}

fn parse_num(s: &str) -> i32 {
    s.parse().expect("failed to parse {s}")
}

fn parse_binop(s: &str) -> BinOp {
    match s {
        ">" => BinOp::Gt,
        "<" => BinOp::Lt,
        "<=" => BinOp::Le,
        ">=" => BinOp::Ge,
        "==" => BinOp::Eq,
        "!=" => BinOp::Neq,
        _ => panic!("unsupported op {s}"),
    }
}

fn parse_condition(s: Vec<&str>) -> Condition {
    Condition {
        left: s[0].to_string(),
        op: parse_binop(s[1]),
        right: parse_num(s[2]),
    }
}

fn evaluate(cond: &Condition, reg: &mut HashMap<&str, i32>) -> bool {
    let &left = reg.get(cond.left.as_str()).unwrap_or(&0);
    match cond.op {
        BinOp::Eq => left == cond.right,
        BinOp::Neq => left != cond.right,
        BinOp::Gt => left > cond.right,
        BinOp::Ge => left >= cond.right,
        BinOp::Lt => left < cond.right,
        BinOp::Le => left <= cond.right,
    }
}

pub fn part1(s: &str) -> String {
    let instructions: Vec<Instruction> = s
        .trim()
        .lines()
        .map(|l| {
            let parts: Vec<&str> = l.trim().split_whitespace().collect();
            Instruction {
                reg: parts[0].to_string(),
                op: parse_op(parts[1]),
                val: parse_num(parts[2]),
                condition: parse_condition(parts[4..].to_vec()),
            }
        })
        .collect();
    let mut registers: HashMap<&str, i32> = HashMap::new();
    for i in &instructions {
        if evaluate(&i.condition, &mut registers) {
            let &cur_value = &registers.get(i.reg.as_str()).unwrap_or(&0);
            let new_value = match i.op {
                Op::Inc => cur_value + i.val,
                Op::Dec => cur_value - i.val,
            };
            registers.insert(i.reg.as_str(), new_value);
        }
    }
    let max_val = registers
        .values()
        .max()
        .expect("no max found something broke");
    return format!("Part 1: {}", max_val);
}

pub fn part2(s: &str) -> String {
    let instructions: Vec<Instruction> = s
        .trim()
        .lines()
        .map(|l| {
            let parts: Vec<&str> = l.trim().split_whitespace().collect();
            Instruction {
                reg: parts[0].to_string(),
                op: parse_op(parts[1]),
                val: parse_num(parts[2]),
                condition: parse_condition(parts[4..].to_vec()),
            }
        })
        .collect();
    let mut registers: HashMap<&str, i32> = HashMap::new();
    let mut max_ever = i32::MIN;
    for i in &instructions {
        if evaluate(&i.condition, &mut registers) {
            let &cur_value = &registers.get(i.reg.as_str()).unwrap_or(&0);
            let new_value = match i.op {
                Op::Inc => cur_value + i.val,
                Op::Dec => cur_value - i.val,
            };
            max_ever = max_ever.max(new_value);
            registers.insert(i.reg.as_str(), new_value);
        }
    }
    return format!("Part 2: {}", max_ever);
}

#[cfg(test)]
mod tests {
    use super::*;

    const EX: &str = "
    b inc 5 if a > 1
    a inc 1 if b < 5
    c dec -10 if a >= 1
    c inc -20 if c == 10
    ";

    #[test]
    fn p1_ex1() {
        assert_eq!(part1(EX), "Part 1: 1");
    }

    #[test]
    fn p2_ex1() {
        assert_eq!(part2(EX), "Part 2: 10");
    }
}
