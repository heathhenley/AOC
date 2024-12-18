import re
from common.utils import problem_harness, timeit, read_input


def combo_op(operand, registers):
  if operand < 4:
    return operand
  match operand:
    case 4: return registers["A"]
    case 5: return registers["B"]
    case 6: return registers["C"]
    case _: return ValueError("Invalid operand")


def run_program(registers, program):
  output = []
  ptr = 0 # program counter
  while ptr < len(program):
    match program[ptr]:
      case 0: # adv
        operand = combo_op(program[ptr+1], registers)
        registers["A"] = int(registers["A"]  / (2**operand))
        ptr +=2
      case 1: # bxl
        registers["B"] = registers["B"] ^ program[ptr+1]
        ptr +=2
      case 2: # bst
        operand = combo_op(program[ptr+1], registers)
        registers["B"] = operand % 8
        ptr +=2
      case 3: # jnz
        if registers["A"] != 0:
          ptr = program[ptr+1]
        else:
          ptr +=2
      case 4: # bxc
        registers["B"] = registers["B"] ^ registers["C"]
        ptr +=2
      case 5: # out
        operand = combo_op(program[ptr+1], registers) % 8
        output.append(operand)
        ptr +=2
      case 6: # bdv
        operand = combo_op(program[ptr+1], registers)
        registers["B"] = int(registers["A"]  / (2**operand))
        ptr +=2
      case 7: # cdv
        operand = combo_op(program[ptr+1], registers)
        registers["C"] = int(registers["A"]  / (2**operand))
        ptr +=2
      case _:
        raise ValueError("Invalid instruction")
  return output


def parse(lines):
  registers = {}
  reg_ptn = r"Register ([ABC]): (\d+)"
  for line in lines:
    if "Register" in line:
      reg, val = re.match(reg_ptn, line).groups()
      registers[reg] = int(val)
    if "Program" in line:
      program = list(map(int, line.split(':')[1].strip().split(",")))
  return registers, program

@timeit
def part1(filename: str) -> int:
  registers, program = parse(read_input(filename))
  return ",".join([str(x) for x in run_program(registers, program)])

def to_octal(num):
  return oct(num)[2:]

def from_octal(digits: list[int]):
  a = 0
  for digit in digits:
    a = a * 8 + digit
  return a


@timeit
def part2(filename: str) -> int:
  registers, program = parse(read_input(filename))
  # look for each number individually, then "shift" them
  # in to get the output we want?
  print(program)
  n_digits = len(program)
  #registers["A"] = (((((0o6 * 8) + 0o5) * 8 + 0o1) * 8 + 0o7) * 8 + 0o7) * 8 + 0o0
  # sample 
  a = 117440
  registers["A"] = a
  registers["B"] = 0
  registers["C"] = 0
  output = run_program(registers, program)
  print(a, oct(a))
  print(output)
  print(program)


  def solve(idx, registers, program, digits):
    # try all the octal digits (0, 7) for the current position
    # if we find a match, try the next one
    digits = digits.copy()
    n = len(program)
    if idx == n:
      return digits
    
    for digit in range(8):
      if idx == 0 and digit == 0:
        continue # no leading zero
      digits[idx] = digit
      a = from_octal(digits)
      registers["A"] = a
      registers["B"] = 0
      registers["C"] = 0
      output = run_program(registers, program)
      #print('output:', output)
      #print('program:', program)
      if output[n - idx - 1] == program[n - idx - 1]:
        sol = solve(idx+1, registers, program, digits.copy())
        if sol:
          return sol
    return None

  digits = [0 for _ in range(n_digits)]
  # solve for the digits
  if (digits := solve(0, registers, program, digits)):
    print(digits)
    registers["A"] = from_octal(digits)
    registers["B"] = 0
    registers["C"] = 0
    print(run_program(registers, program))
    print(f"solution: {from_octal(digits)}")
  else:
    print('no solution found...')
  return from_octal(digits) if digits else 0
  # input ---> AH! Each digit can have more than one value that satisfies the
  # that position in the output
  digits = [0 for _ in range(n_digits)]
  digits[0] = 6
  digits[1] = 1
  digits[2] = 1
  digits[3] = 1
  digits[4] = 7
  digits[5] = 1
  digits[6] = 2
  digits[7] = 7
  digits[8] = 1
  a = from_octal(digits)
  registers["A"] = a
  registers["B"] = 0
  registers["C"] = 0
  output = run_program(registers, program)
  print(a, oct(a))
  print(output[-9:])
  print(program[-9:])




  return 0


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
