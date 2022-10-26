
import matlab.engine
import matplotlib.pyplot as plt
import os
import sys
import time
import numpy as np
import save_simulation_results as ssr
import random
import configparser
import configure_guide

class SimNoGui:
    def __init__(self, config):      
        # Read data from config
        self.config = config 
        # self.pairConfig = configure_guide.read_para("../guide_save_pair.ini") 
        self.blockConfig = configure_guide.read_para("../blockName.ini") 


        self.limit_time = config["simulation"]["limit_time"] 
        self.print_details = config["program_configs"]["print_details"] 


        self.resultPath = config["simulation"]["result_path_no_guide"] 
        #The name of the Simulink Model (To be placed in the same directory as the Python Code) 
        self.modelName = config["simulation"]["model_name_no_guide"] 
        self.simu_circle_time = config["simulation"]["simu_circle_time"] 
        self.start_time = 0
        self.stop_time = 0

        self.home_mode = config["environment_factors"]["home_mode"]
        self.temperature_initial = config["environment_factors"]["temperature_initial"]
        self.temperature_min = config["environment_factors"]["temperature_min"]
        self.temperature_max = config["environment_factors"]["temperature_max"]
        self.humidity_initial = config["environment_factors"]["humidity_initial"]        
        self.humidity_min = config["environment_factors"]["humidity_min"]
        self.humidity_max = config["environment_factors"]["humidity_max"]
        self.odtemperature_initial = config["environment_factors"]["odtemperature_initial"]
        self.odtemperature_min = config["environment_factors"]["odtemperature_min"]
        self.odtemperature_max = config["environment_factors"]["odtemperature_max"]
        self.odhumidity_initial = config["environment_factors"]["odhumidity_initial"]        
        self.odhumidity_min = config["environment_factors"]["odhumidity_min"]
        self.odhumidity_max = config["environment_factors"]["odhumidity_max"]
        self.PolicyThresholdTemperatureMax = int(config["environment_factors"]["PolicyThresholdTemperatureMax"])
        self.PolicyThresholdTemperatureMin = int(config["environment_factors"]["PolicyThresholdTemperatureMin"])
        self.PolicyThresholdHumidityMin = int(config["environment_factors"]["PolicyThresholdHumidityMin"])
        self.PolicyThresholdHumidityMax = int(config["environment_factors"]["PolicyThresholdHumidityMax"])

        # self.paraList = [self.vent, self.window, self.humidifier, self.motion, self.presence, self.tv, self.door,\
        #                    self.ac, self.light, self.heater, self.coffeMachine]
        self.paraList = ['/Data Store Memory-IDTemperature', '/Data Store Memory-IDRHumidity', \
                         '/Data Store Memory-ODTemperature', '/Data Store Memory-ODRHumidity', \
                         '/Data Store Memory-Vent', '/Data Store Memory-window', \
                         '/Data Store Memory-humidifier', '/Data Store Memory-motion', \
                         '/Data Store Memory-presence', '/Data Store Memory-TV', \
                         '/Data Store Memory-AC', '/Data Store Memory-light', \
                         '/Data Store Memory-heater', '/Data Store Memory-coffeeMachine']        
        # self.timestamp = str(round(time.time()))
        self.timestamp = str(round(time.time()))
        self.realTimestamp = self.timestamp
        self.dict = {}
        self.temp_Global_distance = sys.maxsize





    def initialValueAssign(self, blockName, minVal, maxVal):
        initalValue = random.randint(int(minVal), int(maxVal))
        self.eng.set_param(self.modelName + blockName, 'InitialValue', str(initalValue), nargout=0)
        string =  "Initial value of block " +  blockName +  " is " + str(initalValue)
        # Write log
        self.writeLog(string)
        return str(initalValue)


    def initialValueAssignOne(self, blockName, initalValue):
        self.eng.set_param(self.modelName + blockName, 'InitialValue', str(initalValue), nargout=0)
        string =  "Initial value of block " +  blockName +  " is " + str(initalValue)
        self.writeLog(string)


    def initialParameters(self):
        for item in self.running_parameters:
            # print(type(item))
            # print(type(item[0]))
            # print(type(item[-1]))
            self.initialValueAssignOne(item[0], item[-1])
            pass







    def connectToMatlab(self):
        print("Starting MATLAB")
        self.eng = matlab.engine.start_matlab("-logfile 'log.txt'")
        print("Connected to MATLAB")
        
        #Load the model
        # self.eng.eval("model = '{}'".format(self.modelName),nargout=0)
        # self.eng.eval("load_system(model)",nargout=0)
        self.eng.load_system(self.modelName)
        print("Loading Simulink model - " + self.modelName) 





    def start_stop_time_random(self):
        self.start_time = self.stop_time
        self.stop_time = self.start_time + random.randint(1, int(self.simu_circle_time))

        
    def setControlAction(self,u):
        #Helper Function to set value of control action
        self.eng.set_param('{}/u'.format(self.modelName),'value',str(u),nargout=0)
    

    def getHistory(self, var_name):
        # Helper Function to get History, 
        # Here cannot get workspace, only use eval to get
        # mlarry type is not resoleved. here change to ndarry
        # size is 2
        # out = self.eng.workspace['out']
        return np.asarray(self.eng.eval(var_name))


    def connectChecker(self, checker):
        self.checker = checker
        # self.controller.initialize()


    def secondsToMintuesHours(self, total_second):
        hour = total_second // 3600
        minute = total_second // 60 % 60
        second = total_second % 60
        return int(hour), int(minute), int(second)




    def randomSelectBlockAndAssign(self):
        # 
        temp_list = self.blockConfig["first"]["block_names"].split(',')
        # 
        random_value = random.randint(1, len(temp_list) + 4)
        random_block = ""
        if (random_value == 1):
            mutateValue = self.initialValueAssign('/Data Store Memory-IDTemperature', self.temperature_min, self.temperature_max)
            random_block = '/Data Store Memory-IDTemperature'

        elif (random_value == 2):
            mutateValue = self.initialValueAssign('/Data Store Memory-IDRHumidity', self.humidity_min, self.humidity_max)
            random_block = '/Data Store Memory-IDRHumidity'
    
        elif (random_value == 3):
            mutateValue = self.initialValueAssign('/Data Store Memory-ODTemperature', self.odtemperature_min, self.odtemperature_max)
            random_block = '/Data Store Memory-ODTemperature'
    
        elif (random_value == 4):
            mutateValue = self.initialValueAssign('/Data Store Memory-ODRHumidity', self.odhumidity_min, self.odhumidity_max)
            random_block = '/Data Store Memory-ODRHumidity'
    
        else:
            mutateValue = self.initialValueAssign(temp_list[random_value - 5], 0, 1)
            random_block = temp_list[random_value-5]


        self.initialValueAssignOne(random_block, mutateValue)

        return random_block, mutateValue



    def setValueFromLastSimu(self):
        self.initialValueAssignOne('/Data Store Memory-IDTemperature', str(self.getLastValue(self.IDTemperature)))
        self.initialValueAssignOne('/Data Store Memory-IDRHumidity', str(self.getLastValue(self.IDRHumidity)))
        self.initialValueAssignOne('/Data Store Memory-ODTemperature', str(self.getLastValue(self.ODTemperature)))
        self.initialValueAssignOne('/Data Store Memory-ODRHumidity', str(self.getLastValue(self.ODRHumidity)))
        self.initialValueAssignOne('/Data Store Memory-Vent', str(self.getLastValue(self.Vent)))
        self.initialValueAssignOne('/Data Store Memory-window', str(self.getLastValue(self.Window)))
        self.initialValueAssignOne('/Data Store Memory-humidifier', str(self.getLastValue(self.Humidifier)))
        self.initialValueAssignOne('/Data Store Memory-motion', str(self.getLastValue(self.Motion)))
        self.initialValueAssignOne('/Data Store Memory-presence', str(self.getLastValue(self.Presence)))
        self.initialValueAssignOne('/Data Store Memory-TV', str(self.getLastValue(self.TV)))
        self.initialValueAssignOne('/Data Store Memory-AC', str(self.getLastValue(self.AC)))
        self.initialValueAssignOne('/Data Store Memory-light', str(self.getLastValue(self.Light)))
        self.initialValueAssignOne('/Data Store Memory-heater', str(self.getLastValue(self.Heater)))
        self.initialValueAssignOne('/Data Store Memory-coffeeMachine', str(self.getLastValue(self.CoffeeMachine)))



    def simulate(self, policy_num, initial_para_filename):
        # Record the simulation times
        self.simu_times = 0
        self.policy_num = policy_num


        
        self.program_start_time = time.time() 

        for temp_file in os.listdir(self.config["simulation"]["initial_parameters_path"]):
            if temp_file.find('.ini') > -1:
                self.initial_parameter_file = self.config["simulation"]["initial_parameters_path"] + "/" + initial_para_filename
        self.initial_parameter_fileName = initial_para_filename # initial_para filename
        self.initial_parameter_config = configure_guide.read_para(self.initial_parameter_file) # configuration file
        print("Initial parameters is from " + self.initial_parameter_file )


        self.timestamp = self.realTimestamp + "_" + self.initial_parameter_fileName.split(".")[0] + "_Policy_" + str(self.policy_num)
        policy_str = "Checking Policy " + str(self.policy_num)
        print(self.timestamp)
        print(policy_str)
        self.writeLog("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")


        self.current_section = "initial_parameters_" + str(self.policy_num)
        #  runing_parameters is all item in this section
        self.running_parameters = self.initial_parameter_config.items(self.current_section)
        self.initialParameters()



        self.start_time = 0
        self.stop_time = 0





        while int(self.limit_time) > (time.time() - self.program_start_time):
            print("Initialized Model")


            self.start_stop_time_random()

            self.eng.set_param(self.modelName,'StartTime', str(self.start_time), nargout=0)

            self.eng.set_param(self.modelName,'StopTime', str(self.stop_time), nargout=0)

            


            if (self.simu_times > 0):
                self.setValueFromLastSimu()


            self.simu_times = self.simu_times + 1 



            random_block, random_value = self.randomSelectBlockAndAssign()

            string_mutate = "\nSelect block parameter: " + str(random_block) + \
                            ", and mutate the value: " + str(random_value)
            self.writeLog(string_mutate)

            


            hour, minute, second = self.secondsToMintuesHours((time.time() - self.program_start_time))

            program_info = "No guide simulation " + str(self.simu_times) + " time \n" + \
                           "This guide simulation starts " + str(self.start_time) + ", and ends in " + str(self.stop_time) + "\n" + \
                           "Main program has simulated: " + str(hour) + " hours " + str(minute) + " minutes, " + str(second) + ", seconds"

            self.writeLog(program_info)


            #Start Simulation and then Instantly pause
            self.eng.set_param(self.modelName,'SimulationCommand','start','SimulationCommand','pause',nargout=0)


            # Control Loop
            while(self.eng.get_param(self.modelName,'SimulationStatus') != ('stopped' or 'terminating')):
                #Pause the Simulation for each timestep
                self.eng.set_param(self.modelName,'SimulationCommand','continue','SimulationCommand','pause',nargout=0)
                self.TimeStep = self.getHistory('out.TimeStep')
                self.IDTemperature = self.getHistory('out.IDTemperature')
                self.ODTemperature = self.getHistory('out.ODTemperature')
                self.IDRHumidity = self.getHistory('out.IDRHumidity')
                self.ODRHumidity = self.getHistory('out.ODRHumidity')
                self.HomeMode = self.getHistory('out.HomeMode')
                self.Heater = self.getHistory('out.Heater')
                self.AC = self.getHistory('out.AC')
                self.Window = self.getHistory('out.Window')
                self.Light = self.getHistory('out.Light')
                self.Door = self.getHistory('out.Door')
                self.Motion = self.getHistory('out.Motion')
                self.Presence = self.getHistory('out.Presence')
                self.Vent = self.getHistory('out.Vent')
                self.Humidifier = self.getHistory('out.Humidifier')
                self.TV = self.getHistory('out.TV')
                self.CoffeeMachine = self.getHistory('out.CoffeeMachine')






                hour, minute, second = self.secondsToMintuesHours((time.time() - self.program_start_time))

                program_info = "No guide simulation " + str(self.simu_times) + " time \n" + \
                               "This no guide simulation starts " + str(self.start_time) + ", and ends in " + str(self.stop_time) + "\n" + \
                               "\033[5;34mMain program has simulated: " + str(hour) + " hours " + str(minute) + " minutes, " + str(second) + ", seconds\033[0m"
                print(program_info)
                simu_info = "\nCheck times is " + str(self.getLastValue(self.TimeStep) - self.start_time) + \
                            ", Minute " + str(self.getLastValue(self.TimeStep)) + " for simulation" + \
                            ", The indoor temperature is " + str(self.getLastValue(self.IDTemperature)) + \
                            "℃, The indoor relative humidity is " + str(self.getLastValue(self.IDRHumidity)) + \
                            "%, The outdoor temperature is " + str(self.getLastValue(self.ODTemperature)) + \
                            "℃, The outdoor relative humidity is " + str(self.getLastValue(self.ODRHumidity)) + \
                            "%, Home mode is " + str(self.getLastValue(self.HomeMode))
                print(simu_info)
                self.writeLog(simu_info)

                Global_distance = self.checkEngine(self.policy_num)



                if  Global_distance < 0:
                    vio_str = "Policy " + str(self.policy_num) + " is violated"
                    self.writeLog(vio_str)
                    print(vio_str)
                    self.eng.set_param(self.modelName,'SimulationCommand','stop',nargout=0)
                    return

                


    def checkEngine(self, which_policy):
        Global_distance = sys.maxsize
        if (which_policy == 1):
             Global_distance = self.check1()

        elif (which_policy == 2):
             Global_distance = self.check2()

        elif (which_policy == 3):
             Global_distance = self.check3()

        elif (which_policy == 4):
             Global_distance = self.check4()

        elif (which_policy == 5):
             Global_distance = self.check5()

        elif (which_policy == 6):
             Global_distance = self.check6()

        elif (which_policy == 7):
             Global_distance = self.check7()

        elif (which_policy == 8):
             Global_distance = self.check8()

        elif (which_policy == 9):
             Global_distance = self.check9()

        elif (which_policy == 10):
             Global_distance = self.check10()

        else:
            pass
        return Global_distance
        
        # self.check11()


    def plot(self):
        plt.figure()
        plt.plot(self.TimeStep, self.IDTemperature, color='red', linewidth=2, linestyle='--', label = 'IDTemperature')
        plt.plot(self.TimeStep, self.ODTemperature, color='blue', linewidth=2, linestyle='x', label = 'ODTemperature')
        plt.plot(self.TimeStep, self.IDRHumidity, color='black', linewidth=2, linestyle=':', label = 'IDRHumidity')
        plt.plot(self.TimeStep, self.ODRHumidity, color='darkgreen', linewidth=2, linestyle='>', label = 'ODRHumidity')
        plt.xlabel('Minutes')
        plt.ylabel('Temperature/Relative Humidity')
        plt.savefig(os.path.join(self.resultPath, self.timestamp) + ".png")
        # plt.show()


    def writeLog(self, content):
            with open(self.resultPath + "/" + self.timestamp + ".ini", 'a+', encoding='utf-8') as res_write:
                res_write.write(content)
                res_write.write('\n')




    def getLastValue(self, SimulinkValue):
        return np.around(SimulinkValue[-1][0], 2)



    def printAndSaveResults(self, string, Global_distance):
        # save file
        self.writeLog(string)
        if self.print_details == "yes":
            print(string)
        else:
            if (Global_distance < 0):
                print(string)



    def check1(self):
        # State global variables
        # ----------------------- (start) The AC and heater must not be on at the same time. -----------------------
        # Propositional distances
        # 0: turn off, 1: turn on
        x = 0
        y = 0
        heater = self.getLastValue(self.Heater)
        ac = self.getLastValue(self.AC)

        # P1
        if heater > 0:
            x = 1
        else:
            x = -1
        # P2
        if ac > 0:
            y = 1
        else:
            y = -1

        target_param = "Heater and AC turn on together"
        count = 0


        Global_distance = -1 * (min(x, y))
        string = "Policy is 1: " + target_param + \
                 ", Heater state is " + str(heater) + \
                 ", AC state is " + str(ac) + \
                 ", Global distance is " + str(Global_distance)
        self.printAndSaveResults(string, Global_distance)
        return Global_distance






    def check2(self):
        # ----------------------- (start) The windows must be open when heater is on. -----------------------
        x = 0
        y = 0
        heater = self.getLastValue(self.Heater)
        window = self.getLastValue(self.Window)
        # P1
        if heater > 0:
            x = 1
        else:
            x = -1
        # P2
        if window  > 0:
            y = -1
        else:
            y = 1



        target_param = "If heater is on, windows must be open"
        count = 0


        Global_distance = -1 * (min(x, y))

        string = "Policy is 2:" + target_param + \
                 ", Heater state is " + str(heater) + \
                 ", Window state is " + str(window) + \
                 ", Global distance is " + str(Global_distance)
        self.printAndSaveResults(string, Global_distance)
        return Global_distance





    def check3(self):
        # ----------------------- (start) The light must be on then the user arrives home. -----------------------
        x = 0
        y = 0
        light = self.getLastValue(self.Light)
        presence =  self.getLastValue(self.Presence)
        # P1
        if presence > 0:
            x = 1
        else:
            x = -1
        # P2
        if light > 0:
            y = -1
        else:
            y = 1

        target_param = "If the user arrives home, the light must be on "
        count = 0


        Global_distance = -1 * (min(x, y))

        string = "Policy is 3:" + target_param + \
                 ", Light state is " + str(light) + \
                 ", Presence state is " + str(presence) + \
                 ", Global distance is " + str(Global_distance)
        self.printAndSaveResults(string, Global_distance)
        return Global_distance




    def check4(self):
        # ----------------------- (start) The lights must be turned on if the motion sensor is active. -----------------------
        x = 0
        y = 0
        light = self.getLastValue(self.Light)
        motion = self.getLastValue(self.Motion)
        # P1
        if motion > 0:
            x = 1
        else:
            x = -1
        # P2
        if light > 0:
            y = -1
        else:
            y = 1

        target_param = "The lights must be turned on if the motion sensor is active"
        count = 0


        Global_distance = -1 * (min(x, y))


        string = "Policy is 4: " + target_param + \
                 ", Light state is " + str(light) + \
                 ", Motion state is " + str(motion) + \
                 ", Global distance is " + str(Global_distance)
        self.printAndSaveResults(string, Global_distance)
        return Global_distance




    def check5(self):
        # Turn on the heater, if the temperature is below the threshold.
        x = 0
        y = 0
        heater = self.getLastValue(self.Heater)
        idtemperature = self.getLastValue(self.IDTemperature)
        # P1
        x = (self.PolicyThresholdTemperatureMin - idtemperature)/self.PolicyThresholdTemperatureMin
        # P2
        if heater > 0:
            y = -1
        else:
            y = 1


        target_param = "Turn on the heater, if the temperature is below the threshold"
        count = 0


        Global_distance = -1 * (min(x, y))


        string = "Policy is 5: " + target_param + \
                 ", Heater state is " + str(heater) + \
                 ", IDTemperature is " + str(idtemperature) + \
                 "℃, Threshold is " + str(self.PolicyThresholdTemperatureMin) + \
                 ", Global distance is " + str(Global_distance)
        self.printAndSaveResults(string, Global_distance)
        return Global_distance



    def check6(self):
        # An humidifier is turned ON when humidity is detected to below the threshold.
        x = 0
        y = 0
        humidifier = self.getLastValue(self.Humidifier)
        idrhumidity = self.getLastValue(self.IDRHumidity)
        # P1
        # if idrhumidity < self.PolicyThresholdHumidityMin:
        x = (self.PolicyThresholdHumidityMin - idrhumidity) / self.PolicyThresholdHumidityMin
        # P2
        if humidifier > 0:
            y = -1
        else:
            y = 1


        target_param = "An humidifier must be ON when humidity is detected to below the threshold."
        count = 0


        Global_distance = -1 * (min(x, y))

        string = "Policy is 6:" + target_param + \
                 ", Humidifier state is " + str(humidifier) + \
                 ", IDRHumidity is " + str(idrhumidity) + \
                 "%, Threshold is " + str(self.PolicyThresholdHumidityMax) + \
                 "%, Global distance is " + str(Global_distance)
        self.printAndSaveResults(string, Global_distance)
        return Global_distance





    def check7(self):
        # An vent is turned ON when humidity is detected to above the threshold.
        x = 0
        y = 0
        vent = self.getLastValue(self.Vent)
        idrhumidity = self.getLastValue(self.IDRHumidity)
        # P1
        # if idrhumidity > self.PolicyThresholdHumidityMax:
        x = (idrhumidity - self.PolicyThresholdHumidityMax) / idrhumidity
        if vent > 0:
            y = -1
        else:
            y = 1
        # P2


        target_param = "An vent must be ON when humidity is detected to above the threshold."
        count = 0


        Global_distance = -1 * (min(x, y))

        string = "Policy is 7:" + target_param + \
                 ", Vent state is " + str(vent) + \
                 ", IDRHumidity state is " + str(idrhumidity) + \
                 "%, Threshold is " + str(self.PolicyThresholdHumidityMin) + \
                 "%, Global distance is " + str(Global_distance)
        self.printAndSaveResults(string, Global_distance)
        return Global_distance





    def check8(self):
        # Temperature should be within a predefined range when people are at home.
        x = 0
        y = 0
        z = 0
        presence = self.getLastValue(self.Presence)
        idtemperature = self.getLastValue(self.IDTemperature)
        # P1
        if presence > 0:
            x = 1
        else:
            x = -1
        # P2
        # if idtemperature > self.PolicyThresholdTemperatureMax:
        y = (idtemperature - self.PolicyThresholdTemperatureMax) / idtemperature
        # P3
        # if idtemperature < self.PolicyThresholdTemperatureMin:
        z = (self.PolicyThresholdTemperatureMin - idtemperature) / self.PolicyThresholdTemperatureMin



        target_param = "Temperature should be within a predefined range when people are at home."
        count = 0

        Global_distance = -1 * (min(x, max(y, z)))



        string = "Policy is 8:" + target_param + \
                 ", Presence state is " + str(presence) + \
                 ", IDTemperature is " + str(idtemperature) + \
                 "℃, Threshold is " + str(self.PolicyThresholdTemperatureMin) + \
                 "℃ and " + str(self.PolicyThresholdTemperatureMax) + \
                 "℃, Global distance is " + str(Global_distance)
        self.printAndSaveResults(string, Global_distance)
        return Global_distance






    def check9(self):
        # The heater should be turned off when temperature is above a threshold and no one is at home.
        x = 0
        y = 0
        z = 0
        heater = self.getLastValue(self.Heater)
        presence = self.getLastValue(self.Presence)
        idtemperature = self.getLastValue(self.IDTemperature)
        # P1
        # if idtemperature > self.PolicyThresholdTemperatureMax:
        x = (idtemperature - self.PolicyThresholdTemperatureMax) / idtemperature
        # P2
        if presence > 0:
            y = -1
        else:
            y = 1
        # P3
        if heater > 0:
            z = 1
        else:
            z = -1

        target_param = "The heater should be turned off when temperature is above a threshold and no one is at home."

        count = 0



        Global_distance = -1 * (min(min(x,y), z))

        string = "Policy is 9: " + target_param + \
                 ", Heater state is " + str(heater) + \
                 ", Presence state is " + str(presence) + \
                 ", IDTemperature is " + str(idtemperature) + \
                 "℃, Threshold is " + str(self.PolicyThresholdTemperatureMax) + \
                 "℃, Global distance is " + str(Global_distance)
        self.printAndSaveResults(string, Global_distance)
        return Global_distance





    def check10(self):
        # Turn off the humidifier, if a related room’s humidity exceeds the threshold
        x = 0
        y = 0
        humidifier = self.getLastValue(self.Humidifier)
        idrhumidity = self.getLastValue(self.IDRHumidity)
        # P1
        # if idrhumidity > self.PolicyThresholdHumidityMax:
        x = (idrhumidity - self.PolicyThresholdHumidityMax) / idrhumidity
        # P2
        if humidifier > 0:
            y = 1
        else:
            y = -1


        target_param = "Humidifier must be off, if a related room’s humidity exceeds the threshold"
        count = 0

        Global_distance = -1 * (min(x, y))



        string = "Policy is 10: " + target_param + \
                 ", humidifier state is " + str(humidifier) + \
                 ", IDRHumidity state is " + str(idrhumidity) + \
                 "%, Threshold is " + str(self.PolicyThresholdHumidityMax) + \
                 "%, Global distance is " + str(Global_distance)
        self.printAndSaveResults(string, Global_distance)
        return Global_distance




    def check11(self):
        # All window and blinds should be closed when home mode is away.
        x = 0
        y = 0
        window = self.getLastValue(self.Window)
        homeMode = self.getLastValue(self.HomeMode)
        # P1
        if window > 0:
            x = -1
        else:
            x = 1
        # P2
        if homeMode != 2:
            y = 1
        else:
            y = -1

        target_param = "All window and blinds should be closed when home mode is away."
        count = 0

        Global_distance = -1 * (min(x, y))


        string = "Policy is 11: " + target_param + \
                 ", window state is " + str(window) + \
                 ", homeMode state is " + str(homeMode) + \
                 ", Global distance is " + str(Global_distance)
        self.printAndSaveResults(string, Global_distance)








    def disconnect(self):
        self.eng.set_param(self.modelName,'SimulationCommand','stop',nargout=0)
        self.eng.quit()

















