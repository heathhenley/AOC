from collections.abc import Callable

# Function either returns a value or a lambda - keep calling the lambda until
# it returns a value
def trampoline(func: Callable, *args) -> Callable:
    result = func(*args)
    while callable(result):
        result = result()
    return result


# Original recursive fibonacci (tail recursive style but no tco of course)
def fib(n: int, a: int = 0, b: int = 1) -> int:
    return a if n == 0 else fib(n - 1, b, a + b)


# Modified to return a lambda if it's not done that calls itself with the next
# values
def fib_t(n: int, a: int = 0, b: int = 1) -> int | Callable:
    return a if n == 0 else lambda: fib_t(n - 1, b, a + b)


def main():
    n = 1000

    r = trampoline(fib_t, n)
    print(f"trampoline: {str(r)[:10]}..., digits: {len(str(r))}")
    # trampoline: 4346655768..., digits: 209 ✅

    try:
        r = fib(n)
        print(f"recursive: {str(r)[:10]}..., digits: {len(str(r))}")
    except RecursionError as e:
        print(f"recursive: {e}")
    # recursive: maximum recursion depth exceeded in comparison ❌


if __name__ == "__main__":
    main()
