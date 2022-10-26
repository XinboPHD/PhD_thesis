

import configparser

# file_path = "results.ini"




def read_simu_res():
	config = configparser.ConfigParser()
	config.read(file_path)
	return config


def write_simu_res(section, item, value, file_path):
    config = configparser.ConfigParser()



 	# Check the section exist 
    if (config.has_section(section) == False): 
        config[section] = {}
    config.set(section, item, value)

	# wirte agian then effect
    with open(file_path, 'w') as configfile:
        config.write(configfile)







