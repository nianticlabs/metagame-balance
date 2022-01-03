import unittest

from framework.DataObjects import StandardMetaData, Archtype


class TestStandardMetaData(unittest.TestCase):

    def test_set_archtype(self):
        for x in range(100):
            meta = StandardMetaData()
            archtypes = []
            for _ in range(x):
                archtypes.append(Archtype())
            for archtype in archtypes:
                meta.set_archtype(archtype)
            # repeat should not affect
            for archtype in archtypes:
                meta.set_archtype(archtype)
            self.assertEqual(len(meta._teams), x)
            self.assertEqual(len(meta._usage), x)
            self.assertEqual(len(meta._victories), x * x - x)

    def test_update(self):
        meta = StandardMetaData()
        archtypes = []
        for _ in range(100):
            archtypes.append(Archtype())
        for archtype in archtypes:
            meta.set_archtype(archtype)
        count = [0] * 100
        for x in range(1, 100):
            for i in range(0, x):
                count[i] += 1
                count[i + 1] += 1
                meta.update(archtypes[i], archtypes[i + 1])
        for i in range(98):
            self.assertEqual(meta.get_usagerate(archtypes[i]), count[i] / meta._total_usage)
            self.assertEqual(meta.get_winrate(archtypes[i], archtypes[i + 1]), 1.0)
        for x in range(1, 100):
            for i in range(0, x):
                count[i] += 1
                count[i + 1] += 1
                meta.update(archtypes[i + 1], archtypes[i])
        for i in range(98):
            self.assertEqual(meta.get_usagerate(archtypes[i]), count[i] / meta._total_usage)
            self.assertEqual(meta.get_winrate(archtypes[i], archtypes[i + 1]), 0.5)

    def test_remove(self):
        meta = StandardMetaData()
        archtypes = []
        for _ in range(10):
            archtypes.append(Archtype())
        for archtype in archtypes:
            meta.set_archtype(archtype)
        count = [0] * 10
        for x in range(1, 10):
            for i in range(0, x):
                count[i] += 1
                count[i + 1] += 1
                meta.update(archtypes[i], archtypes[i + 1])
        meta._total_usage -= meta._usage[archtypes[0]]
        count = count[1:]
        meta.remove_archtype(archtypes[0])
        archtypes.pop(0)
        self.assertEqual(len(meta._teams), 9)
        for i in range(7):
            self.assertEqual(meta.get_usagerate(archtypes[i]), count[i] / meta._total_usage)
            self.assertEqual(meta.get_winrate(archtypes[i], archtypes[i + 1]), 1.0)

    def test_limited_history(self):
        meta = StandardMetaData(5)
        archtypes = []
        for _ in range(3):
            archtypes.append(Archtype())
        for archtype in archtypes:
            meta.set_archtype(archtype)
        for x in range(4):
            meta.update(archtypes[0], archtypes[1])
        self.assertEqual(meta._usage[archtypes[0]], 4)
        self.assertEqual(meta._usage[archtypes[1]], 4)
        self.assertEqual(meta._total_usage, 8)
        for x in range(6):
            meta.update(archtypes[0], archtypes[1])
        self.assertEqual(meta._total_usage, 10)
        self.assertEqual(meta._usage[archtypes[0]], 5)
        self.assertEqual(meta._usage[archtypes[1]], 5)
        self.assertEqual(meta.get_usagerate(archtypes[0]), 0.5)
        self.assertEqual(meta.get_usagerate(archtypes[1]), 0.5)
        self.assertEqual(meta.get_usagerate(archtypes[2]), 0.0)
