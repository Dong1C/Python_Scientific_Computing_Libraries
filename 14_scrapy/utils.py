import time
import asyncio
from functools import wraps


def async_timer(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        start_time = loop.time()
        result = await func(*args, **kwargs)
        end_time = loop.time()
        elapsed_time = end_time - start_time
        print(f"Function {func.__name__} took {elapsed_time:.2f} seconds to execute")
        return result

    return wrapper


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} took {end-start:.2f} seconds to execute")
        return result

    return wrapper


@async_timer
async def example_coroutine():
    await asyncio.sleep(1)


async def main():
    await example_coroutine()


if __name__ == "__main__":
    asyncio.run(main())
