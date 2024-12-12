from libraries import *


# список url
urls = ['https://www.example.com'] * 10


def fetch_url(url: str) -> str:
    response = requests.get(url)
    return response.text


def sequence() -> None:
    start_time = perf_counter()
    for url in urls:
        fetch_url(url)
    end_time = perf_counter()
    print(f'sequence time: {end_time - start_time: 0.2f} seconds')


def threads() -> None:
    start_time = perf_counter()
    threads_list = []

    for url in urls:
        thread = threading.Thread(target=fetch_url, args=(url,))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    end_time = perf_counter()
    print(f'threads time: {end_time - start_time: 0.2f} seconds')


def processes() -> None:
    start_time = perf_counter()
    with multiprocessing.Pool(processes=len(urls)) as pool:
        pool.map(fetch_url, urls)
    end_time = perf_counter()
    print(f'processes time: {end_time - start_time: 0.2f} seconds')


async def fetch_url_async(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as response:
        return await response.text()


async def async_sequence() -> None:
    async with aiohttp.ClientSession() as session:
        start_time = perf_counter()
        for url in urls:
            await fetch_url_async(session, url)
        end_time = perf_counter()
        print(f'async sequence time: {end_time - start_time:0.2f} seconds')


async def async_gather() -> None:
    async with aiohttp.ClientSession() as session:
        start_time = perf_counter()
        tasks = [fetch_url_async(session, url) for url in urls]
        await asyncio.gather(*tasks)
        end_time = perf_counter()
        print(f'async gather time: {end_time - start_time:0.2f} seconds')


def run_async_tests() -> None:
    asyncio.run(async_sequence())
    asyncio.run(async_gather())


if __name__ == "__main__":
    print("--------sequence---------")
    sequence()
    print("---------threads--------")
    threads()
    print("---------processes--------")
    processes()
    print("--------asyncio---------")
    run_async_tests()
"""

    Результатом должно стать (знаки вопроса заменятся на ваше время выполнения):

--------sequence---------
sequence time:  6.08 seconds

---------threads--------
threads time:  0.62 seconds

---------processes--------
processes time:  1.95 seconds

--------asyncio---------
async sequence time: 2.03 seconds
async gather time: 0.61 seconds

"""