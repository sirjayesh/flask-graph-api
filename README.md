# flask-graph-api
=====


A project to connect to your Microsoft Graph Explorer registered in Microsoft Azure AD. Register your app in azure portal and configure the details in config.py file.


======


Run the project using command

python app.py



A project to connect to your Microsoft Graph Explorer registered in Microsoft Azure AD. Register your app in azure portal and configure below variables in config.py file.

  - client_id : Enter your azure AD Graph app registration client ID
  - client_secret : Enter your azure AD Graph app registration client Secret
- resource_uri = 'https://graph.microsoft.com/'
- authority_url = 'https://login.microsoftonline.com'
- api_version = 'beta'  or 'v1'
- organisation = 'xyz' (Eg. microsoft or google or apple ,etc)
- domain = "@xyz.com"  (Eg. Your email domain Eg. @microsoft.com or @gmail.com or @apple.com, etc)

## End Points:

# /checkuser
    > Request Header variable names: 
    ntaccount and dlname

  - To check if user is present in the Distribution List. If exists, it will return True, else False.

