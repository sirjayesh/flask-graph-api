from flask import Flask,request,make_response
from utils import *
from flask_jsonpify import jsonify
import os,io

from flask_cors import CORS, cross_origin

app = Flask(__name__)
 
@app.route('/checkuser')
def checkUser():
	ntAccount = request.headers.get('ntaccount')
	dlName = request.headers.get('dlname')
	if ntAccount == None or dlName == None:
		return jsonify({"Error":"NT Account and/or Distribution List not set."})
	else:
		ntAccount = ntAccount.lower()
		dlName = dlName.lower()

	tokenHeader = getTokenHeader()	
	
	userID = getUserID(ntAccount,tokenHeader)
	if userID is not None:
	    status = checkUserPresent(userID,dlName,tokenHeader)
	    return jsonify(status)
	else:
		return jsonify({"Error":"Invalid NT Account"})

@app.route('/getusergroups')
def getGroups():
	ntAccount = request.headers.get('ntaccount')
	if ntAccount == None:
		return jsonify({"Error":"NT Account not set."})
	else:
		ntAccount = ntAccount.lower()
		
	tokenHeader = getTokenHeader()	
	userID = getUserID(ntAccount,tokenHeader)
	if userID is not None:
	    listGroups = getUserGroups(userID,tokenHeader)
	    listGroups.sort()
	    countResults = {}
	    countResults["Count"]=len(listGroups)
	
	    grpResults = [dict(name=grp) for grp in listGroups]
	    return  json.dumps([countResults,grpResults])
	else:
		return jsonify({"Error":"Invalid NT Account."})


@app.route('/getuserdata')
def getUserData():
	ntAccount = request.headers.get('ntaccount')
	if ntAccount == None:
		return jsonify({"Error":"NT Account not set."})
	else:
		ntAccount = ntAccount.lower()

	tokenHeader = getTokenHeader()	
	
	userData = getUserDetails(ntAccount,tokenHeader)
	return jsonify(userData)



@app.route('/image/<ntAccount>')
def getImage(ntAccount):
	if ntAccount == None:
		return jsonify({"Error":"NT Account not set."})
	else:
		ntAccount = ntAccount.lower()
	tokenHeader = getTokenHeader()	
	img = getProfilePicture(ntAccount,tokenHeader)	
	response = make_response(img.content)
	response.headers.set('Content-Type', 'image/jpeg')
	return response

@app.route('/getemployeehierarchy')
def getDirectReports():
	mgrNTAccount = request.headers.get('ntaccount')
	if mgrNTAccount == None:
		return jsonify({"Error":"NT Account not set."})
	else:
		mgrNTAccount = mgrNTAccount.lower()
		
	tokenHeader = getTokenHeader()	
	listEmployees = getDirectReportsManager(mgrNTAccount,tokenHeader)
	listEmployees.sort()
	
	return  jsonify(listEmployees)


@app.route('/search')
def searchFilter():
	searchTxt = request.headers.get('search')
	listEmployees=[]
	if searchTxt == None:
		return jsonify({"Error":"Enter Search Text"})
	else:
		searchTxt = searchTxt.lower()
	tokenHeader = getTokenHeader()	
	listEmployees = searchUsersDetailed(searchTxt,tokenHeader)
	listEmployees.sort()
	return  jsonify(listEmployees)	 


@cross_origin()
@app.route('/filter/<searchTxt>')
def searchUsersFilter(searchTxt):
	listEmployees=[]
	if searchTxt == None:
		return jsonify({"Error":"Enter Search Parameter"})
	else:
		searchTxt = searchTxt.lower()
	tokenHeader = getTokenHeader()	
	listEmployees = searchUsers(searchTxt,tokenHeader)
	listEmployees.sort()
	return  jsonify(listEmployees)	

if __name__ == "__main__":
    app.run()