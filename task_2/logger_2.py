import os
from datetime import datetime
from functools import wraps


def logger(path: str) -> callable:
    """Decorator which logs the function calls.

    The decorator takes the path to the log file as an argument.
    It saves the date and time of the function call, the function name,
    the arguments and the result of the function call.
    """
    def __logger(old_function: callable) -> callable:
        @wraps(old_function)
        def new_function(*args, **kwargs) -> str:
            """The function which is used to replace the old one.
            It makes all the necessary work and then calls the old function.
            """
            current_datatime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_string = (
                # The string which is saved to the log file
                f'Функция "{old_function.__name__}" '
                f'вызвана {current_datatime} '
                f'с аргументами {args}, {kwargs}'
            )
            result = old_function(*args, **kwargs)
            log_string += f' - result: {result}'

            with open(path, 'a', encoding='utf-8') as file:
                # Save the string to the log file
                file.write(log_string + '\n')

            return result
        return new_function
    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), \
            "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, \
                f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
