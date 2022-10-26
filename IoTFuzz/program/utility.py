import numpy as np
import os
import argparse
import configure_guide
import configure_inputs
import random

def removeDSFile(processList):
    temp_list = [x for x in processList if x[0] is not '.']
    return temp_list



def removeUsedExcel(excel_path, result_path):
    excel_list = []
    for x in removeDSFile(os.listdir(excel_path)):
        excel_list.append(x.split('.')[0])
    # print(excel_list)

    # result filename is 1659003678-2019-10-6.ini
    result_list = []
    for x in removeDSFile(os.listdir(result_path)):
        if (os.path.isfile(os.path.join(result_path, x))):
            temp = x.split('.')[0]
            result_list.append(temp)
    # print (result_list)

    return_list = []
    return_list  = [x + '.xlsx' for x in excel_list if x not in result_list]
    # print(return_list)
    print("Outdoor environment excel has ", str(len(excel_list)))
    print("Previous has simulated ", str(len(result_list)))
    print("Remaining is ", str(len(return_list)))

    return return_list




def parse_args():
    """
    :return:
    """
    description = "you should add those parameter"                   
    parser = argparse.ArgumentParser(description=description)        
                                
    help = "Please specify the type of simulation: env, ran, gui, and no_gui"                                     
    parser.add_argument('type', choices=['env', 'ran', 'gui', 'no_gui'], help = help)                   
    args = parser.parse_args()                                               
    return args



def initialValueAssign(self, blockName, minVal, maxVal):
    initalValue = random.randint(int(minVal), int(maxVal))
    self.eng.set_param(self.modelName + blockName, 'InitialValue', str(initalValue), nargout=0)

    return str(initalValue)






def createInitialParameters(section_num, file_index):     
    blockConfig = configure_guide.read_para("blockName.ini") 
    block_list = blockConfig["first"]["block_names"].split(',')

    inputConfig = configure_inputs.read_para() 

    temperature_min = int(inputConfig["environment_factors"]["temperature_min"])
    temperature_max = int(inputConfig["environment_factors"]["temperature_max"])
    humidity_min = int(inputConfig["environment_factors"]["humidity_min"])
    humidity_max = int(inputConfig["environment_factors"]["humidity_max"])
    odtemperature_min = int(inputConfig["environment_factors"]["odtemperature_min"])
    odtemperature_max = int(inputConfig["environment_factors"]["odtemperature_max"])
    odhumidity_min = int(inputConfig["environment_factors"]["odhumidity_min"])
    odhumidity_max = int(inputConfig["environment_factors"]["odhumidity_max"])

    file_path = "initial_parameters/initial_parameters_" + str(section_num) + "_" + str(file_index) + ".ini"
    for i in range(1, section_num+1):
        section = "initial_parameters_" + str(i)


        initial_value = random.randint(temperature_min, temperature_max)
        block = '/Data Store Memory-IDTemperature'
        configure_guide.write_para(file_path, section, block, str(initial_value))
        # 

        initial_value = random.randint(humidity_min, humidity_max)
        block = '/Data Store Memory-IDRHumidity'
        configure_guide.write_para(file_path, section, block, str(initial_value))
        # 
        initial_value = random.randint(odtemperature_min, odtemperature_max)
        block = '/Data Store Memory-ODTemperature'
        configure_guide.write_para(file_path, section, block, str(initial_value))
        # 
        initial_value = random.randint(odhumidity_min, odhumidity_max)
        block = '/Data Store Memory-ODRHumidity'
        configure_guide.write_para(file_path, section, block, str(initial_value))


        for block in block_list:
            # 
            initial_value = random.randint(0, 1)
            # 
            configure_guide.write_para(file_path, section, block, str(initial_value))
    print(file_path)


































