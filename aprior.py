#! -*- coding:utf-8 -*-
import itertools

class Apriori:
    def __init__(self,min_sup=0.4,dataDic={}):
        self.data = dataDic  ##构建数据记录词典，形如{'T800': ['I1', 'I2', 'I3', 'I5'],...}
        self.size = len(dataDic) #统计数据记录的个数
        self.min_sup = min_sup  ##最小支持度的阈值
        self.min_sup_val = min_sup * self.size ##最小支持度计数

    def find_frequent_1_itemsets(self):
        FreqDic = {} #{itemset1:freq1,itemsets2:freq2},用于统计物品的支持度计数
        for event in self.data:  ##event为每一条记录，如T800
            for item in self.data[event]: ##item就是I1，I2，I3，I4，I5
                if item in FreqDic:
                    FreqDic[item] += 1
                else:
                    FreqDic[item] = 1
        L1 = []
        for itemset in FreqDic:
            if FreqDic[itemset] >= self.min_sup_val: ##过滤掉小于最小支持度阈值的物品
                L1.append([itemset])
        return L1

    def has_infrequent_subset(self,c,L_last,k):
        ## c为当前集合，L_last为上一个频繁项集的集合，k为当前频繁项集内的元素个数,
        ## 该函数用于检查当前集合的子集是否 都为频繁项集
        subsets = list(itertools.combinations(c,k-1)) #itertools是排列组合模块，目的就c分解，如[1,2,3]将分成[(1,2),(1,3),(2,3)]
        for each in subsets:
            each = list(each) #将元组转化为列表
            if each not in L_last:  ##子集是否 都为频繁项集
                return True
        return False

    def apriori_gen(self,L_last): #L_last means frequent(k-1) itemsets
        k = len(L_last[0]) + 1
        Ck = []
        ##
        for itemset1 in L_last:
            for itemset2 in L_last:
                #join step
                flag = 0
                for i in range(k-2):
                    if itemset1[i] != itemset2[i]:
                        flag = 1 ##若前k-2项中如果有一个项是不相等，新合并的集合是不可能是频繁项集
                        break
                if flag == 1:
                    continue
                if itemset1[k-2] < itemset2[k-2]:
                    c = itemset1 + [itemset2[k-2]]
                else:
                    continue

                #pruning setp
                if self.has_infrequent_subset(c,L_last,k):##判断子集是否为频繁项集
                    continue
                else:
                    Ck.append(c)
        return Ck

    def do(self):
        L_last = self.find_frequent_1_itemsets() ##过滤掉小于最小支持度阈值的物品
        L = L_last
        i = 0
        while L_last != []:
            Ck = self.apriori_gen(L_last) ##合并形成新的频繁项集
            FreqDic = {}
            for event in self.data:
                #get all suported subsets
                for c in Ck: ##统计新形成的频繁项集的个数
                    if set(c) <= set(self.data[event]):#判断新合成的频繁项目是否为数据记录的子集
                        if tuple(c) in FreqDic:
                            FreqDic[tuple(c)]+=1
                        else:
                            FreqDic[tuple(c)]=1
            # print FreqDic
            Lk = []
            for c in FreqDic:
                # print c
                # print '------'
                if FreqDic[c] > self.min_sup_val:##判断新形成的频繁项集是否大于最小支持度的阈值
                    Lk.append(list(c))
            L_last = Lk
            L += Lk
        return L  ## L就是新形成的频繁项集的集合

# #******Test******
# Data = {'T100':['I1','I2','I5'],
#         'T200':['I2','I4'],
#         'T300':['I2','I3'],
#         'T400':['I1','I2','I4'],
#         'T500':['I1','I3'],
#         'T600':['I2','I3'],
#         'T700':['I1','I3'],
#         'T800':['I1','I2','I3','I5'],
#         'T900':['I1','I2','I3']}
#
# a=Apriori(dataDic=Data)
# # print a.do()
# print Data
# print a.do()