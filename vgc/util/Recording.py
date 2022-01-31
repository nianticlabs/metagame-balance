import ast
import codecs
import os
import pickle
from typing import List, Tuple

from vgc.datatypes.Objects import Pkm

Frame = Tuple[List, List, int, int, bool]
Trajectory = List[Frame]


class GamePlayRecorder:

    def __init__(self, buffer_size: int = 2048, name: str = "", c0: str = "", c1: str = "", t0: List[Pkm] = None,
                 t1: List[Pkm] = None):
        # Data to record
        self.competitors: List[str] = [c0, c1]
        self.teams: List[List[Pkm]] = [t0, t1]
        self.buffer: Trajectory = []
        # Recorder parameters
        self.buffer_size: int = buffer_size
        self.name: str = "Data/" + name
        self.pos: int = 0
        self.f = None

    def open(self):
        """
        Open recorder for reading.
        """
        self.f = open(self.name, "r")
        self.competitors = ast.literal_eval(self.f.readline())
        self.teams = [[], []]
        idx = 0
        while idx < len(self.teams):
            raw = self.f.readline()
            while raw != '\n':
                self.teams[idx].append(pickle.loads(bytes.fromhex(raw[:-1])))
                raw = self.f.readline()
            idx += 1

    def init(self, name: str = None, append=False):
        """
        Init recorder for writing.
        """
        if name is not None:
            self.name = "Data/" + name
        if not os.path.exists("Data/"):
            os.makedirs("Data/", exist_ok=True)
        with open(self.name, "a+" if append else "w+") as f:
            f.write(str(self.competitors) + "\n")
            for team in self.teams:
                for pkm in team:
                    f.write(codecs.encode(pickle.dumps(pkm), "hex").decode() + '\n')
                f.write('\n')

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
        return row

    def load(self):
        """
        Load next chuck from file to buffer.
        """
        index = 0
        while index < self.buffer_size:
            line = self.f.readline()
            if not line:
                break
            self.buffer.append(eval(line))
            index += 1
