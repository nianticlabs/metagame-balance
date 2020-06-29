from typing import List, Tuple


class Recorder:

    def __init__(self,  buffer_size: int = 4096, name: str = "Agent"):
        self.buffer_size: int = buffer_size
        self.name: str = "../Data/" + name
        self.buffer: List[Tuple[List, int, int]] = []
        self.pos: int = 0

    def clear(self):
        """
        Empty internal buffer.
        """
        self.buffer.clear()

    def full(self) -> bool:
        """
        Check if internal buffer is full.
        """
        return len(self.buffer) >= self.buffer_size

    def save(self, append=True):
        """
        Persist memory buffer on file.

        :param append: if to append data to EOF
        """

        with open(self.name, "a+" if append else "w+") as f:
            for e in self.buffer:
                f.write(str(e) + "\n")

    def record(self, record: Tuple[List, int, int]):
        """
        Store data row to buffer. If buffer is empty persist all data and empty before.

        :param record: data row (observation: List, action: int, episode: int)
        """
        if self.full():
            self.save()
            self.clear()
        self.buffer.append(record)

    def starved(self) -> bool:
        """
        Check of the buffer is starved.

        :return: if there is no more data to read
        """
        return self.pos >= len(self.buffer)

    def read(self) -> Tuple[List, int, int]:
        """
        Read next element from buffer.

        :return: next element from buffer
        """
        if self.starved():
            self.clear()
            self.load()
        row: Tuple[List, int, int] = self.buffer[self.pos]
        self.pos += 1
        return row

    def load(self):
        """
        Load next chuck from file to buffer.
        """
        self.pos = 0
        index = 0
        with open(self.name, "r") as f:
            while True and index < self.buffer_size:
                line = f.readline()
                if not line:
                    break
                self.buffer.append(eval(line))
                index += 1
