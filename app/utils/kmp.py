"""Courtesy of https://gist.github.com/m00nlight/daa6786cc503fde12a77"""


from typing import Iterator


class KMP:
    def partial(self, pattern):
        """Calculate partial match table: String -> [Int]"""
        ret = [0]

        for i in range(1, len(pattern)):
            j = ret[i - 1]
            while j > 0 and pattern[j] != pattern[i]:
                j = ret[j - 1]
            ret.append(j + 1 if pattern[j] == pattern[i] else j)
        return ret

    def search(self, dataset, pattern):
        """
        KMP search main algorithm: String -> String -> [Int]
        Return all the matching position of pattern string P in T
        """
        partial, ret, j = self.partial(pattern), [], 0

        for i in range(len(dataset)):
            while j > 0 and dataset[i] != pattern[j]:
                j = partial[j - 1]
            if dataset[i] == pattern[j]:
                j += 1
            if j == len(pattern):
                ret.append(i - (j - 1))
                j = partial[j - 1]

        return ret
