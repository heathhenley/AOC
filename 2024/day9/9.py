from common.utils import problem_harness, timeit, read_input


@timeit
def part1(filename: str) -> int:
  disk_map = [int(x) for x in list(read_input(filename)[0])]
  print(disk_map)
  # even indices are the files - their file id is their pos in the list
  files = {i // 2: disk_map[i] for i in range(0, len(disk_map), 2)}
  print(files)
  # odd indices are blocks of free space
  free = {i // 2 + 1: disk_map[i] for i in range(1, len(disk_map), 2)}
  print(free)
  print(sum(free.values()))
  # start with the left most free block
  # start with the right most file
  # take a block from the right most file idx, put it in the current free idx
  # move to the next free idx were' at 0 fro this block
  new_files = {}
  curr_free_idx = 1
  stack = [(idx, files[idx]) for idx in files]
  while stack:
    # fill the current free idx with the right most fild idx
    file_idx, blocks = stack.pop()
    
    # find next free idx
    while free[curr_free_idx] == 0:
      curr_free_idx += 2
      if curr_free_idx >= len(free):
        break

    # fill the free idx with the file idx
    free[curr_free_idx] -= 1
    new_files[curr_free_idx] = new_files.get(curr_free_idx, []) + [file_idx]

    # if the file idx has more blocks, put it back in the stack 
    if blocks > 1:
      stack.append((file_idx, blocks - 1))

    # how do we know when we're done?
  
  # merge the original files with the new files
  print(new_files)
  print(files)

  n = max(max(files.keys()), max(new_files.keys()))
  s = ""
  for i in range(0, n):
    print(s)
    if i % 2 == 0:
      s += str(files[i // 2])
    else:
      print(new_files[i])
      s += "".join([str(x) for x in new_files[i]])
  print(s)




  return 0


@timeit
def part2(filename: str) -> int:
  return 0


def main():
  problem_harness(part1, part2)

if __name__ == '__main__':
  main()
