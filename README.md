# PhD Thesis: Protect Smart Homes from Vulnerabilities: Large-Scale Testbed, Static and Dynamic Techniques

Everything about research work, source code, and datasets mentioned in the thsis. Demos can be found [here](https://www.youtube.com/watch?v=sm9jo6eM7ds) demonstrating the work.

_ _ _

## [Table of contents](README.md)
* Structure of Thesis & Completed Work 
* Introduction
* Literature Review
  * Physical devices
  * Operation rules
  * Communication
* TAESim: A Testbed for IoT Security Analysis of Trigger-Action Environment
* Topic Generation of Smart Homes for Security, Safety, and Privacy Analysis
* IoTFuzz: Automated Discovery of Violations in Smart Homes with Real Environment
_ _ _

### Structure of Thesis & Completed Work
<p>Abstract:</p>
<p>The IoT ecosystem that integrates the digital system with the physical world has markedly changed the way people live and work. The rapid development of
emerging technologies, such as 5G, is bringing about a paradigm shift in IoT history. Meanwhile, security is one of the paramount research problems in IoT as the creation of new scenarios and architectures introduces previously unknown security threats in addition to the traditional ones. Undoubtedly, finding vulnerabilities in the IoT ecosystem is more vital than ever. The various security vulnerabilities lead to a few security domains in the IoT ecosystem including physical devices, execution rules, and communication. Research communities have conducted a significant amount of work in the field of vulnerability discovery by utilizing diverse code analysis techniques based on different types of code, such as source code, binary code, and especially novel types of code, etc. With a focus on the security domains, we investigate the emerging research by reviewing recent representative work that appeared in the dominant period. We provided a roundup and a research outlook of the developing area, IoT vulnerability discovery with code intelligence. Specifically, we review recent representative work published in the dominant time to investigate the emerging research and summarize the research methodology commonly adopted in this fast-growing area. To investigate the impacts of physical interactions on IoT safety and security, we introduce a simulation testbed to support reusable simulations in the research of IoT safety and security, especially for the IoT activities in home automation that could involve possibly unexpected interactions. The testbed operates over MATLAB/Simulink and constructs a digital twin for modeling the nature of the trigger-action environment using simulations. Besides, the IoT-based smart home relies on textual language to express its functionalities for users. To improve the understanding of smart home scenarios, we propose a smart home scenario generation assistant for generating smart home usages and providing specific scenarios for security, safety, and privacy analysis. Specifically, it generates realistic and comprehensible home automation rules as synthetic data, that reflects the intended use cases for various scenarios, which reveals potential risks of security, safety, and privacy. Moreover, given the generated home automation rules and scenarios, we use pre-trained contextual embeddings and Topic Modeling to cluster them into groups of scenarios, enabling scenario understanding of particular IoT applications. Moreover, many work attempts to provide defense mechanisms to ensure IoT safety and security through statically analyzing scenarios without the effects of physical environment and runtime information. To address these problems, we propose a fuzzing framework to dynamically check the cyber security and physical safety aspects of smart homes with respect to targeted policies. It can mutate the inputs from policies, human activities, indoor environment, and reallife outdoor weather conditions. In addition to the binary status of devices, the continuous-value status in smart homes is leveraged to perform mutation and simulation. For large-scale testing, the fuzzing framework uses digital twins to simulate normal behaviors, the impacts of the outdoor environment, and human activities in smart homes.</p>




|Chapter         | Source code          | Paper accepted by|
|:-------------|:------------------|:------|
|Literature Review    |[Reviewed papers](https://github.com/BeauBan/Recent-IoT-based-Smart-Home-Security-and-Safety-Paper)     |[International Conference on Network and System Security (NSS), 2022](https://dl.acm.org/doi/abs/10.1007/978-3-031-23020-2_15)) |
|TAESim: A Testbed for IoT Security Analysis of Trigger-Action Environment    |[TAESim](https://github.com/XinboPHD/PhD_thesis/tree/main/TAESim)    |[European Symposium on Research in Computer Security (ESORICS), 2022](https://beauban.github.io/papers/TAESim.pdf) |
|Automatic Topic Generation of Smart Homes for Security, Safety, and Privacy Analysis     |[SHSGen](https://github.com/XinboPHD/PhD_thesis/tree/main/SHSGen)     |Under review |
|IoTFuzz: Automated Discovery of Violations in Smart Homes with Real Environment     |[IoTFuzz](https://github.com/XinboPHD/PhD_thesis/tree/main/IoTFuzz)    |Under reivew |


_ _ _


### Literature Review
Part of the content comes from our survey paper: A Survey on IoT Vulnerability Discovery

#### Physical devices
<p> The devices are the core components and play an essential role in the IoT ecosystem, not only interacting with every part in IoT including cloud backends, mobile phones, hubs, physical environment but also controlling the factors of the real-world. Meanwhile, the products on markets highly likely contain the known but have not been fixed vulnerabilities. For example, zero-day vulnerabilities are totally new threats to security in the IoT ecosystem.</p>

#### Operation rules
<p>Home automation solutions are mainly provided by Samsung SmartThings and IFTTT, which have the largest share market of smart home based platforms. The SmartThings environment is consisted of four main components: a hub, a companion mobile app, a cloud backend, and an IoT device. Each hub supports several radio protocols such as ZWave,Wi-Fi, and ZigBee to communicate with physical products in the ecosystem. End-users can control the hub, devices, and install SmartApps from a special app store through companion mobile apps. The cloud backend is used to run SmartApps and device handlers, which represent the software wrappers for IoT devices. IFTTT allows end-users to facilitate inter-operability with devices or online services to link various automation via web management. The rules are usually published by third-parties as recipes or applets. In each of the rules, it contains a trigger event, an optional condition, and one or more actions.</p>

#### Communication
<p>In the IoT ecosystem, data is transmitted among devices, mobile phones, cloud backends based on several protocols. Communication is vital in the IoT ecosystem since the core functionalities of IoT are automation and data transmission. The tasks of communication include connection, pairing, binding, and transmission. The different architectures and scenarios of IoT have their own ways of building communication protocols and standards. The security of key information protection in the communication channels relies on the design of tbe communication scheme. Thus, it is important to figure out the message specified in different protocols for further analysis.</p>


_ _ _
### [TAESim: A Testbed for IoT Security Analysis of Trigger-action Environment](https://beauban.github.io/papers/TAESim.pdf)
<p>Abstract:</p>
<p>The Internet of Things (IoT) networks promote significant convenience in every aspect of our life, including smart vehicles, smart cities, smart homes, etc. With the advancement of IoT technologies, the IoT platforms bring many new features to the IoT devices so that these devices can not only passively monitor the environment (e.g. conventional sensors), but also interact with the physical surroundings (e.g. actuators). In this light, new problems of safety and security arise due to the new features. For instance, the unexpected and undesirable physical interactions might occur among devices, which is known as inter-rule vulnerability. A few work have investigated the inter-rule vulnerability from both cyberspace and physical channels. Unfortunately, only few research papers take advantage of run-time simulation techniques to properly model trigger action environments. Moreover, no simulation platform is capable of modeling primary physical channels and studies the impacts of physical interactions on IoT safety and security. In this paper, we introduce TAESim, a simulation testbed to support reusable simulations in the research of IoT safety and security, especially for the IoT activities in home automation that could involve possibly unexpected interactions. TAESim operates over MATLAB/Simulink and constructs a digital twin for modeling the nature of the trigger-action environment using simulations. It is an open-access platform and can be used by the research community, government, and industry who work toward preventing the safety and security consequences in the IoT ecosystem. In order to evaluate the effectiveness and effciency of the testbed, we conduct some experiments and the results show that the simulations are completed in a few seconds. We also present two case studies that can report unexpected consequences.</p>


_ _ _
### Automatic Topic Generation of Smart Home IoT for Security, Safety, and Privacy Analysis
<p>Abstract:</p>
<p>The user demands for seamless automation of devices have driven the development of the smart home, in which the Internet of Things (IoT) ecosystem embraces a new trend of personal customization. Popular platforms such as IFTTT enable automation through trigger-action programming, enabling efficient automation with minimum human intervention. IoT devices react to not only cyberspace but also the physical environment, giving rise to potential issues in computing-related security, human’s life safety, and user’s privacy. Recent research analyzes the home automation rules, attempting to speculate the practical and innovative usage of IoT devices through hypothesizing a specific combination of rules among thousands of services. However, the current methods lack comprehensible scenario understanding, which imposes restrictions on the smart home IoT applications due to security, safety, and privacy concerns. In this paper, we propose a smart home scenario generation assistant, SHSGEN, for generating smart home usages and providing specific scenarios for security, safety and privacy analysis. Specifically, it generates realistic and comprehensible home automation rules as synthetic data, that reflects the intended use cases for various scenarios, which reveals potential risks of security, safety and privacy. Moreover, given the generated home automation rules and scenarios, we use pre-trained contextual embeddings and Topic Modeling to cluster them into groups of scenarios, enabling scenario understanding of particular IoT applications. SHSGEN can help researchers and engineers in policy development by using a large number of useful scenarios in an intelligent, automatic, and flexible way. We conduct several experiments to demonstrate the reasonability, comprehensibility, and validity of the generated scenarios, and the representativeness of the generated topics. The results show that SHSGEN can learn the inherent logic from scenarios created by a user, and then generate reasonable, comprehensible and valid scenarios. The generated topics are shown to be representative in smart home deployments.</p>


_ _ _
### IoTFuzz: Automated Discovery of Violations in Smart Homes with Real Environment
<p>Abstract:</p> 
<p>Smart homes (SHs) are becoming increasingly intelligent these days, including environment management, home automation, and human-machine interactions. However, safety and security risks of SHs restrict their wide adoption. This paper proposes a fuzzing framework, IoTFuzz, to dynamically check the cyber security and physical safety aspects of SHs. IoTFuzz mutates the inputs from policies, human activities, indoor environment, and real-life outdoor weather conditions. In addition to the binary status of devices, the continuous-value status in SHs is leveraged to perform mutation and simulation. The policies are expressed as temporal logic formulas with time constraints to report violations. Moreover, for large-scale testing, IoTFuzz uses digital twins to simulate normal behaviors, the impacts of the outdoor environment, and human activities in SHs. IoTFuzz can also intelligently infer rule-policy correlation based on Natural Language Processing (NLP) techniques. We evaluate IoTFuzz with 15 rules and 10 pre-defined unique policies. Our extensive evaluations illustrate that IoTFuzz can effectively reveal the impacts of real-life outdoor weather on SHs resulting in a maximum of 4154 violations and a minimum of 41 violations in different weather from experiments of 8 years. IoTFuzz also discovers that a maximum of 35.4% improper human activities can lead the risky situations for SHs.</p>





<!-- 
[back](https://github.com/skyInGitHub/PhD_thesis) -->
