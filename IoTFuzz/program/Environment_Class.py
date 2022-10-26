
import matlab.engine
import matplotlib.pyplot as plt
import os
import time
import numpy as np
import save_simulation_results as ssr
import random


class SimEnv:
    def __init__(self, config, excelFilePath):      
        # Read data from config
        self.config = config
        self.excelFilePath = excelFilePath
        self.excelFileName = self.excelFilePath.split('/')[-1]
        self.resultPath = config["simulation"]["result_path"]
        #The name of the Simulink Model (To be placed in the same directory as the Python Code) 
        self.modelName = config["simulation"]["model_name"] 
        self.stop_time = config["simulation"]["stop_time"]

        self.home_mode = config["environment_factors"]["home_mode"]

        self.temperature_initial = config["environment_factors"]["temperature_initial"]
        self.temperature_min = config["environment_factors"]["temperature_min"]
        self.temperature_max = config["environment_factors"]["temperature_max"]
        self.humidity_initial = config["environment_factors"]["humidity_initial"]        
        self.humidity_min = config["environment_factors"]["humidity_min"]
        self.humidity_max = config["environment_factors"]["humidity_max"]

        self.PolicyThresholdTemperatureMax = int(config["environment_factors"]["PolicyThresholdTemperatureMax"])
        self.PolicyThresholdTemperatureMin = int(config["environment_factors"]["PolicyThresholdTemperatureMin"])
        self.PolicyThresholdHumidityMin = int(config["environment_factors"]["PolicyThresholdHumidityMin"])
        self.PolicyThresholdHumidityMax = int(config["environment_factors"]["PolicyThresholdHumidityMax"])


        # Saved name 
        self.timestamp = self.excelFileName.split('.')[0]
        # self.timestamp = str(round(time.time())) + "-" + self.excelFileName.split('.')[0]
        self.dict = {}

        

    # Specify Outdoor environment file
    def inputsEnvironment(self):
        self.eng.set_param(self.modelName + '/OutDoor_weather_spreadsheet','FileName', self.excelFilePath, nargout=0)
        self.Excel = self.eng.get_param(self.modelName + '/OutDoor_weather_spreadsheet','FileName')
        print("The outdoor file is ", self.Excel)
        # outdoor environment added


    # Specify initial value to blocks
    def initialValueAssign(self, blockName, initalValue):
        self.eng.set_param(self.modelName + blockName, 'InitialValue', initalValue, nargout=0)

    def initialParameters(self):
        # self.eng.set_param(self.modelName+'/PhysicalEnv', 'Open', "on", nargout=0)
        # fig = self.eng.set_param(self.modelName+'/PhysicalEnv', 'OpenAtSimulationStart', 'true', nargout=0)
        self.initialValueAssign('/Data Store Memory-IDTemperature', self.temperature_initial)
        self.initialValueAssign('/Data Store Memory-IDRHumidity', self.humidity_initial)
        self.initialValueAssign('/Data Store Memory-homeRead', self.home_mode)




    def randomInitialAssign(self, randmValue, blockName, initalValue):
        if (random.random() < randmValue):
            self.eng.set_param(self.modelName + blockName, 'InitialValue', initalValue, nargout=0)

    def humanInteraction(self):
        # Human interaction, random specify the value to device
        self.randomInitialAssign(0.05, '/Data Store Memory-heater', "1")
        self.randomInitialAssign(0.04, '/Data Store Memory-AC', "1")
        self.randomInitialAssign(0.03, '/Data Store Memory-light', "1")
        self.randomInitialAssign(0.1,  '/Data Store Memory-door', "1")
        self.randomInitialAssign(0.01, '/Data Store Memory-motion', "1")
        self.randomInitialAssign(0.3,  '/Data Store Memory-presence', "1")



    def connectToMatlab(self):
        print("Starting MATLAB")
        self.eng = matlab.engine.start_matlab("-logfile 'log.txt'")
        print("Connected to MATLAB")
        
        #Load the model
        # self.eng.eval("model = '{}'".format(self.modelName),nargout=0)
        # self.eng.eval("load_system(model)",nargout=0)
        self.eng.load_system(self.modelName)
        print("Loading Simulink model - " + self.modelName) 
        
        # Outdoor environment, change name of spreadsheet
        self.inputsEnvironment()

        # Send initial parameters to simulation
        self.initialParameters()

        print("Initialized Model")
        # stop time
        self.eng.set_param(self.modelName,'StopTime', self.stop_time, nargout=0)




        #Start Simulation and then Instantly pause
        self.eng.set_param(self.modelName,'SimulationCommand','start','SimulationCommand','pause',nargout=0)







 
        
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




    # The corresponding data cannot be found in the workspace here, and I don't know what is wrong
    # It can only be forcibly read with the eval function
    # After reading it out, it is mlarray.double, which is converted to numpy.ndarry type with np.asarray
    # ndarry is 2-dimensional, as many rows of data as there are time steps, only one column
    # So read the latest data as [-1][0], of type numpy.float64
    # Note that the data in simulink should be changed to array, 2D, important
    def simulate(self):
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



            simu_info = "Minute " + str(self.getLastValue(self.TimeStep)) + " for simulation" + \
                        ", The indoor temperature is " + str(self.getLastValue(self.IDTemperature)) + \
                        "℃, The indoor relative humidity is " + str(self.getLastValue(self.IDRHumidity)) + \
                        "%, The outdoor temperature is " + str(self.getLastValue(self.ODTemperature)) + \
                        "℃, The outdoor relative humidity is " + str(self.getLastValue(self.ODRHumidity)) + \
                        "%, Home mode is " + str(self.getLastValue(self.HomeMode)) 
            # simu_info = "The simulation is runing for " + str(self.getLastValue(self.TimeStep))  
            print(simu_info)
            self.writeLog(simu_info)
            # Write data and send to checker np.around( [-1][0], 2)
            self.checkEngine()


    def checkEngine(self):
        self.check1()
        self.check2()
        self.check3()
        self.check4()
        self.check5()
        self.check6()
        self.check7()
        self.check8()
        self.check9()
        self.check10()
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
            with open(os.path.join(self.resultPath, self.timestamp) + ".ini", 'a+', encoding='utf-8') as res_write:
                res_write.write(content)
                res_write.write('\n')



    # ndarry is a 2-D array, it gers -1 row and first column, two decimal places
    def getLastValue(self, SimulinkValue):
        return np.around(SimulinkValue[-1][0], 2)

    def check1(self):
        # State global variables
        # ----------------------- (start) The AC and heater must not be on at the same time. -----------------------
        # Propositional distances
        # 0: turn off, 1: turn on
        x = 0
        y = 0
        # np.around(self.Heater[-1][0], 2)
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

        # print(target_param)
        string = "Policy is 1: " + target_param + \
                 ", Heater state is " + str(heater) + \
                 ", AC state is " + str(ac) + \
                 ", Global distance is " + str(Global_distance)
        self.writeLog(string)
        # print("Heater state is " + str(heater))
        # print("AC state is " + str(ac))
        # print("Global distance is " + str(Global_distance))
        print(string)


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
        self.writeLog(string)
        # print("Heater state is " + str(heater))
        # print("Window state is " + str(window))
        # print("Global distance is " + str(Global_distance))
        print(string)




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
        self.writeLog(string)
        # print("Heater state is " + str(light))
        # print("Presence state is " + str(presence))
        # print("Global distance is " + str(Global_distance))
        print(string)



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
        self.writeLog(string)
        # print("Light state is " + str(light))
        # print("Motion state is " + str(motion))
        # print("Global distance is " + str(Global_distance))
        print(string)        




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
        self.writeLog(string)
        # print("Heater state is " + str(heater))
        # print("IDTemperature state is " + str(idtemperature))
        # print("Global distance is " + str(Global_distance))
        print(string)



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
                 "%, Threshold is " + str(self.PolicyThresholdHumidityMin) + \
                 "%, Global distance is " + str(Global_distance)
        self.writeLog(string)
        # print("Heater state is " + str(heater))
        # print("IDRHumidity state is " + str(idrhumidity))
        # print("Global distance is " + str(Global_distance))
        print(string)




    def check7(self):
        # An vent is turned ON when humidity is detected to above the threshold.
        x = 0
        y = 0
        vent = self.getLastValue(self.Vent)
        idrhumidity = self.getLastValue(self.IDRHumidity)
        # P1
        # if idrhumidity > self.PolicyThresholdHumidityMax:
        x = (idrhumidity - self.PolicyThresholdHumidityMax) / idrhumidity
        # P2
        if vent > 0:
            y = -1
        else:
            y = 1
        


        target_param = "An vent must be ON when humidity is detected to above the threshold."
        count = 0

        Global_distance = -1 * (min(x, y))

        string = "Policy is 7:" + target_param + \
                 ", Vent state is " + str(vent) + \
                 ", IDRHumidity state is " + str(idrhumidity) + \
                 "%, Threshold is " + str(self.PolicyThresholdHumidityMax) + \
                 "%, Global distance is " + str(Global_distance)
        self.writeLog(string)
        # print("Heater state is " + str(vent))
        # print("IDTemperature state is " + str(idrhumidity))
        # print("Global distance is " + str(Global_distance))
        print(string)




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
        self.writeLog(string)
        # print("Presence state is " + str(presence))
        # print("IDTemperature state is " + str(idtemperature))
        # print("Global distance is " + str(Global_distance))
        print(string)





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
        self.writeLog(string)
        # print("Heater state is " + str(heater))
        # print("Presence state is " + str(presence))
        # print("IDTemperature state is " + str(idtemperature))
        # print("Global distance is " + str(Global_distance))
        print(string)




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
        self.writeLog(string)
        # print("Humidifier state is " + str(humidifier))
        # print("IDTemperature state is " + str(idrhumidity))
        # print("Global distance is " + str(Global_distance))
        print(string)



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
        self.writeLog(string)
        # print("Window state is " + str(window))
        # print("HomeMode state is " + str(homeMode))
        # print("Global distance is " + str(Global_distance))
        print(string)
        # print("!!!!!!!!!!!!", homeMode)





    def disconnect(self):
        self.eng.set_param(self.modelName,'SimulationCommand','stop',nargout=0)
        self.eng.quit()



