# coding: utf-8

# Author: Cai, Jiefei
# Date  : 2018/08/03 10:25:00


# 写正则,顺便说下代码里读取作业的时候全部改小写了.所以匹配也要小写的
searchstring = "StaticTime".lower()

# 只搜索列表内的控件，如果列表包含all，则全部搜索。代码里了会lower这些值，可改
Controls = [
    "all"
]

# 是否启用正则匹配
regexp = False

# 目前没用
path = ""

# stg
# kettle_dir = r"D:\caijiefei\bd-embdrepo-stg"

# prd
#kettle_dir = r"D:\caijiefei\bd-embdrepo_prd"

# wm
kettle_dir = r"D:\Profile\PyScript\kettle_find\data"
