from libraries import *


# запускать с n = 700003
def fibonacci(n: int) -> int:  # содержимое функции не менять
    """Возвращает последнюю цифру n-е числа Фибоначчи."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b % 10


# запускать с f, a, b, n равными соответственно math.sin, 0, math.pi, 20000000
def trapezoidal_rule(f: math.sin, a: int, b: float, n: int) -> int:  # содержимое функции не менять
    """Вычисляет определенный интеграл функции f от a до b методом трапеций с n шагами."""
    h = (b - a) / n
    integral = (f(a) + f(b)) / 2.0
    for i in range(1, n):
        integral += f(a + i * h)
    return integral * h


def sequence() -> None:
    start_time = perf_counter()

    # Вычисление fibonacci
    fib_result = fibonacci(700003)
    print(f'fibonacci = {fib_result}')

    # Вычисление интеграла
    trap_result = trapezoidal_rule(math.sin, 0, math.pi, 20000000)
    print(f'trapezoidal_rule = {trap_result}')

    end_time = perf_counter()
    print(f'sequence time: {end_time - start_time: 0.2f} seconds\n')


def threaded_fibonacci(result: list, n: int) -> None:
    result.append(fibonacci(n))


def threaded_trapezoidal_rule(result: list, f: int, a: int, b: float, n: int) -> None:
    result.append(trapezoidal_rule(f, a, b, n))


def threads() -> None:
    start_time = perf_counter()

    fib_result = []
    trap_result = []

    fib_thread = threading.Thread(target=threaded_fibonacci, args=(fib_result, 700003))
    trap_thread = threading.Thread(target=threaded_trapezoidal_rule, args=(trap_result, math.sin, 0, math.pi, 20000000))

    fib_thread.start()
    trap_thread.start()

    fib_thread.join()
    trap_thread.join()

    print(f'fibonacci = {fib_result[0]}')
    print(f'trapezoidal_rule = {trap_result[0]}')

    end_time = perf_counter()
    print(f'threads time: {end_time - start_time: 0.2f} seconds\n')


def process_fibonacci(result: list, n: int) -> None:
    result.append(fibonacci(n))


def process_trapezoidal_rule(result: list, f: int, a: int, b: float, n: int) -> None:
    result.append(trapezoidal_rule(f, a, b, n))


def processes() -> None:
    start_time = perf_counter()

    fib_result = multiprocessing.Manager().list()
    trap_result = multiprocessing.Manager().list()

    fib_process = multiprocessing.Process(target=process_fibonacci, args=(fib_result, 700003))
    trap_process = multiprocessing.Process(target=process_trapezoidal_rule,
                                           args=(trap_result, math.sin, 0, math.pi, 20000000))

    fib_process.start()
    trap_process.start()

    fib_process.join()
    trap_process.join()

    print(f'fibonacci = {fib_result[0]}')
    print(f'trapezoidal_rule = {trap_result[0]}')

    end_time = perf_counter()
    print(f'processes time: {end_time - start_time: 0.2f} seconds\n')


async def async_fibonacci(n: int) -> int:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, fibonacci, n)


async def async_trapezoidal_rule(f: math.sin, a: int, b: float, n: int) -> int:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, trapezoidal_rule, f, a, b, n)


async def main() -> None:
    start_time = perf_counter()

    # Создание задач
    fib_task = asyncio.create_task(async_fibonacci(700003))
    trap_task = asyncio.create_task(async_trapezoidal_rule(math.sin, 0, math.pi, 20000000))

    # Ожидание выполнения задач
    fib_result = await fib_task
    trap_result = await trap_task

    # Вывод результатов
    print(f'fibonacci = {fib_result}')
    print(f'trapezoidal_rule = {trap_result}')

    end_time = perf_counter()
    print(f'asyncio time: {end_time - start_time: 0.2f} seconds\n')


# Запуск основного события
if __name__ == '__main__':
    print("--------sequence---------")
    sequence()
    print("---------threads--------")
    threads()
    print("---------processes--------")
    processes()
    print("--------asyncio---------")
    asyncio.run(main())
"""
    Результатом должно стать (знаки вопроса заменятся на ваше время выполнения):

--------sequence---------
fibonacci = 7
trapezoidal_rule = 2.000000000000087
sequence time:  5.23 seconds

---------threads--------
fibonacci = 7
trapezoidal_rule = 2.000000000000087
threads time:  5.16 seconds

---------processes--------
fibonacci = 7
trapezoidal_rule = 2.000000000000087
processes time:  5.25 seconds

--------asyncio---------
fibonacci = 7
trapezoidal_rule = 2.000000000000087
asyncio time:  5.31 seconds

"""