import functools
import os
from datetime import datetime


def logger(old_function: callable) -> callable:
    """Decorator for logging functions.

    Args:
        old_function (function): The function to be decorated.

    Returns:
        function: The decorated function.

    Description:
        The logger decorator logs information about the function call to a file
            named main.log.
        The information includes the function name, call time, arguments,
            keyword arguments, and result.
    """
    @functools.wraps(old_function)
    def new_function(*args, **kwargs):
        current_datatime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_string = (
            f'Функция "{old_function.__name__}" '
            f'вызвана {current_datatime} '
            f'с аргументами {args}, {kwargs}'
        )
        result = old_function(*args, **kwargs)
        log_string += f' - result: {result}'

        with open('main.log', 'a', encoding='utf-8') as file:
            file.write(log_string + '\n')

        return result
    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert (
            str(item) in log_file_content
        ), f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
