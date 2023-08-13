Title: TIL: Timing Function Execution
Date: 2023-08-11 15:30
Modified: 2023-08-13 20:00
Category: Python
Tags: TIL, Python, context manager
Authors: Michael Knott
Summary: Utilities to time function execution  
Status: Published

## Timing Code

Recently a colleague presented on ways to time code execution using `time.perf_counter{}` to make informed decisions on code performance in terms of speed. This led me to think about creating some utilities that simplify the process. I've included examples of a context manager, a decorator and the `timeit` function below:

### Timing Code with a Context Manager

    :::python
    import random
    import time

    class Timer:
        def __enter__(self):
            self.start = time.perf_counter()
            return self
        
        def __exit__(self, exc_type, exc_value, traceback):
            self.end = time.perf_counter()
            self.interval = self.end - self.start


    def unique_nums_using_set(nums):
        return list(set(nums))

    def unique_nums_using_fromkeys(nums):
        return list(dict.fromkeys(nums))


    def main():
        nums = [random.randint(0, 10) for _ in range(1000000)]
        with Timer() as timer_one:
            unique_nums = unique_nums_using_set(nums)
            print(f"func = {unique_nums_using_set.__name__}")
            print(f"Total = {unique_nums}")
        print(f"Elapsed time: {timer_one.interval:0.4f} seconds")

        with Timer() as timer_two:
            unique_nums = unique_nums_using_fromkeys(nums)
            print(f"func = {unique_nums_using_fromkeys.__name__}")
            print(f"Total = {unique_nums}")
        print(f"Elapsed time: {timer_two.interval:0.4f} seconds")

    if __name__ == "__main__":
        main()

    # terminal output
    func = unique_nums_using_set
    Total = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    Elapsed time: 0.0118 seconds
    func = unique_nums_using_fromkeys
    Total = [10, 3, 8, 9, 2, 6, 5, 4, 0, 1, 7]
    Elapsed time: 0.0231 seconds

One thing I learnt while implementing the context manager is that you need to return `self` from the `__enter__` method to use the `as` keyword. The below implementation shows another implementation without returning `self`. Note in the `main()` function that an instance of `Timer` is instantiated and assigned to `t` to be used with the `with` keyword.

    :::python
    import random
    import time

    class Timer:
        def __enter__(self):
            self.start = time.perf_counter()
        
        def __exit__(self, exc_type, exc_value, traceback):
            self.end = time.perf_counter()
            self.interval = self.end - self.start


    def unique_nums_using_set(nums):
        return list(set(nums))

    def unique_nums_using_fromkeys(nums):
        return list(dict.fromkeys(nums))


    def main():
        nums = [random.randint(0, 10) for _ in range(1000000)]
        timer_one = Timer()
        timer_two = Timer()

        with timer_one:
            unique_nums = unique_nums_using_set(nums)
            print(f"func = {unique_nums_using_set.__name__}")
            print(f"Total = {unique_nums}")
        print(f"Elapsed time: {timer_one.interval:0.4f} seconds")

        with timer_two:
            unique_nums = unique_nums_using_fromkeys(nums)
            print(f"func = {unique_nums_using_fromkeys.__name__}")
            print(f"Total = {unique_nums}")
        print(f"Elapsed time: {timer_two.interval:0.4f} seconds")

    if __name__ == "__main__":
        main()

    # terminal output
    func = unique_nums_using_set
    Total = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    Elapsed time: 0.0118 seconds
    func = unique_nums_using_fromkeys
    Total = [3, 4, 1, 6, 2, 10, 9, 5, 7, 8, 0]
    Elapsed time: 0.0233 seconds

### Timing Code with a Decorator

    :::python
    import random
    import time
    from functools import wraps

    def timer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            func(*args, **kwargs)
            end = time.perf_counter()
            print(f'Elapsed time: {end-start:0.4f}')
        return wrapper

    @timer
    def unique_nums_using_set(nums):
        print(f"func = {unique_nums_using_set.__name__}")
        return list(set(nums))

    @timer
    def unique_nums_using_fromkeys(nums):
        print(f"func = {unique_nums_using_fromkeys.__name__}")
        return list(dict.fromkeys(nums))

    if __name__ == "__main__":
        nums = [random.randint(0, 10) for _ in range(1000000)]
        unique_nums_using_set(nums)
        unique_nums_using_fromkeys(nums)
    
    # terminal output
    func = unique_nums_using_set
    Elapsed time: 0.0119
    func = unique_nums_using_fromkeys
    Elapsed time: 0.0254

### Using @wraps to return the original function name

The `@wraps` decorator is required to return the wrapped functions name when calling `unique_nums_using_set.__name__` or `unique_nums_using_fromkeys.__name__` instead of returning `wrapper` as the name. `@wraps` updates the the metadata of the wrapper function to return the metadata of the original function.

### Timing Code with `timeit`

As the `timeit` function is used to measure small snippets of Python code, I've passed the expressions using `set()` and `dict.fromkeys` directly to the `timeit` function. 

    :::python
    import random
    from timeit import timeit

    nums = [random.randint(0, 10) for _ in range(1000000)]

    set_time = timeit(
        stmt="list(set(nums))", setup="from __main__ import nums", number=100
    )

    fromkeys_time = timeit(
        stmt="list(dict.fromkeys(nums))", setup="from __main__ import nums", number=100
    )

    print(f"Time using set(): {set_time:.2f} seconds")
    print(f"Time using dict.fromkeys(): {fromkeys_time:.2f} seconds")

    # terminal output
    Time using set(): 1.54 seconds
    Time using dict.fromkeys(): 2.85 seconds

The statement I've passed to the `timeit` `setup` parameter seems clumsy. Another alternative is to use the `globals` parameter to allow the `timeit` function to access `nums`.

    :::python
    set_time = timeit(
        stmt="list(set(nums))", globals=globals(), number=100
    )

    fromkeys_time = timeit(
        stmt="list(dict.fromkeys(nums))", globals=globals(), number=100
    )
