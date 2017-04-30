import json
from flask import request
from flask import Flask
from base64 import decodestring
from flask import jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)

def g_getDir(imageName):
	return "../inputImages/"+imageName+"/"


def dumpToJson(kps, filename):
	import json
	calcdKeypoints = []
	for kp in kps:
		tempObj = {}
		tempObj["x"] = int(kp[0])
		tempObj["y"] = int(kp[1])
		calcdKeypoints.append(tempObj)

	keyPoints = {}
	keyPoints['keypoints'] = calcdKeypoints
	output = {}
	output['output'] = keyPoints

	f = open(filename,'w+')
	f.write( json.dumps(output) )

def saveImageAndDataInternal(imageName, imageBase64Encoded, keypoints):
	import os

	dir = g_getDir(imageName)
	if not os.path.exists(dir):
		os.makedirs(dir)

	imageData = decodestring(imageBase64Encoded)
	with open(dir + imageName + ".jpg", "wb") as fh:
	    fh.write(imageData)

	jsonOutput = {
		"output": {
			"keypoints": keypoints
		}
	}
	with open(dir + "keypoints.json", "wb") as fh:
	    fh.write(json.dumps(jsonOutput))


def saveImageAndData(imageName, jsonData):
	imageBase64Encoded = jsonData['imageData']
	keypoints = jsonData['keypoints']
	saveImageAndDataInternal(imageName, imageBase64Encoded, keypoints)


def runTheApp(imageName1, imageName2):
	import commands
	commandStr = './app compareTwoImages '+ imageName1 + ' ' + imageName2
	print 'Running command: \t' + commandStr
	output = commands.getstatusoutput(commandStr)
	print 'Finished: \t\t' + commandStr

	return output[1]


@app.route('/runTestWithJsonData', methods=['GET', 'POST'])
def hello_world():

	#prep the data
	data = request.get_json(silent=True)

	imageName1 = "someName1"
	saveImageAndData(imageName1, data['image1'])
	imageName2 = "someName2"
	saveImageAndData(imageName2, data['image2'])

	#run the app with the data
	result = runTheApp(imageName1, imageName2)

	#read the results


	#send the results back
	return jsonify(result)



CORS(app)
app.run(host='0.0.0.0', port=80)
