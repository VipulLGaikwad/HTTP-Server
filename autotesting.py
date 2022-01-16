import sys
import requests
import webbrowser
import socket
import subprocess


try:
	port = sys.argv[1]
except IndexError:
	print("PLEASE enter the port number in command line")
	sys.exit(1)

url = "http://127.0.0.1:" + port

#changes the file permissions
subprocess.call(['sh', './mode.sh'])

######################################################################################

#THIS IS THE TESTING FOR THE GET REQUEST
print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for GET response without filename for status code 200\n")
print("\033[0;37m")
#checking without filename
urlget1= url + "/"
response = requests.get(urlget1)
try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
	print("Text of the response: {}\n".format(response.text))
except:
	print("There is some error in the response\n")

######################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for GET response with filename for status code 200\n")
print("\033[0;37m")
#checking without filename
urlget2 = url + "/" + "home.html"
response = requests.get(urlget2)
try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
	print("Text of the response: {}\n".format(response.text))
except:
	print("There is some error in the response\n")

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for GET response for 404 status code\n")
print("\033[0;37m")
urlget3 = url + "/" + "random.html"
response = requests.get(urlget3)
try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
	print("Text of the response: {}\n".format(response.text))
except:
	print("There is some error in the response\n")

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for GET response for 403 status code\n")
print("\033[0;37m")
urlget4 = url + "/" + "delete2.txt"
response = requests.get(urlget4)
try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
	print("Text of the response: {}\n".format(response.text))
except:
	print("There is some error in the response\n")

#####################################################################################

#THIS IS THE TESTING FOR THE HEAD REQUEST
print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for HEAD response for status code 200 without filename\n")
print("\033[0;37m")
urlhead1 = url + "/"
response = requests.head(urlhead1)
try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
	# print("Text of the response: {}\n".format(response.text))
except:
	print("There is some error in the response\n")

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for HEAD response for status code 404\n")
print("\033[0;37m")
urlhead2 = url + "/random.html"
response = requests.head(urlhead2)
try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
	# print("Text of the response: {}\n".format(response.text))
except:
	print("There is some error in the response\n")

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for HEAD response for status code 403\n")
print("\033[0;37m")
urlhead3 = url + "/delete2.txt"
response = requests.head(urlhead3)
try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
except:
	print("There is some error in the response\n")
	
#####################################################################################

#here first make the delete.txt file in the local machine and then check 
print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for DELETE response for status code 200\n")
print("\033[0;37m")
urldelete1 = url + "/delete.txt"
response = requests.delete(urldelete1)
try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
	print("Text of the response: {}\n".format(response.text))
except:
	print("There is some error in the response\n")

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for DELETE response for status code 404\n")
print("\033[0;37m")
urldelete2 = url + "/random.txt"
response = requests.delete(urldelete2)
try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
	print("Text of the response: {}\n".format(response.text))
except:
	print("There is some error in the response\n")

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for PUT response for status code 200\n")
print("\033[0;37m")
urlput1 = url + "/putdata.txt"
response = requests.put(urlput1, data={'user_name':'vipul','email':'gaikwad@gmail.com'})

try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
except:
	print("There is some error in the response\n")

#####################################################################################

#here first delete the putdata2.txt from local machine and then check for the 201 status code
print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for PUT response for status code 201\n")
print("\033[0;37m")
urlput2 = url + "/putdata2.txt"
response = requests.put(urlput2, data={'user_name':'vipul','email':'gaikwad@gmail.com'})

try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
except:
	print("There is some error in the response\n")

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for 501 status code\n")
print("\033[0;37m")
response = requests.options(url)
try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
	print("Text of the response: {}\n".format(response.text))
except:
	print("There is some error in the response\n")

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for POST response for application/x-www-form-urlencoded\n")
print("\033[0;37m")
response = requests.post(url, data={'user_name':'geetesh1','email':'geet1@gmail.com'})

try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
	print("Text of the response: {}\n".format(response.text))
except:
	print("There is some error in the response\n")

print("---------------------------------------------------------------------")
print("Testing for the POST response for multipart/form-data\n")

#####################################################################################

#testing for the if-modified-since header
#GET request is being sent
print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for GET requests if modified since header\n")
print("GET request with 200 status code and with body\n")
print("\033[0;37m")
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('127.0.0.1',int(port)))
data = ""
data += "GET /index.html HTTP/1.1\r\n"
data += f"Host: 127.0.0.1:{port}\r\n"
data += "Content-Type: text/html\r\nUser-Agent: Mozilla\r\nAccept-Language: en-US\r\nIf-Modified-Since: Sun, 20 Dec 2020 19:00:00\r\n\r\n"
clientSocket.send(data.encode())
modifiedSentence = clientSocket.recv(10000)
clientSocket.close()
print(modifiedSentence.decode())

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for GET requests if modified since header\n")
print("GET request with 304 status code and without body\n")
print("\033[0;37m")
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('127.0.0.1',int(port)))
data = ""
data += "GET /index.html HTTP/1.1\r\n"
data += f"Host: 127.0.0.1:{port}\r\n"
data += "Content-Type: text/html\r\nUser-Agent: Mozilla\r\nAccept-Language: en-US\r\nIf-Modified-Since: Sun, 13 Nov 2021 20:00:00\r\n\r\n"
clientSocket.send(data.encode())
modifiedSentence = clientSocket.recv(10000)
clientSocket.close()
print(modifiedSentence.decode())

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for HEAD requests if modified since header\n")
print("HEAD request with 200 status code\n")
print("\033[0;37m")
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('127.0.0.1',int(port)))
data = ""
data += "HEAD /index.html HTTP/1.1\r\n"
data += f"Host: 127.0.0.1:{port}\r\n"
data += "Content-Type: text/html\r\nUser-Agent: Mozilla\r\nAccept-Language: en-US\r\nIf-Modified-Since: Sun, 12 Nov 2020 20:00:00\r\n\r\n"
clientSocket.send(data.encode())
modifiedSentence = clientSocket.recv(10000)
clientSocket.close()
print(modifiedSentence.decode())

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for HEAD requests if modified since header\n")
print("HEAD request with 304 status code\n")
print("\033[0;37m")
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('127.0.0.1',int(port)))
data = ""
data += "HEAD /index.html HTTP/1.1\r\n"
data += f"Host: 127.0.0.1:{port}\r\n"
data += "Content-Type: text/html\r\nUser-Agent: Mozilla\r\nAccept-Language: en-US\r\nIf-Modified-Since: Sun, 13 Nov 2021 20:00:00\r\n\r\n"
clientSocket.send(data.encode())
modifiedSentence = clientSocket.recv(10000)
clientSocket.close()
print(modifiedSentence.decode())

#####################################################################################

print("---------------------------------------------------------------------")
print("\033[0;31m")
print("This is the testing for 414 status code\n")
print("\033[0;37m")
url += "/qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjaaaaaaaaaaaaaaaaaakkkkkkkkkkkkjjjjjjjjjjjjjjjjjjjaaaaaaaaaaaaaaaaaajjjjjjjjjjjjjjjjjjjjj"

response = requests.get(url)
try:
	print("Status code of response: {}\n".format(response.status_code))
	print("Headers of response: {}\n".format(response.headers))
	print("Text of the response: {}\n".format(response.text))
except:
	print("There is some error in the response\n")

#####################################################################################


webbrowser.open_new_tab('upload.html')
