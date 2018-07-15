import sys
import os

filepath=sys.argv[0]
filepath='../test_picture'
pathDir = os.listdir(filepath)
for i in pathDir:
    print(i)