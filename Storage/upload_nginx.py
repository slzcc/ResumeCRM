import requests
import socket
import re

def getIP(domain):
	myaddr = socket.getaddrinfo(domain, 'http')
	return myaddr[0][4][0]

def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False

def UploadNginx(url, fileName, filePath, storagePath):

	domain = url.split("/")[2].split(":")[0]
	domain_ip = ""
	if not isIP(domain):
		domain_ip = getIP(domain)
		url = url.replace(domain, domain_ip)

	files = {"file1": (fileName, open(filePath, 'rb'), "multipart/form-data")}
	data = {"custom_path": storagePath}
	session = requests.post(url=url, data=data, files=files)
	return session.text