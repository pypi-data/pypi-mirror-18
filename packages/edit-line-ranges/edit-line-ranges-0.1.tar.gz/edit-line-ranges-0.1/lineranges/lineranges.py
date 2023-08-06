from collections import namedtuple


class Line(object):
    def __init__(self, value, index):
        self.value = value
        self.index = index

    def __repr__(self):
        return "value {} and index {}".format(self.value, self.index)


def change_line(lines, new_line, count_from=1):
    """Change text for a single line.

    Args:
        lines (list): this is the list that gets modified
        new_line (Line): this contains the index and new value for the line being edited
        count_from (int): lines counting starts from this value

    Examples:
        >>> values = [12.0, 1.0, 12.0]
        >>> change_line(values, Line(100.0, 2), count_from=0)
        >>> values
        [12.0, 1.0, 100.0]
        >>> other_values = ['first', 'second', 'third']
        >>> change_line(other_values, Line('hello', 2))
        >>> other_values
        ['first', 'hello', 'third']
        >>>

    """
    lines[new_line.index - count_from] = new_line.value


