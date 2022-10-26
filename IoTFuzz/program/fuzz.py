import sys, os

import time
import random
import utility



args = utility.parse_args()
print("You are going to simulation", args.type, "type")




# 1. read inputs, open simulators
import configure_inputs
config = configure_inputs.read_para()
# print(config["simulation"]["stop_time"])
# print(type(config["simulation"]["stop_time"]))


# 2. simulate every step, check violations
import open_simulator
if (args.type  == "env"):
	# Simulate environment 
	open_simulator.OutDoorEnvironmentExperiments(config)

elif (args.type  == "no_gui"):
	# Simulate no guide
	open_simulator.NoGuideExperiments(config)
else:
	pass

