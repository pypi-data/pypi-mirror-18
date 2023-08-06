import sys


class Progress:
    def __init__(self, stream):
        self.count = 0
        self.text = ""
        self.last_lengths = [0, 0]
        self.stream = stream

    def update(self, new_text):
        self.count += 1
        self.text = new_text
        self.refresh()

    def refresh(self):
        for length in self.last_lengths:
            self.stream.write(" " * length)
            self.stream.write("\n")
        self.stream.write("\033[F\033[F")
        messages = [
            '%d done' % self.count,
            self.text
        ]
        for m in messages:
            self.stream.write("%s\n" % m)
        self.last_lengths = [len(x) for x in messages]
        self.stream.write("\033[F\033[F")