#coding=utf-8
from aprior import Apriori

DATA_PATH = 'data/trainingTitle/'
import os
import jieba
import  jieba.posseg as pseg


## 获取博客标题,并作分词, 过滤单字和无用的标点符号, 形成购物蓝
def read_data():
    total_baskets = {}
    for path, dirs, files in os.walk(DATA_PATH):
        for file in files:
            file_path = DATA_PATH + file
            f = open(file_path)
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                token = line.split('`')
                uid = token[0]
                title = token[1]
                seg = pseg.cut(title)
                basket = []
                for w in seg:
                    if w.word.__len__() <= 2 or 'x' in w.flag:
                        continue
                    basket.append(w.word.encode('utf-8'))
                if basket.__len__() < 1:
                    continue
                total_baskets[uid] = basket
    return total_baskets

total_baskets = read_data()

# ## 检查购物篮
# for uid in total_baskets:
#     basket = total_baskets[uid]
#     print uid
#     for item in basket:
#         print item,
#     print


a=Apriori(dataDic=total_baskets,min_sup=0.005)
# print a.do()
frequent_itemst =  a.do()
print frequent_itemst
