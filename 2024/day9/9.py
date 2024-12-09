from dataclasses import dataclass
from common.utils import problem_harness, timeit, read_input


@dataclass
class MemoryBlock:
  fileidx: int = None

@dataclass
class MemoryBlockWithSize:
  fileidx: int = None
  size: int = 0


def print_blocks(blocks):
  s = ''
  for block in blocks:
    s += str(block.fileidx) if block.fileidx is not None else '.'
  print(s)

def print_blocks_with_size(blocks):
  s = ''
  for block in blocks:
    c = str(block.fileidx) if block.fileidx is not None else '.'
    s += c * block.size
  print(s)

@timeit
def part1(filename: str) -> int:
  disk_map = [int(x) for x in list(read_input(filename)[0])]
  memory = []
  for idx, d in enumerate(disk_map):
    if idx % 2 == 0:
      for _ in range(d):
        memory.append(MemoryBlock(
          fileidx=idx // 2
        ))
    else:
      for _ in range(d):
        memory.append(MemoryBlock(fileidx=None))
  left, right = 0, len(memory) - 1
  while left < right:
    if memory[left].fileidx is not None:
      left += 1
    elif memory[right].fileidx is None:
      right -= 1
    else:
      memory[left] = memory[right]
      memory[right] = MemoryBlock(fileidx=None)
      left += 1
      right -= 1

  checksum = 0
  for idx, block in enumerate(memory):
    if block.fileidx is not None:
      checksum += idx * block.fileidx
  return checksum


@timeit
def part2(filename: str) -> int:
  disk_map = [int(x) for x in list(read_input(filename)[0])]
  memory = []
  for idx, d in enumerate(disk_map):
    if idx % 2 == 0:
      memory.append(MemoryBlockWithSize(
        fileidx=idx // 2,
        size=int(d)
      ))
    else:
      memory.append(MemoryBlockWithSize(fileidx=None, size=int(d)))
  # go backwards to try to move each one once?
  left, right = 0, len(memory) - 1
  while right > 0:
    for left in range(right):
      ml = memory[left]
      mr = memory[right]
      if mr.fileidx is not None and ml.fileidx is None:
        # if there is space - take this one 
        if ml.size >= mr.size:
          ml.size -= mr.size
          memory = (
            memory[:left]
            + [MemoryBlockWithSize(fileidx=mr.fileidx, size=mr.size)]
            + memory[left:]
          )
          mr.fileidx = None
    right -= 1

  #print_blocks_with_size(memory)


  # make it like part 1 just get it over with
  m = []
  for idx, block in enumerate(memory):
    for _ in range(block.size):
      m.append(MemoryBlock(fileidx=block.fileidx))

  checksum = 0
  for idx, block in enumerate(m):
    if block.fileidx is not None:
      checksum += idx * block.fileidx
  return checksum




def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
