# coding=utf-8

from igraph import *

from pypinyin import lazy_pinyin

import aprior


def load_data(filename):
    basket_data = {}
    f = open(filename)
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        tokens = line.split(',')
        basket_data[tokens[0]] = tokens[1:]
    return basket_data

## 获取一元频繁项集
def get_frequent_item(basket_data):
    frequent_item = {}
    for basket in basket_data:
        for item in basket_data[basket]:
            if item not in frequent_item:
                frequent_item[item] = 1
            else:
                frequent_item[item] += 1
    sorted_frequent_item = sorted(frequent_item.items(), key=lambda item:-item[1])
    str_item = ''
    str_item_data = ''
    for item in sorted_frequent_item:
        str_item += "'" + item[0] + "'" + ','
    str_item = str_item.strip(",")
    for item in sorted_frequent_item:
        str_item_data += str(item[1])+ ','
    str_item_data = str_item_data.strip(",")
    print str_item
    print str_item_data


## 可视化
def visualize(frequent_itemset):


    k = 3

    new_itemset = []
    labels = []

    ## 取特定的频繁项集
    for itemset in frequent_itemset:
        if itemset.__len__() != k:
            continue
        new_itemset.append(itemset)
        for item in itemset:
            newitem =  "".join(lazy_pinyin(unicode(item,"utf-8")))
            labels.append(newitem)

    print new_itemset.__len__()
    ## 构图
    vetex_num = new_itemset.__len__() * k
    print vetex_num
    g = Graph(vetex_num)
    i = 0
    for itemset in new_itemset:
        g.add_edge(i,i+1)
        g.add_edge(i+1,i+2)
        i += k
    g.vs["label"] = labels

    # 绘图
    print 'ok'
    p = Plot()
    p.background = "#ffffff"
    p.add(g,
          bbox=(50,50,550,550),
          layout = "fr",
          vertex_size = 10,
          edge_width = 0.5,
          edge_color = "grey",
          )
    p.show()
    p.save("./graph_3_0.02.png")


def main():
    filename = 'data/training.txt'
    basket_data = load_data(filename)
    get_frequent_item(basket_data)  ##获取一元频繁项集

    ## 执行aprior算法,获得frequent_itemset
    apr = aprior.Apriori(min_sup=0.02, dataDic=basket_data)
    frequent_itemset = apr.do()

    ## 可视化
    visualize(frequent_itemset)

main()