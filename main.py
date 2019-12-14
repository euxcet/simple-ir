# -*- coding: utf-8 -*-
from elastic import Elastic
import time
from tqdm import tqdm

elastic = Elastic()

def exception_handler(request, exception):
    print("Request failed")

def modify(line):
    x = line.split(' ')
    prev = "/w"
    for i in range(len(x)):
        nxt = "/w"
        if i + 1 < len(x):
            nxt = "/" + x[i + 1].split('/')[1]
        pre = prev
        prev = "/" + x[i].split('/')[1]
        x[i] = pre + x[i].split('/')[0] + nxt
    return " ".join(x)



def create_index():
    #print(elastic.delete_index())
    #print(elastic.create_index())
    fin = open("Sogou0000", "r", encoding = 'utf-8')
    for i in range(48000000):
        line = fin.readline()
        #print(line)
        #print(modify(line))
        elastic.insert_doc(line)
        if i % 5000 == 0:
            print(i)




if __name__ == '__main__':
    create_index()
    #print(elastic.insert_doc("中国/a 是/b 北京/c").json())
    #time.sleep(1)
    #print(elastic.search_doc("中国/.*").json())
