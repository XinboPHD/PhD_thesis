
# TAESim
This is a MATLAB implementation of the trigger-action environment
It includes cyberspace/physical channels, rules, and devices to create trigger-action environment implementations for smart home scenarios.
Also act as basis of IoTFuzz.


### Abstract
TAESim is a simulation testbed to support reusable simulations in the research of IoT safety and security, especially for the IoT activities in home automation that could involve possibly unexpected interactions. TAESim operates over MATLAB/Simulink and constructs a digital twin for modeling the nature of the trigger-action environment using simulations. It is an open-access platform and can be used by the research community, government, and industry who work toward preventing the safety and security consequences in the IoT ecosystem. In order to evaluate the effectiveness and efficiency of the testbed, we conduct some experiments and the results show that the simulations are completed in a few seconds. We also present two case studies that can report unexpected consequences.


### Devices
In this section, we present the way to model the IoT devices in this testbed. Simulink provides a block, Data Store Memory, to store a global variable during the simulation. It meets the demands of the modeling status of the device (e.g. on and off). For example, in the Figure below, a Data Store Memory block stores the device state. It allows to specify value 0 or 1 to each Data Store Memory block representing "on" or "off" for status of the relevant device. 

![Image text](https://github.com/XinboPHD/PhD_thesis/blob/main/TAESim/images/AC.png)

### Channels
A device can affect one or multiple physical channels. In an IoT environment, the automation is achieved by producing interactions via channels. There are two kinds of channels including cyberspace channels and physical channels. The equation of indoor temperature gain/loss is shown below:

<img src="https://github.com/XinboPHD/PhD_thesis/blob/main/TAESim/images/temperature%20loss.jpg" width="40%" >


### Apps
Home automation rules, called IoT apps, are the core of the smart home to automatically trigger the devices to act. Generally, the IoT apps have three elements: trigger event, condition, and action event. The trigger event is either a specific action of a device such as turning on/off or reaching a threshold in a physical channel such as temperature. The condition is optional in IoT apps and can be either from cyberspace or physical space. The figure shows an app named ‘Turn off light if motion detected’. It is an official SmartApp from the SmartThings community written in the Groovy programming language.

<img src="https://github.com/XinboPHD/PhD_thesis/blob/main/TAESim/images/app.jpg" width="50%" >




# Installation 

TAESim is supported by MATLAB/Simulink. 

The following instructions assume you are using Python 3 and a Debian-based (like Ubuntu) installation.

.. note::

   MATLAB/Simlink is commercial product developed by MathWorks. You may have to purchace liciences or apply access from institutions and universities for academic purpose.


### Parameters

By default, TAESim has default values for the parameters. We use the default parameters for evaulation. Please refer to parameters [here](https://github.com/XinboPHD/PhD_thesis/blob/main/TAESim/data.m) or find more details in [paper](https://beauban.github.io/papers/TAESim.pdf).



# License
---------

This project is licensed under the MIT License - see the [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
 file for details.
