import sys
import time
import os
os.chdir("digital_twin") 
import Environment_Class as env
import NoGuide_Class as no_gui
import configure_inputs
import utility

# Outdoor environment
def lanuch(config, excelfilePath):
	simulation = env.SimEnv(config, excelfilePath)
	#Establishes a Connection
	simulation.connectToMatlab()

	# #Instantiates the controller
	# checker = env.PolicyChecker()
	# simulation.connectChecker(checker)

	# #Control Loop
	simulation.simulate()

	# Generate a figure 
	# simulation.plot()

	#Closes Connection to MATLAB
	simulation.disconnect()


def OutDoorEnvironmentExperiments(config):
	print("Outdoor environment simulation starts")

	excelPath = config["simulation"]["excel_path"]
	resultPath = config["simulation"]["result_path"]
	# 
	excelRemainList = utility.removeUsedExcel(excelPath, resultPath)
	for excelfilename in excelRemainList:
		excelfilePath = os.path.join(excelPath, excelfilename)
		lanuch(config, excelfilePath)
















# No Guide
def lanuch_no_guide(config, initial_para_filename):
	simulation = no_gui.SimNoGui(config)

	# #Control Loop
	for policy_num in range(1, 11):
		#Establishes a Connection
		simulation.connectToMatlab()

		simulation.simulate(policy_num, initial_para_filename)


		#Closes Connection to MATLAB
		simulation.disconnect()


def NoGuideExperiments(config):
	print("No Guide simulation starts")
	# 
	# initial_parameters_path = 
	# 
	initial_para_file_list = []
	for temp_file in os.listdir(config["simulation"]["initial_parameters_path"]):
		if temp_file.find('.ini') > -1:
			initial_para_file_list.append(temp_file)

	print("Experiments files have " + str(len(initial_para_file_list)))

	for initial_para_filename in initial_para_file_list:
		lanuch_no_guide(config, initial_para_filename)














