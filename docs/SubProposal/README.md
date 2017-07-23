# Title:
Autonomous Robot Cluster or Design and implementation of a self driving car network

# Abstract & Objective:
The objective of this project is to create a network of self driving cars. The cars will be taught to drive using machine learning and positional data acquired either through sensors on the vehicle or a camera above. Once the cars are able to follow any path or road we will introduce an intersection. Routing at the intersection will be done by the server back end of the network. Based on when the cars are arriving and where they need to go the server will tell them how they should behave at the intersection. This routing will also be achieved by machine learning. Once a single intersection with two cars can be handled we will continue to expand the system until we run out of time. The next step would be adding more cars to a single intersection system; followed by adding more intersections.

# Citations:
### [Cite 1] [Author]
	Description: Description of citation and how it pertains to project.
### [Cite 2] [Author]
	Description: Description of citation and how it pertains to project.

# Bill of Material:
	Note: This is a preliminary estimation of what we would be expecting to spend. Subject to change or increase. All Prices in CAD.
Per robot unit:

### MCU: PIC18F45K40-I/P-ND – $3.11
![alt text](http://i.imgur.com/0FfDsOo.jpg "PIC18F45K40-I/P-ND")
	Description: 40-Pin 8-bit MCU unit from MicroChip. Reason for using this MCU is that there is a familiar IDE for use with the line of product, and there is also a IEEE 802.15.4 compatible Tranciever that we would want to use in this project.
URL: https://www.digikey.ca/short/3vhwbw

### MRF24J40MAT-I/RMCT-ND Unit – $14.70
![alt text](http://i.imgur.com/TrBCVn9.jpg "MRF24J40MAT-I/RMCT-ND")
	Description: MicroChip brand RF Tranciever Module, for this project we are hoping to use IEEE Standard 802.15.4 radios to creat a network of functional robots, more specificaly we are hoping to use a popular protocol known as ZigBee to achive this. 

This RF module is compatable with ZigBee and we hope to use this to connect to the SPI interface of our MCU unit. The RF module will send instructions to the MCU to make it carry out tasks. 

There are many RF modules to chose from, so we may experiment and research others while working on the project.
URL: https://www.digikey.ca/short/3vhwbf


### Motor x2 - $0.59
![alt text](http://i.imgur.com/VG4MF6S.jpg "DC Motor")
	Description: Simple DC Motor, we would use an H-Bridge circuit to properly drive the control of the motors, would use simple controls to control direction of robot.

### L293D H-Bridge Circuit - $0.45
![alt text](http://i.imgur.com/KcCCGoF.jpg "L293D H-Bridge Circuit")
	Description: H-Bridge Circuit IC. Since we are trying to build a simple car, we would control the two motors and their direction using a simple H-Bridge IC. It would be directly connected to the MCU's GPIO.

### Base station:
USB-OTG interface - $?.??
	Desc:

# Tasks & Roadmap:

### September:
	-Research ZigBee protocol
	-Develop software simulation of P2P communication network/neural net
### October:
	-Prototype hardware implementation for robot/basestation
	-Develop software for base station
### November:

### December:

### January:

### February:
	-Work on presentation/report
### March:
