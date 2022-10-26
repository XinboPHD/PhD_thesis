


import configparser

file_path = "parameters.ini"




def read_para():
	config = configparser.ConfigParser()
	config.read(file_path)
	return config


def write_para(section, item, value):
    config = configparser.ConfigParser()
    config.read(file_path)


 	# Check the section exist 
    if (config.has_section(section) == False): 
        config[section] = {}
    config.set(section, item, value)

    with open(file_path, 'w') as configfile:
        config.write(configfile)







