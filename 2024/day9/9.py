from dataclasses import dataclass
from common.utils import problem_harness, timeit, read_input


@dataclass
class MemoryBlock:
  fileidx: int = None
  size: int = 0


def print_blocks_with_size(blocks):
  s = ''
  for block in blocks:
    c = str(block.fileidx) if block.fileidx is not None else '.'
    s += c * block.size
  print(s)

def map_to_memory(disk_map, part1=True):
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


@timeit
def part1(filename: str) -> int:
  disk_map = [int(x) for x in list(read_input(filename)[0])]
  memory = map_to_memory(disk_map, part1=True)
  print_blocks_with_size(memory)

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
  memory = map_to_memory(disk_map, part1=False)
  print_blocks_with_size(memory)


  # don't need the while actually - just trying once for each full block
  for right in range(len(memory) - 1, -1, -1):
    for left in range(right):
      ml = memory[left]
      mr = memory[right]
      if mr.fileidx is not None and ml.fileidx is None:
        # if there is space - take this one 
        if ml.size >= mr.size:
          ml.size -= mr.size
          memory.insert(left, MemoryBlock(fileidx=mr.fileidx, size=mr.size))
          #memory = (
          #  memory[:left]
          #  + [MemoryBlock(fileidx=mr.fileidx, size=mr.size)]
          #  + memory[left:]
          #)
          mr.fileidx = None
    right -= 1

  # make it like part 1 just get it over with (all size 1 blocks)
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
