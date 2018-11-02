import requests,json
import config

domain = config.domain
organisation = config.organisation

def getTokenHeader():
	payload = {
	    'grant_type':'client_credentials',
	    'resource':config.resource_uri,
	    'client_id':config.client_id,
	    'client_secret':config.client_secret,
	}
	getTokenURL = config.authority_url+'/'+organisation+'.onmicrosoft.com/oauth2/token'
	tokenResponse = requests.post(getTokenURL,headers={ "content-Type":"application/x-www-form-urlencoded"},data=payload)
	token =  json.loads(tokenResponse.content)['access_token']
	headers = {
		'Content-Type':'application/json',
		'Authorization':"Bearer " + token
	}
	return headers

def getUserID(ntAccount,tokenHeader):
	version = config.api_version
	userIDResponse = requests.get('https://graph.microsoft.com/'+version+'/users/'+ntAccount+domain,headers=tokenHeader)
	data  = json.loads(userIDResponse.content) 
	try:
	    userID = data['id']
	    return userID
	except:
	    return None

def getPropertyValue(ntAccount,tokenHeader,property):
	version = config.api_version
	url  = 'https://graph.microsoft.com/'+version+'/users/'+ntAccount+domain+property
	print (url)
	userIDResponse = requests.get(url,headers=tokenHeader)
	data  = json.loads(userIDResponse.content) 
	try:
	    value = data['value']
	    return value
	except:
	    return None

	
def checkUserPresent(userID,dlName,tokenHeader):
	version = config.api_version
	flag = False	
	chechMemberOfURL = 'https://graph.microsoft.com/'+version+'/users/'+userID+'/memberOf'
	memberOfdata = requests.get(chechMemberOfURL,headers=tokenHeader)
	data = json.loads(memberOfdata.content)

	for group in data['value']:
		for k,v in group.items():
			if k == 'displayName' and v.lower() == dlName:
				flag = True
				break	
	if flag == True:
		return True
	else:
		return False
	
		
def getUserGroups(userID,tokenHeader):
    #Step 1 : Fetch group id and add them to a list
	version = config.api_version
	url1 = "https://graph.microsoft.com/"+version+"/users/"+userID+"/getMemberGroups"
	payload = {
		'securityEnabledOnly':'false'
    }
	groupIDdata = requests.post(url1,headers=tokenHeader,json=payload)
	data = json.loads(groupIDdata.content)
	groupIDs = data['value']

    #Step 2 : Pass the list (in Step 1 ) of group ids to fetch the group names
	url2 = "https://graph.microsoft.com/"+version+"/directoryObjects/getByIds"

	payload2 = {
        "ids": groupIDs
    }
	groupNamedata = requests.post(url2,headers=tokenHeader,json=payload2)
	dataNames = json.loads(groupNamedata.content)
	listMemberGroups = []
	for group in dataNames['value']:	
		for k,v in group.items():
			if k == 'displayName':
				v= v.encode("utf8")
				listMemberGroups.append(str(v))
	return listMemberGroups

		
def getUserDetails(ntAccount,tokenHeader):
    version = config.api_version
    response = requests.get('https://graph.microsoft.com/'+version+'/users/'+ntAccount+domain+'?$expand=manager',headers=tokenHeader)
    data  = json.loads(response.content) 
    userData = {}
    masterList = []
    lstReportees = []
    try:
        userData['emailID'] =  data['mail']
        userData['firstName'] =  data['givenName']
        userData['lastName'] =  data['surname']
        userData['mobile'] = data['mobilePhone']
        userData['loginAccount'] =  data['mailNickname']
        userData['uniqueName'] =  data['displayName']
        userData['userCode'] = data['employeeId']  if version == "beta" else ""
        userData['location'] = data['city'] + ',' + data['country']
        if joiningDate is not None:
            userData['joiningDate'] = joiningDate.split('|')[0]
        else:
            userData['joiningDate'] =  ""
        try:
            userData['manager'] = data['manager']['displayName']
            userData['managerMail'] = data['manager']['mail']
        except:
            userData['manager'] =  None
            userData['managerMail'] = None
        if userData['employeeCategory'] == 'Management':
            lstReportees = getDirectReportsManager(ntAccount,tokenHeader)
        masterList.append(userData)        
        masterList.append(lstReportees)        

    except:
        return "Invalid NT Account"
    return masterList


def getProfilePicture(ntAccount,tokenHeader):
    version = config.api_version
    url = "https://graph.microsoft.com/"+version+"/users/"+ntAccount+domain+"/photo/$value"
    img = requests.get(url,headers=tokenHeader)
    return img
 

def getDirectReportsManager(mgrNtAccount,tokenHeader):
    version = config.api_version
    url = "https://graph.microsoft.com/"+version+"/users/"+mgrNtAccount+domain+"/directReports"

    response = requests.get(url,headers=tokenHeader)
    lstEmployees  = json.loads(response.content) 
    employeeDetails = []

    lstKeys = lstEmployees.keys()

    if 'value' in lstKeys:
        for data in lstEmployees['value']:	
            try:
                userData = {}
                userData['NTAccount'] =  data['mailNickname']
                userData['FullName'] =  data['displayName']
                userData['EmpCode'] = data['employeeId']  if version == "beta" else ""
                employeeDetails.append(userData)
            except Exception as ex:
                print (ex)
                print (data)
         
    return employeeDetails

def searchUsers(searchText,tokenHeader):
    version = config.api_version

    url = "https://graph.microsoft.com/"+version+"/users?$filter=startswith(displayName,'"+searchText+"') or startswith(givenName,'"+searchText+"') or startswith(surname,'"+searchText+"') or startswith(mail,'"+searchText+"') or startswith(userPrincipalName,'"+searchText+"')"

    if version == "beta":
       url +=  " or startswith(employeeId,'"+searchText+"')"
    url += "&$select=displayName,mailNickname&$format=json"
    response = requests.get(url,headers=tokenHeader)
    lstEmployees  = json.loads(response.content) 

    lstNames = []
    for data in lstEmployees['value']:	
        try:
             dct = {}
             dct['Name'] = data['displayName']
             dct['NTAccount'] = data['mailNickname']
             lstNames.append(dct)
        except Exception as ex:
             print (ex)
             print (data)
    return lstNames

def searchUsersDetailed(searchText,tokenHeader):
    version = config.api_version

    url = "https://graph.microsoft.com/"+version+"/users?$filter=startswith(displayName,'"+searchText+"') or startswith(givenName,'"+searchText+"') or startswith(surname,'"+searchText+"') or startswith(mail,'"+searchText+"') or startswith(userPrincipalName,'"+searchText+"')"

    if version == "beta":
       url +=  " or startswith(employeeId,'"+searchText+"')"
    url += "&$expand=manager&$format=json"
    response = requests.get(url,headers=tokenHeader)
    lstEmployees  = json.loads(response.content) 
    employeeDetails=[]
    master = []
    for data in lstEmployees['value']:	
        try:
            userData = {}
            userData['emailID'] =  data['mail']
            userData['firstName'] =  data['givenName'].split(" ")[0] if data['givenName'].split(" ")[0] is not None else data['givenName']
            userData['lastName'] =  data['surname']
            userData['mobile'] = data['mobilePhone']
            userData['loginAccount'] =  data['mailNickname']
            userData['uniqueName'] =  data['displayName']
            userData['userCode'] = data['employeeId']  if version == "beta" else ""
            userData['location'] = data['city'] + ',' + data['country']
            userData['manager'] = data['manager']['displayName']
            userData['managerMail'] = data['manager']['mail']
            if userData not in employeeDetails:
                employeeDetails.append(userData)
        except Exception as ex:
             print (ex)
             print (data)
    master.append(employeeDetails)
    if len(employeeDetails) == 1 :
          print (employeeDetails[0]['loginAccount'])
          lstReportee = getDirectReportsManager(employeeDetails[0]['loginAccount'],tokenHeader)
          if len(lstReportee) > 0:
               print ("Has " + str(len(lstReportee)) + "reportees" )  
               master.append(lstReportee)
    return master
