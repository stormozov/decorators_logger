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


if __name__ == '__main__':
    @logger('flat_generator.txt')
    def flat_generator(list_of_list: list) -> list:
        """Generator that handles lists with any level of nesting.

        Args:
            list_of_list (list): List with nested lists.

        Yields:
            list: A flat list.

        Example:
            >>> list_of_lists_2 = [
            ...     [['a'], ['b', 'c']],
            ...     ['d', 'e', [['f'], 'h'], False],
            ...     [1, 2, None, [[[[['!']]]]], []]
            ... ]
            >>> list(flat_generator(list_of_lists_2))
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

        Notes:
            The generator uses recursive calls to handle lists
                with any level of nesting.
        """
        for item in list_of_list:
            if isinstance(item, list):
                yield from flat_generator(item)
            else:
                yield item

    @logger('flat_iterator.txt')
    class FlatIterator:
        """An iterator that flattens a list of lists into a single list."""

        def __init__(self, list_of_list: list[list]) -> None:
            """Initialize a FlatIterator instance.

            Args:
                list_of_list (list[list]): A list of lists to be iterated over.

            Returns:
                None
            """
            self.list_of_list = list_of_list

        def __iter__(self) -> 'FlatIterator':
            """Return an iterator over the list of lists.

            Returns:
                FlatIterator: An iterator over the list of lists.
            """
            self.stack = [iter(self.list_of_list)]
            return self

        def __next__(self) -> list:
            """Return the next item in the list of lists.

            Returns:
                list: The next item in the list of lists.
            """
            while self.stack:
                try:
                    item = next(self.stack[-1])
                except StopIteration:
                    self.stack.pop()
                    continue
                if isinstance(item, list):
                    self.stack.append(iter(item))
                else:
                    return item
            raise StopIteration


    numbers_list = [1, 5, [5, 6, [7]]]

    print(
        'Run flat_generator: ',
        list(flat_generator(numbers_list))
    )
    print(
        'Run FlatIterator: ',
        list(FlatIterator(numbers_list)),
    )
