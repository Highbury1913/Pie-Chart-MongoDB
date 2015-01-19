########
### Make a pie charts of varying size - see
### http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.pie for the docstring.
########
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from pymongo import MongoClient
from matplotlib.widgets import Slider, Button, RadioButtons
from bson.objectid import ObjectId

connection = MongoClient("mongodb://student:readOnly@ds041180.mongolab.com:41180/utsa_db")
SensorData = connection.utsa_db.SensorData
SensorType = connection.utsa_db.SensorType
Sensor = connection.utsa_db.Sensor

SensorTypeDict = {}
SensorTypelabels = []
for x in SensorType.find():
	SensTypeTypeID = x['_id']
	SensTypeDescription=x['Description']
	tempdict = {SensTypeTypeID:SensTypeDescription}
	SensorTypeDict.update(tempdict)
for k,v in SensorTypeDict.items():
	SensorTypelabels.append(v)

SensorDict = {}
Sensorlabels = []
for x in Sensor.find():
	SensID = x['_id']
	SensTypeID=x['TypeID']
	tempdict = {SensID:SensTypeID}
	SensorDict.update(tempdict)
for k,v in SensorDict.items():
	Sensorlabels.append(v)

# The dictionary.get() below allows you to tie the 1000 (SensorID) to the SensorTypeDescription  so 1000 -> RTU1, 1001 -> RTU2, 1004 -> SMALL UNIT, etc.
#trial1 = SensorTypeDict.get((SensorDict.get(%s))) %key
#print(trial1)



dictArray = {}
nDates = int(SensorData.count())		#1440 number of minutes in a day; 9 sensors
key=[]
value=[]
Eng = 0
id = nDates/2
for x in SensorData.find({"_id":id}):
	date = x['Date']
	#xEnergy=x['Energy']
	#xEnergy=xEnergy.replace('\n','')
	#xSensorID=x['SensorID']
	#dict = {xSensorID:xEnergy}
#	print(date)
	#dictArray.update(dict)
	#Eng +=float(xEnergy)		#Total energy consumed in that day/time
for x in SensorData.find({"Date": {'$regex': date}}):
	xDate=x['Date']
	xEnergy=x['Energy']
	xEnergy=xEnergy.replace('\n','')
	xSensorID=x['SensorID']
	dict = {xSensorID:xEnergy}
	dictArray.update(dict)
	Eng +=float(xEnergy)		#Total energy consumed in that day/time
for k,v in dictArray.items():
	key.append(k)
	value.append(float(v)/Eng*100.0)
	
################ WORKS BUT RETURNS SUM OF ENERGY AS ZERO
###totalEnergy = SensorData.aggregate({"$group":{"_id":"$Date", "total":{"$sum":"$Energy"}}})
###print("Total Energy:")
###print(totalEnergy)
################

fig, axarr = plt.subplots(2)
fig.canvas.set_window_title('Relative Energy Usage Per Sensor Per Minute')

# Draw the pie chart
axarr[0].set_title(date)
l = axarr[0].pie(value,labels=key, autopct='%1.1f%%', shadow=True)
axarr[0].set_position([0.1,0.2,.75,.75])

# Draw the slider
axarr[1].set_position([0.1, 0.1, 0.8, 0.03])
record = Slider(axarr[1],'Date',2000,nDates,valinit=(nDates)/2)

# Update the pi chart based off of the record 
def update(val):
	axarr[0].clear()
	id = int(val)
	print('Record Number: ' +str(id))
	dictArray = {}
	key=[]
	value=[]
	Eng = 0
	for x in SensorData.find({"_id":id}):
		date = x['Date']
	for x in SensorData.find({"Date": {'$regex': date}}):
		xDate=x['Date']
		xEnergy=x['Energy']
		xEnergy=xEnergy.replace('\n','')
		xSensorID=x['SensorID']
		dict = {xSensorID:xEnergy}
		dictArray.update(dict)
		Eng +=float(xEnergy)		#Total energy consumed in that day/time
	for k,v in dictArray.items():
		key.append(k)
		value.append(float(v)/Eng*100.0)
	axarr[0].set_title(date)
	l = axarr[0].pie(value,labels=key, autopct='%1.1f%%', shadow=True)
	fig.canvas.draw_idle()
	
	ID2Desc = []
	for k in key:
		x = SensorTypeDict.get(SensorDict.get(k))
		ID2Desc.append(x)
		

	axarr[0].legend(ID2Desc,loc='upper right',bbox_to_anchor=(1.15, 1),prop={'size':8})

record.on_changed(update)	
ID2Desc = []
for k in key:
	x = SensorTypeDict.get(SensorDict.get(k))
	ID2Desc.append(x)
	

axarr[0].legend(ID2Desc,loc='upper right',bbox_to_anchor=(1.15, 1),prop={'size':8})
plt.show()