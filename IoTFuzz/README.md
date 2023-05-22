# IoTFuzz

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-red.svg)](#python)

IoTFuzz is a fuzzing framework for smart homes with real environment. You can freely use it to define and find more violations. By creating a digital twin and specifying a metric temporal logic (MTL) formula, IoTFuzz is able to mutate inputs related to the formula and use real-world weather data to discover more interesting violations. 


##  Overiview
IoTFuzz mutates the inputs from policies, human activities, indoor environment, and real-life outdoor weather conditions. In addition to the binary status of devices, the continuousvalue status in SHs is leveraged to perform mutation and simulation. The policies are expressed as temporal logic formulas with time constraints to report the violations. Moreover, for large-scale testing, IoTFuzz uses digital twins to simulate normal behaviors, the impacts of the outdoor environment, and human activities in SHs. IoTFuzz can also intelligently infer rule-policy correlation based on Natural Language Processing (NLP) techniques.

<img  src="https://github.com/XinboPHD/PhD_thesis/blob/main/IoTFuzz/images/overview.png">



##  Setup
We assume that you already finished installation for MATLAB/Simulink, on Windows, MacOS or Ubuntu LTS / Debian Linux. <br>

- <a href="https://www.mathworks.com/content/dam/mathworks/mathworks-dot-com/academia/student-competitions/best-robotics/files/Installation_of_MATLAB_and_Simulink.pdf"> MATLAB and Simulink installation </a>
- <a href="https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html"> MATLAB API for Python installation </a>

Note: Use MATLAB 2020b and later version for succesful run.

<b>Install others</b> <br>
* Python = 3.6.13
* matlabengineforpython = R2020b
* numpy=1.19.2

<b>Download source code</b> <br>
```
git clone https://github.com/XinboPHD/PhD_thesis/IoTFuzz.git
```



## Virtural Machine
If you use vitural machine to build environment, I would recommand you to download the virtual machine image and run IoTFuzz.

OS: Windows 10 (Suggest turning off automatical update)

User name: administrator

No password

Conda environment name: IoTFuzz

We pre-install IoTFuzz and relevant softwares in a virutal machine, built in Windows 10 OS. It can be download from here. 
The virtual machine is created in VMware Fusion. The environment can succesfully support IoTFuzz running.


Note: MATLAB requires liciences to use. The MATLAB in virtual machine is deactivated. IoTFuzz can run after is activated. Otherwise it reports an error.


## Usage
### Python Function
On a high level, we provide a python script fuzz and python objects. The function provides all the supported features while the fuzzing process launch simulator to dynamically test digital twin. Check our demo to see how to use these two interfaces. Please refer to `fuzz.py` for implementation details.

### Arguments 
To run IoTFuzz, the script needs a arguments to specify the fuzzing type. We provide two fuzzing types as follow:

Using the test cases from real-life weather

```
python fuzz.py env
```

Or, use the randomly generated testcase,
```
python fuzz.py no_gui
```

If no argument is given, the program is terminated and you will get 

```
usage: fuzz.py [-h] {env,ran,gui,no_gui}
fuzz.py: error: the following arguments are required: type
```

`parameters.ini` indicates the simulation configuration. Change some value to conduct the experiments on other datasets.
For fuzzing type `env`, change `excel_path = Outdoor_weather/xlsxNoNoise/YearbyYear/2015` to use different dataset.
For fuzzing type `no_gui`,  `initial_parameters_path = initial_parameters/Experiments_used` specify the input folder, either change the documnets in this folder or change path.


### Result
The results are saved in folder `result` for both fuzzing types. Raw data records the details of simulation and checking results. A script is provided to extract and summary the results.



## Violation discovered by IoTFuzz
If you want to closely look into bug cases discovered by IoTFuzz, please review the paper (will be published soon). 
<img  src="https://github.com/XinboPHD/PhD_thesis/blob/main/IoTFuzz/images/policy.png">





## Demonstration videos
- <a href="https://youtu.be"> A demo for smart home protection </a>





##  NLP Analysis
Here, I would like to explain how to use NLP techniques to find correlation between rules and policies. ArduPilot to a bitcode file because I got several emails asking about it.

A Correlation Engine that leverages NLP in the design of text similarity computation architecture, an overview of which is given as follow. It is defined as a classification task, using a pre-trained language model to specify whether a policy should be included. To simplify the analysis of unstructured text, it first performs Part-of-Speech (POS) tagging and decompose the key terms of SHs. Nouns are the key terms that are further processed to find the maps of rules and policies. 

<img  src="https://github.com/XinboPHD/PhD_thesis/blob/main/IoTFuzz/images/NLP.png">

This figure shows the a example of POS tagging and the nouns are easily found in the textual sentence. For example, "When humidity is below the threshold, turn on the humidifier" has 2 terms, a device humidifier and physical channel humidity, expressed as nouns in this rule. We extract nouns and construct a collection of them (humidifier, humidity).

<img width = "500" src="https://github.com/XinboPHD/PhD_thesis/blob/main/IoTFuzz/images/PosTagging.png">

<!-- ## Tips
 -->

