import pickle
from typing import List, Tuple
from framework.DataObjects import Pkm

Frame = Tuple[List, List, int, int, bool]
Trajectory = List[Frame]


class GamePlayRecorder:  # TODO

    def __init__(self, buffer_size: int = 2048, name: str = "", c0: str = "", c1: str = "", t0: List[Pkm] = None,
                 t1: List[Pkm] = None):
        # Data to record
        self.competitors: List[str] = [c0, c1]
        self.teams: List[List[Pkm]] = [t0, t1]
        self.buffer: Trajectory = []
        # Recorder parameters
        self.buffer_size: int = buffer_size
        self.name: str = "../Data/" + name
        self.pos: int = 0
        self.f = None

    def open(self):
        """
        Open recorder for reading.
        """
        self.f = open(self.name, "r")

    def init(self, append=True):
        with open(self.name, "a+" if append else "w+") as f:
            f.write(str(self.competitors) + "\n")
            for team in self.teams:
                f.write(str([pickle.dumps(pkm) for pkm in team]) + "\n")

    def close(self):
        """
        Close recorder in reader mode.
        """
        self.f.close()

    def empty(self) -> bool:
        """
        Check if internal buffer is empty.
        """
        return len(self.buffer) == 0

    def clear(self):
        """
        Empty internal buffer.
        """
        self.buffer.clear()
        self.pos = 0

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

    def record(self, frame: Frame):
        """
        Store data row to buffer. If buffer is empty persist all data and empty before.

        :param frame: data row (observation: List, action: int, episode: int)
        """
        if self.full():
            self.save()
            self.clear()
        self.buffer.append(frame)

    def starved(self) -> bool:
        """
        Check of the buffer is starved.

        :return: if there is no more data to read
        """
        return self.pos >= len(self.buffer)

    def read(self) -> Frame:
        """
        Read next element from buffer.

        :return: next element from buffer
        """
        if self.starved():
            self.clear()
            self.load()
            if self.empty():
                return [], [], -1, -1, False
        row: Frame = self.buffer[self.pos]
        self.pos += 1
        print(self.pos)
        return row

    def load(self):
        """
        Load next chuck from file to buffer.
        """
        index = 0
        while True and index < self.buffer_size:
            line = self.f.readline()
            if not line:
                break
            self.buffer.append(eval(line))
            index += 1
