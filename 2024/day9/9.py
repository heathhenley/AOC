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
    #print(idx, d)
    if idx % 2 == 0:
      memory.append(MemoryBlockWithSize(
        fileidx=idx // 2,
        size=int(d)
      ))
    else:
      memory.append(MemoryBlockWithSize(fileidx=None, size=int(d)))

  #print_blocks_with_size(memory)

#  right = len(memory) - 1
#  while right > 0:
#    if memory[right].fileidx is None:
#      right -= 1
#      continue
#    block_size = 0
#    k = right
#    fid = memory[right].fileidx
#    while memory[k].fileidx == fid:
#      block_size += 1
#      k -= 1
#    # find the first free block big enough to fit the current block
#    for start, length in map.items():
#      if block_size <= length:
#        break
#    else:
#      # need to move along to the nex file - we can't fit the current one
#      right -= block_size
#      continue
#
#    
#    # find the left most block that can fit the current file
#    for idx, block in enumerate(memory):
#      if block.fileidx is None:
#        start = idx
#        while memory[idx].fileidx is None:
#          idx += 1
#        if idx - start >= block_size:
#          break
#    else:
#      # we can't fit the file anywhere, need to skip to the next file
#      while fid == memory[right].fileidx:
#        right -= 1
#        continue
#    # we can fit the file blocks, so move them
#    for _ in range(block_size):
#      print(start, right)
#      memory[start] = memory[right]
#      memory[right] = MemoryBlock(fileidx=None)
#      start += 1
#      right -= 1
#
#    if fid == 0:
#      break
#
#  checksum = 0
#  for idx, block in enumerate(memory):
#    if block.fileidx is not None:
#      checksum += idx * block.fileidx
#  return checksum

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
