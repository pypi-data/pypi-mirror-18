#! /usr/bin/env python
from collections import defaultdict

import sys


class Args:
    obj = None

    d = defaultdict(list)
    synonyms = defaultdict(list)
    callbacks = defaultdict(list)

    def __init__(self, obj):
        self.obj = obj

    def register(self, word, callback, n_args=0, synonyms=[]):
        if not self.d[word]:
            self.d[word] = [callback, n_args]
            self.synonyms[word] = synonyms

    def act(self, args):
        l = len(args)
        i = 0
        while i < l:
            a = self.resolve_word(args[i])
            if a in self.d:
                callback = self.d[a][0]
                n = self.d[a][1]
                callargs = []
                for j in range(n):
                    callargs.append(args[i + j + 1])
                i += n + 1
                self.callbacks[callback] = callargs
                callback(*callargs)
            else:
                print 'Unknown argument', a
                i += 1

    def resolve_word(self, word):
        if word in self.d:
            return word
        else:
            for key in self.synonyms:
                if word in self.synonyms[key]:
                    return key
        return None


if __name__ == "__main__":
    class testclass:
        def playfrom(self, n):
            print 'playing from', n

        def shuffle(self):
            print 'shuffling'


    tc = testclass()

    args = Args(tc)
    args.register('from', tc.playfrom, 1, ['playfrom', 'fr'])
    args.register('shuf', tc.shuffle, 0, ['shuff', 'shuffle'])

    print args.synonyms
    args.act(sys.argv[1:])
