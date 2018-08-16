import requests

def UploadNginx(url, fileName, filePath, storagePath):
	files = {"file1": (fileName, open(filePath, 'rb'), "multipart/form-data")}

	data = {"custom_path": storagePath}
	session = requests.post(url=url, data=data, files=files)
	return session.text