import time
import os
import csv
from datetime import datetime
import re

def removeDSFile(processList):
    temp_list = [x for x in processList if x[0] is not '.']
    return temp_list


def tryint(s):                      
    try:
        return int(s)
    except ValueError:
        return s

def str2int(v_str):                
    return [tryint(sub_str) for sub_str in re.split('([0-9]+)', v_str)]

def sort_humanly(v_list):    
    return sorted(v_list, key=str2int)

# 去掉时间戳
def delet_timestamp(path_data,  path_save):
    result_list = []
    for x in removeDSFile(os.listdir(path_data)):
        result_list.append(x)
    # print(result_list)

    for filename in result_list:
        # 用下划线打乱再组合起来。不要第一个
        new_filename = '_'.join(filename.split('_')[1:])
        file_path =  os.path.join(path_data, filename)
        new_file_path = os.path.join(path_data, new_filename)
        os.rename(file_path, new_file_path)
        print(new_file_path)


delet_timestamp("data", "extract")








def extract_timestamp(input_list, path_data, path_save):
    result_list = input_list

    csv_list = []
    csv_list.append(input_list[0].split('/')[1].split("_Policy_")[0])
    totoal_minutes = 0
    Incomple_num = 10
    # 打开每个文件，抽取violation，计数，然后存入一个csv
    for file_path in result_list:
        comlete = False
        print(file_path)
        # 文件名
        filename = file_path.split('/')[1]
        # 打开后阅读, 对每一个文件读出Mintues
        with open (file_path, 'r', encoding='latin1') as Read:
            content_list = Read.readlines()
            # print(content_list[-1])
            # print(len(content_list))

        miutes = 0 
        for line in content_list:
            # # 判断是否跑完的, 这是读完的。
            if line.find("is violated") > -1:
                Incomple_num-=1
                comlete = True

            # 判断是Minitues大小
            if line.find('Minute') > -1:
                temp = line.split('Minute')
                temp = temp[1].split('for')[0].strip()
                miutes = int(float(temp)) if int(float(temp))   > miutes else miutes
        

        if comlete == False:
            miutes = 0
        # 找到最大的minites了，按顺序加入
        csv_list.append(str(miutes)) 
        totoal_minutes += miutes
        # print(miutes)


    csv_list.append(totoal_minutes)
    # print(Incomple_num)
    csv_list.append(str(Incomple_num))
    # print(csv_list)


    new_csv_list = []
    # new_csv_list.append(csv_list_title)
    new_csv_list.append(csv_list)
    # print(new_csv_list)
    with open('no_guided_results_detail.csv', 'a', newline='') as Write:
            writer = csv.writer(Write)
            writer.writerows(new_csv_list)





input_list_list = []
initial_file_index = 1

while initial_file_index <= 100:
    input_list = []
    for filename in os.listdir("data"): 
        key = "initial_parameters_20_" + str(initial_file_index) + "_"
        if filename.find(key) > -1 :
            input_list.append(os.path.join("data", filename))
            # print(filename)
    if len(input_list) == 10:
        input_list.sort(key=str2int)
        input_list_list.append(input_list)
    initial_file_index += 1

input_list_list.sort(key=lambda x:x[0])

# for x in input_list_list:
#     for y in x:
#         print(y)


# 创建新文件
csv_list_title = ["Initial Filename", "Policy 1",  "Policy 2",  "Policy 3",  "Policy 4",  "Policy 5",  "Policy 6",  "Policy 7",  "Policy 8",  "Policy 9",  "Policy 10", "Incomplete_policy", "Total_timestamp"]
with open('no_guided_results_detail.csv', 'w', newline='') as Write:
        writer = csv.writer(Write)
        writer.writerow(csv_list_title)

for initial_file in input_list_list:
    # extract_timestamp(input_list_list[0], "data", "extract")
    extract_timestamp(initial_file, "data", "extract")








