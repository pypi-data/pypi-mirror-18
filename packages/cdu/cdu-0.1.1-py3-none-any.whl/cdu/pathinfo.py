from collections import defaultdict
import math


class PathInfo:
    def __init__(self, key):
        self.key = key
        self.storage_classes = defaultdict(StorageClassInfo)

    def __repr__(self):
        return '<PathInfo: %s, %d bytes, %d files>' % (
            self.key,
            self.size,
            self.file_count,
        )

    @property
    def file_count(self):
        return sum([x.file_count for x in self.storage_classes.values()])

    @property
    def size(self):
        return sum([x.size for x in self.storage_classes.values()])

    @property
    def ts_min(self):
        return min([x.ts_min for x in self.storage_classes.values()])

    @property
    def ts_max(self):
        return max([x.ts_max for x in self.storage_classes.values()])

    def add_file(self, file):
        self.storage_classes[file['StorageClass']].add_file(file)

    def add_directory(self, directory):
        for storage_class, info in directory.storage_classes.items():
            self.storage_classes[storage_class].add(info)

    def to_json(self):
        return {
            'key': self.key,
            'data': dict((x[0], x[1].to_json()) for x in self.storage_classes.items())
        }


class StorageClassInfo:
    def __init__(self):
        self.file_count = 0
        self.size = 0
        self.ts_min = math.inf
        self.ts_max = 0

    def add(self, new):
        self.file_count += new.file_count
        self.size += new.size
        self.ts_min = min(self.ts_min, new.ts_min)
        self.ts_max = max(self.ts_max, new.ts_max)

    def add_file(self, new_file):
        self.file_count += 1
        self.size += new_file['Size']
        self.ts_min = min(self.ts_min, new_file['LastModified'].timestamp())
        self.ts_max = max(self.ts_max, new_file['LastModified'].timestamp())

    def __repr__(self):
        return '<StorageClassInfo: %d, %d>' % (
            self.file_count,
            self.size,
        )

    def to_json(self):
        return {
            'file_count': self.file_count,
            'size': self.size,
            'ts_min': int(self.ts_min),
            'ts_max': int(self.ts_max),
        }