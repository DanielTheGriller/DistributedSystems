""" Daniel Linna
	0509355
	28.2.2020 """
import os
import pickle 
import json
import xml.etree.ElementTree as ET
import msgpack
import yaml
from timeit import default_timer as timer
import matplotlib as mpl
import matplotlib.pyplot as plt 

mpl.use('WebAgg')
mpl.rc('webagg', address='0.0.0.0', port='8000')
""" This program serializes and deserializes data
using different formats. It compares the processing times
and file sizes of each formats using bar graphs. """

# Defining example data to use for serialization
exampledata = {
	"user": {
		"firstname": "Brian",
		"lastname": "Brooks",
		"age": 25,
	},
	"address": {
		"street": "Example Street",
		"streetnumber": 124,
		"zip-code": 53110,
		"country": "Finland"
	},
	"employment": {
		"education": "Master of Science",
		"specialization": "Information technology",
		"job": "Senior Programmer"
	},
	"family": {
		"married": "Yes",
		"children": 2
	}
}

# Function which serializes data using Pickle
def pickling():
	pickleFile = open("serialized.pickle","wb")
	pickle.dump(exampledata,pickleFile)
	pickleFile.close()


# Function which deserializes Pickled data
def unpickling():
	unpickleFile = open("serialized.pickle", "rb")
	new_data = pickle.load(unpickleFile)
	unpickleFile.close()


# Function which serializes data using JSON
def serializerJSON():
	jsonFile = open("serialized.json", "w")
	json.dump(exampledata, jsonFile)
	jsonFile.close()


# Function which deserializes JSON-formatted data
def deserializerJSON():
	jsonFile = open("serialized.json", "r")
	new_data = json.load(jsonFile)
	jsonFile.close()


# Function which serializes data using XML
def serializerXML():
	elem = ET.Element('SerializedData')
	for key, val in exampledata.items():
		child = ET.Element(key)
		for subkey, subval in val.items():
			grandchild = ET.SubElement(child,subkey)
			grandchild.text = str(subval)
		elem.append(child)

	xmlFile = open("serialized.xml", "wb")
	xmlFile.write(ET.tostring(elem))
	xmlFile.close()

	
# Function which deserializes XML-formatted data
def deserializerXML():
	tree = ET.parse("serialized.xml")
	data = tree.getroot()


# Function which serializes data using MessagePack
def serializerMessagePack():
	msgpackFile = open("serialized.msgpack", "wb")
	msgpack.pack(exampledata, msgpackFile)
	msgpackFile.close()
	

#Function which deserializes .msgpack formatted data
def deserializerMessagePack():
	msgpackFile = open("serialized.msgpack", "rb")
	data = msgpack.unpack(msgpackFile)
	msgpackFile.close()


# Function which serializes data using YAML
def serializerYAML():
	yamlFile = open("serialized.yaml", "w")
	yaml.dump(exampledata, yamlFile)
	yamlFile.close()


# Function which deserializes YAML formatted data
def deserializerYAML():
	yamlFile = open("serialized.yaml", "r")
	data = yaml.load(yamlFile, Loader=yaml.FullLoader)
	yamlFile.close()


""" This function calculates the process time when serializing or
deserializing data. The functions are called 99 times to get 
a consistent time which is comparable to other formats. This is 
done because the input data is so small, that the differences would
be random if functions were called only once. """
def timecalculator(function):
	processStart = timer()
	for i in range(1,100):
		function()
	processEnd = timer()
	processTime = processEnd-processStart
	return processTime


# Defining lists needed to put functions as parameters to timecalculator()
list_of_ser_functions = [pickling, serializerJSON, serializerXML, serializerMessagePack, serializerYAML]
list_of_deser_functions = [unpickling, deserializerJSON, deserializerXML, deserializerMessagePack, deserializerYAML]
ser_results = []
deser_results = []
list_of_functionnames = ['Pickle', 'JSON', 'XML', 'MessagePack', 'YAML']


# Calculating the times of serializations
i = 0
for function in list_of_ser_functions:
	ser_results.append(timecalculator(function))
	i += 1


# Calculating the times of deserializations
i = 0
for function in list_of_deser_functions:
	deser_results.append(timecalculator(function))
	i += 1


# Defining file names to pass to loop.
list_of_filenames = ['serialized.pickle', 'serialized.json', 'serialized.xml', 'serialized.msgpack', 'serialized.yaml']
file_sizes = []
# Loop through different formats of files and check the sizes
for files in list_of_filenames:
	file_sizes.append(os.stat(files).st_size)

# Defining size for the figure, 16x8 inches
plt.figure(figsize=(16,8))
# Defining x-axis values
left = [1,2,3,4,5]

# Plot properties for serialization times
plt.subplot(131)
plt.bar(left, ser_results, tick_label = list_of_functionnames, width = 0.8, color = 'red')
plt.xlabel('Format')
plt.ylabel('Time')
plt.title('Serialization times per format')

# Plot properties for deserialization times
plt.subplot(132)
plt.bar(left, deser_results, tick_label = list_of_functionnames, width = 0.8, color = 'blue')
plt.xlabel ('Format')
plt.ylabel('Time')
plt.title('Deserialization times per format')

# Plot properties for file sizes
plt.subplot(133)
plt.bar(left, file_sizes, tick_label = list_of_functionnames, width = 0.8, color = 'green')
plt.xlabel('Format')
plt.ylabel('Size')
plt.title('Serialized file sizes per format')

# Draw the graph
plt.show()


