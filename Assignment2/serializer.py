""" Daniel Linna
	0509355
	28.2.2020 """
import pickle 
import json
import xml.etree.ElementTree as ET
import msgpack
import yaml


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
	}
}

def pickling():
	pickleFile = open("serialized.pickle","wb")
	pickle.dump(exampledata,pickleFile)
	pickleFile.close()

def unpickling():
	unpickleFile = open("serialized.pickle", "rb")
	new_data = pickle.load(unpickleFile)
	unpickleFile.close()

def serializerJSON():
	jsonFile = open("serialized.json", "w")
	json.dump(exampledata, jsonFile)
	jsonFile.close()

def deserializerJSON():
	jsonFile = open("serialized.json", "r")
	new_data = json.load(jsonFile)
	jsonFile.close()

def serializerXML():
	elem = ET.Element('SerializedData')
	for key, val in exampledata.items():
		child = ET.Element(key)
		for subkey, subval in val.items():
			grandchild = ET.SubElement(child,subkey)
			grandchild.text = str(subval)
		elem.append(child)

	xmlFile = open("serialized.xml", "w")
	xmlFile.write(ET.tostring(elem))
	xmlFile.close()

	
def deserializerXML():
	tree = ET.parse("serialized.xml")
	data = tree.getroot()


def serializerMessagePack():
	msgpackFile = open("serialized.msgpack", "w")
	msgpack.pack(exampledata, msgpackFile)
	msgpackFile.close()
	

def deserializerMessagePack():
	msgpackFile = open("serialized.msgpack", "r")
	data = msgpack.unpack(msgpackFile)
	msgpackFile.close()


def serializerYAML():
	yamlFile = open("serialized.yaml", "w")
	yaml.dump(exampledata, yamlFile)
	yamlFile.close()


def deserializerYAML():
	yamlFile = open("serialized.yaml", "r")
	data = yaml.load(yamlFile, Loader=yaml.FullLoader)
	yamlFile.close()


pickling()
unpickling()
serializerJSON()
deserializerJSON()
serializerXML()
deserializerXML()
serializerMessagePack()
deserializerMessagePack()
serializerYAML()
deserializerYAML()
