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




## Violation discovered by IoTFuzz
If you want to closely look into bug cases discovered by IoTFuzz, please review the paper (will be published soon). 
<img  src="https://github.com/XinboPHD/PhD_thesis/blob/main/IoTFuzz/images/policy.png">





## Demonstration videos
### Case 1
- <a href="https://youtu.be/EiWLCj-pQ7M"> Correct behavior of the parachute </a>
- <a href="https://youtu.be/nhmKE03-bnk"> (i) Buggy behavior of the parachute and (ii) parachute operations after patching the bug</a>  
<br> <b>Q</b>: Why is this case a logic bug? <br>
<b>A</b>: the ArduPilot official documentation states that the following four conditions must hold to deploy a parachute while preserving the drone safety: (1) the motors must be armed, (2) the vehicle must not be in the FLIP or ACRO flight modes, (3) the barometer must show that the
vehicle is not climbing, and (4) the vehicle’s current altitude must be above the CHUTE_ALT_MIN parameter value. <br>
we found that ArduPilot improperly checks the first three requirements. 
This leads to a policy violation where the vehicle deploys the parachute when it is climbing, causing it to crash on the ground. 




##  NLP Analysis
Here, I would like to explain how to use NLP techniques to find correlation between rules and policies. ArduPilot to a bitcode file because I got several emails asking about it.

### 1) Environment
- ArduPilot: copter 4.1 version (https://github.com/ArduPilot/ardupilot/commit/68619c308737e5199992a9523bacabe9710c8e7e)
- LLVM 13.0.0
- Ubuntu 20.04

