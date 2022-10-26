import time
import os
import csv
from datetime import datetime

def removeDSFile(processList):
    temp_list = [x for x in processList if x[0] is not '.']
    return temp_list



def extract(path_data, path_save):
    excel_list = []
    for x in removeDSFile(os.listdir(path_data)):
        excel_list.append(x)
    print(excel_list)

    csv_list = []
    csv_list_title = ["title", "total_violations", "total_minutes", "violations"]

    # 打开每个文件，抽取violation，计数，然后存入一个csv
    for excel in excel_list:
        # 文件路径
        excel_path = os.path.join(path_data, excel)
        # 打开后阅读
        with open (excel_path, 'r', encoding='latin1') as Read:
            content_list = Read.readlines()
            # print(content_list)

        # violation总个数
        violation_num = 0
        # 多少时间步有负数policy总个数
        minute_num = 0
        # 哪些policy出问题
        policy_list = []

        temp_result = []
        result = []
        for line in content_list:
            if (line.find("Minute") > -1):
                # temp_result暂时保存Minute和负数policies，
                # 如果不大于1个，证明这个时间步没有violation
                if (len(temp_result) > 1):
                    result.extend(temp_result)
                    minute_num+=1

                # 为下一个时间步重置temp_result 
                temp_result = []
                temp_result.append(line)
            if (line.find("Global distance is -") > - 1):
                temp_result.append(line)
                violation_num+=1
                policy_str = line.split(':')[0]
                policy_No = policy_str.split(' ')[2]
                if (policy_No not in policy_list):
                    policy_list.append(policy_No)
                # print(policy_list)

        # 抽取violation存入新文件
        saved_excel_path = os.path.join(path_save, excel)
        with open (saved_excel_path, 'w') as Write:
            Write.writelines(result)
        print(excel.split('.')[0])


        # 抽取信息写入csv
        # title, total_violations, total_minutes, violations
        csv_list.append([excel.split('.')[0], violation_num, minute_num, '-'.join(policy_list)])
    
    # 排序
    csv_list.sort(key=(lambda date: datetime.strptime(date[0], "%Y-%m-%d")))
    # csv_list = sorted(csv_list,key=(lambda date: datetime.strptime(date[0].split[','][-1], "%Y-%m-%d")))
    new_csv_list = []
    new_csv_list.append(csv_list_title)
    new_csv_list.extend(csv_list)
    # print(csv_list)
    with open('results_detail.csv', 'w', newline='') as Write:
            writer = csv.writer(Write)
            writer.writerows(new_csv_list)



extract("data", "extract")





# policy 9 文本有问题，修正
def change(path_data, path_save):
    excel_list = []
    for x in removeDSFile(os.listdir(path_data)):
        excel_list.append(x)
    print(excel_list)

    # 打开每个文件，抽取violation，计数，然后存入一个csv
    for excel in excel_list:
        # 文件路径
        excel_path = os.path.join(path_data, excel)
        # 打开后阅读
        with open (excel_path, 'r') as Read:
            content_list = Read.readlines()
            # print(content_list)
        result = []
        for line in content_list:
            if (line.find("Policy is 9") > -1):
                line = line.replace('\n', ' ')
            if (line.find("temperature is above a threshold and no one is at home") > - 1):
                line = line.lstrip()
            result.append(line)


        saved_excel_path = os.path.join(path_save, excel)
        with open (saved_excel_path, 'w') as Write:
            Write.writelines(result)
        print(excel)








