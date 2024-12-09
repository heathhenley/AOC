from dataclasses import dataclass
from common.utils import problem_harness, timeit, read_input


@dataclass
class MemoryBlock:
  fileidx: int = None
  size: int = 0


def print_blocks_with_size(blocks: list[MemoryBlock]):
  s = ''
  for block in blocks:
    c = str(block.fileidx) if block.fileidx is not None else '.'
    s += c * block.size
  print(s)


def map_to_memory(disk_map= list[int], part1=True) -> list[MemoryBlock]:
  memory = []
  for idx, d in enumerate(disk_map):
    if part1:
      memory.extend([
        MemoryBlock(fileidx=idx // 2 if idx % 2 == 0 else None, size=1)
        for _ in range(d)]
      )
    else:
      memory.append(MemoryBlock(
        fileidx=idx // 2 if idx % 2 == 0 else None, size=d
      ))
  return memory


def expand(m: list[MemoryBlock]) -> list[MemoryBlock]:
  # expand the memory blocks to be size 1
  expanded = []
  for block in m:
    for _ in range(block.size):
      expanded.append(MemoryBlock(fileidx=block.fileidx))
  return expanded


def checksum(m: list[MemoryBlock]) -> int:
  return sum(idx * block.fileidx for idx, block in enumerate(m)
             if block.fileidx is not None)


@timeit
def part1(filename: str) -> int:
  disk_map = [int(x) for x in list(read_input(filename)[0])]
  memory = map_to_memory(disk_map, part1=True)

  # just one loop this time, tracks the next free block (they are all size 1 so 
  # it doesn't matter for this part)
  left, right = 0, len(memory) - 1
  while left < right:
    # need to find free block on left and taken block on right
    if memory[left].fileidx is not None:
      left += 1
      continue
    if memory[right].fileidx is None:
      right -= 1
      continue
    # swap them
    memory[left], memory[right] = memory[right], memory[left]
    left += 1
    right -= 1

  return checksum(memory)


@timeit
def part2(filename: str) -> int:
  disk_map = [int(x) for x in list(read_input(filename)[0])]
  memory = map_to_memory(disk_map, part1=False)

  # take each block starting from the right - if it's a file, find the first
  # empty block from the left that it can fit in and put it there - don't need
  # the while because we only have to try once for each file block
  # this approach technically works for part 1 style input as well, but it's
  # slower to do that way (moving one by one and looping all the back up to next
  # empty block - instead of keeping the left pointer updated like part 1 does)
  for right in range(len(memory) - 1, -1, -1):
    for left in range(right):
      ml = memory[left]
      mr = memory[right]
      if mr.fileidx is not None and ml.fileidx is None:
        if ml.size >= mr.size:
          ml.size -= mr.size
          memory.insert(left, MemoryBlock(fileidx=mr.fileidx, size=mr.size))
          mr.fileidx = None
  return checksum(expand(memory))


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
