from .lineranges import Line


class Parser(object):
    def __init__(self):
        self.input_lines = []
        self.out_lines = []
        self.current_line = 0

    def fromFile(self, filepath):
        with open(filepath, 'rt') as f:
            self.fromString(f.read())

    def fromString(self, string):
        self.input_lines = string.splitlines()

    def parse_line(self):
        """Parse current line and add a Line instance to self.out_lines.

        Each line can be:
            - an index
            - an index followed by one or more whitespaces and the new value
            - a range of indices N-M  (N and M are included), with optional value following

        If no value is indicated, the object Line receives None.
        Examples:
            >>> string = '2 100.0\n3\n4-6 200.0'
            >>> p = Parser()
            >>> p.fromString(string)
            >>> p.parse_line()
            >>> p.out_lines
            [Line(value='100.0', index=2),
            Line(value=None, index=3),
            Line(value='200.0', index=4),
            Line(value='200.0', index=5),
            Line(value='200.0', index=6)]
            >>>
        """
        def add_element(value, index):
            self.out_lines.append(Line(value, int(index)))
        line = self.input_lines[self.current_line]
        splitted = line.split()
        indices = splitted[0]
        if len(splitted) == 2:
            value = splitted[1]
        else:
            value = None
        indices_extremes = indices.split('-')
        if len(indices_extremes) == 2:
            lower = int(indices_extremes[0])
            upper = int(indices_extremes[1])
            for i in range(lower, upper+1):
                add_element(value, i)
        else:
            add_element(value, indices_extremes[0])

    def parse_all(self):
        """Parse all lines"""
        while self.current_line < len(self.input_lines):
            self.parse_line()
            self.current_line += 1