# coding: utf8

import chardet

gbk_dir = r"D:\git\mongo-python-driver\ez_setup.py"

gbk_s = open(gbk_dir,'r')

gbk = gbk_s.read()

gbk_s.close()


# Easy
print chardet.detect(gbk)

# Advance
from chardet.universaldetector import UniversalDetector

gbk_s = open(gbk_dir,'r')


detector = UniversalDetector()
for l in gbk_s:
    detector.feed(l)
    if detector.done:
        break

detector.close()
print detector.result

gbk_s.close()
