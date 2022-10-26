


import configparser

# file_path = "guide_save_pair.ini"




def read_para(file_path):
	config = configparser.ConfigParser()
	config.optionxform = lambda option: option
	config.read(file_path)
	return config


def write_para(file_path, section, item, value):
    config = configparser.ConfigParser()
    config.optionxform = lambda option: option
    config.read(file_path)

	

 	# Check the section exist 
    if (config.has_section(section) == False): 
        config[section] = {}
    config.set(section, item, value)

    with open(file_path, 'w') as configfile:
        config.write(configfile)








































# filepath = os.path.join(os.getcwd(),'config.ini')
# cp = configparser.ConfigParser()
# cp.read(filepath)

# #删除
# cp.remove_option('addtest1','province')#删除option
# cp.remove_section('addtest2')#删除section
# with open(filepath,'w+') as f:
#     cp.write(f)







