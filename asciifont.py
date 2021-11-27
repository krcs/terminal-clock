import re
import collections.abc

class AsciiFont:
    def __init__(self, filename):
        f = open(filename, "r");
        raw_lines = f.read();

        if len(raw_lines) == 0:
            return

        self._lines = re.split("\n", raw_lines)
        self.size = self._get_size()
        self._chars = self._get_chars()
        f.close()

    def __getitem__(self, index):
        if type(index) == int:
            if index >= 0 and index <= 9:
                return self._chars[index]
            return

        if len(index) != 1:
            return

        if index == ":":
            return self._chars[10]

        if index >= '0' and index <= '9':
            return self._chars[int(index)]
        
        return

    def _get_size(self):
        font_width = 0
        font_height = 0

        height = 0
        margin = 0

        margin_rx = re.compile("^\s*")

        for line in self._lines:

            if len(line) == 0:
                if height > 0:
                    font_height = height
                height = 0
                continue

            if len(line) > font_width:
                font_width = len(line)

            height += 1

            m = margin_rx.search(line)
            if m:
                if margin == 0:
                    margin = m.end()
                elif m.end() < margin:
                    margin = m.end()

        font_width = font_width - margin
        return [font_width, font_height]

    def _get_chars(self):
        result = []
        char = []
        for line in self._lines:
            if len(line) == 0:
                if len(char) > 0:
                    result.append(char)
                char = []
                continue

            char.append(line[-self.size[0]:])
        return result
