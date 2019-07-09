import os
import sys
import hashlib
import functools

import json

class DirMap():

    def __init__(self, cwd):
        self.rootdir = cwd
        self.scheme = {}
        self.hashed = False

        self.define_structure()
        self.scheme = self.gotree(self.scheme, os.path.dirname(self.rootdir))

        #self.dump_tree('MD5scheme.json')

        return self.scheme

    def define_structure(self):
        rootdir = self.rootdir.rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1
        for path, dirs, files in os.walk(rootdir):
            folders = path[start:].split(os.sep)
            subdir = dict.fromkeys(files)
            parent = functools.reduce(dict.get, folders[:-1], self.scheme)
            parent[folders[-1]] = subdir

    def MD5(self, target):
        with open(target, 'rb') as tg:
            data = tg.read()
            return hashlib.md5(data).digest()

    def gotree(self, root, stack):
        for node in root:
            if root[node] is None:
                root[node] = self.MD5(stack+os.sep+node)
            elif isinstance(root[node],dict):
                root[node] = self.gotree(root[node], stack+os.sep+node)
        
        return root

    def dump_tree(self, output):
        with open(output, 'w') as tree:
            json.dump(self.scheme, tree)



class DoubleFinder(DirMap):
    def __init__(self, cwd):
        super().__init__(cwd)
        self.print_douples(self.find_douples())

    def define_structure(self):
        rootdir = self.rootdir.rstrip(os.sep)
        start = rootdir.rfind(os.sep) + 1
        for path, dirs, files in os.walk(rootdir):
            for _file in files:
                filepath = path+os.sep+_file
                digest = self.MD5(filepath)
                try:
                    self.scheme[digest].append(filepath)
                except KeyError:
                    self.scheme[digest] = [filepath,]
                    
    def gotree(self, dumbass,bombass): #stub
        return self.scheme

    def find_douples(self):
        doubled = list(filter(lambda files: len(files)>1, self.scheme.values()))
        return doubled

    def print_douples(self,douples):
        for douple in douples:
            print('[!] Identical files:')
            for _file in douple:
                print('    '+_file)


if __name__ == '__main__':

    tmap = DoubleFinder(os.getcwd())
