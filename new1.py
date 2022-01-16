import logging
import socket 
import sys
import threading
import os
import time
import mimetypes
import shutil
import random
from configparser import ConfigParser
import errno
import datetime
import string

#user input from command line
host = "127.0.0.1"
try:
	port = int(sys.argv[1])
except IndexError:
	print("PLEASE enter the port number in command line")
	sys.exit(1)


#socket formation and binding
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)
print("Server is ON", s.getsockname())


#status code and their reasons
reason = {200:"OK", 201:"Created", 304:"Not Modified", 403:"Forbidden", 404:"Not Found", 414:"URI Too Long", 501:"Not Implemented"}


#month conversion to numbers
mon = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4, 'May' : 5, 'Jun' : 6, 'Jul' : 7, 'Aug' : 8, 'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12 }


#detecting the file name
def filename_detector(request1):
	if request1[1].decode() == '/':
		filename = "index.html"
	else:
		filename = request1[1].decode().strip('/')
	return filename


#detecting the status code
def status_code_detector(filename):
	try: 	
		with open(filename,'rb') as file:
			status_code = 200
			dummy = file.read()
	except IOError as x:
		if x.errno == errno.ENOENT:
			status_code = 404
		elif x.errno == errno.EACCES:
			status_code = 403
		else:
			pass
	return status_code


#body formation for the response
def body_formation(filename,status_code):
	#response body formation
	if (status_code == 200):
		if filename == '/':
			with open('index.html','rb') as file:
				rb = file.read()
		else:
			with open(filename,'rb') as file:
				rb = file.read()
	elif (status_code == 404):
		with open('notfound.html','rb') as file:
			rb = file.read()
	elif (status_code == 501):
		with open('notimplemented.html','rb') as file:
			rb = file.read()
	elif (status_code == 403):
		with open('noreadpermission.html','rb') as file:
			rb = file.read()
	elif (status_code == 414):
		with open('urilong.html','rb') as file:
			rb = file.read()
	return rb



#formation of the headers for the response
def header_formation(status_code,request1,dt,filename):
	length = 0

	if (status_code == 200) or(status_code == 201) or (status_code == 304) or (status_code == 403) or (status_code == 404) or (status_code == 414) or (status_code == 501):
		r1_line = "HTTP/1.1 {} {}\r\n".format(status_code, reason[status_code])

	if (b'Accept-Encoding:' in request1):
		ind = request1.index(b'Accept-Encoding:')
		r1_line += request1[ind].decode() + request1[ind + 1].decode() + "\r\n"

	try:
		length = os.path.getsize(filename)
		r1_line += "Content-Length: {}\r\n".format(length) 
	except:
		pass

	try:
		r1_line += "Content-Type: " + mimetypes.guess_type(filename)[0] + "\r\n"
	except:
		r1_line += "Content-Type: " + "text/html\r\n"
	
	r1_line += "Date: " + dt + "\r\n"
		
	try:
		r1_line +="Last-Modified: " + lastmodified(filename) + "\r\n"
	except:
		pass

	r1_line += "Server: My Server\r\n"

	try:
		if not b'cookie' in request1:
			cookie = cookie_generator(request1)
			cookie = cookie + "\r\n"
			r1_line += "Set-Cookie: HttpSession=" + cookie
	except:
			try:
				ind2 = request1.index(b'Cookie:')
				r1_line += "Set-Cookie: " + request1[ind2 + 1].decode() + "\r\n"
				f = open(cookie_file_root, "r+")
				value = request1[ind2 + 1].decode().strip("HttpSession=")
				host1 = request1.index(b'Host:')
				host2 = request1[host1 + 1].decode()
				user1 = request1.index(b'User-Agent:')
				user2 = request1[user1 + 1].decode()
				value2 = host2 + "  " + user2 + "  " + value
				f.write(value2)
				f.write("\n")
				f.close()
			except:
				pass

	if (b'Connection:' in request1):
		ind = request1.index(b'Connection:')
		r1_line += request1[ind].decode() + request1[ind + 1].decode() + "\r\n"
	else:
		r1_line += "Connection: close\r\n"
	

	return r1_line


#last modified header function
def lastmodified(filename):
	try:
		epoch_time = os.path.getmtime(filename) #gives the epoch time
		current_time = time.ctime(epoch_time)
	except:
		current_time = time.ctime()

	arrange = current_time.split()
	arrange[0]+=","
	
	orderGMT="02143" #order in which the readable format has to be arranged to get standard internet format
	server_time=''
	
	for i in orderGMT:
		server_time = server_time + arrange[int(i)] + " "
	server_time+="GMT"

	return server_time


#if-modified-since header function
def ifmodifiedsince(filename,checkdate):
	try:
		epoch_time = os.path.getmtime(filename)
		current_time = time.ctime(epoch_time)
	except:
		current_time = time.ctime()
	
	ifheader = current_time.split()
	
	#this are for the file in the local machine 
	year = int(ifheader[4])
	month = mon[ifheader[1]]
	day = int(ifheader[2])
	rtime = ifheader[3].split(":")
	hour = int(rtime[0])
	mins = int(rtime[1])
	sec = int(rtime[2])
	current_server_time = datetime.datetime(year,month,day,hour,mins,sec)

	#this are for the required time
	checkdate = checkdate.split()
	year = int(checkdate[3])
	month = mon[checkdate[2]]
	day = int(checkdate[1])
	rtime = checkdate[4].split(":")
	hour = int(rtime[0])
	mins = int(rtime[1])
	sec = int(rtime[2])
	required_check_time = datetime.datetime(year,month,day,hour,mins,sec)

	if required_check_time < current_server_time:
		return True
	else:
		return False


#generates the cookies if not already present
def cookie_generator(request1):
	f = open(cookie_file_root, "r+")
	cookie = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 10))
	host1 = request1.index(b'Host:')
	host2 = request1[host1 + 1].decode()
	user1 = request1.index(b'User-Agent:')
	user2 = request1[user1 + 1].decode()
	cookie2 = host2 + "  " + user2 + "  " + cookie
	if not cookie in f.read():
		f.write(cookie2)
		f.write("\n")
		f.close()
	
	return cookie


#logging function
def logfunction(status_code,request1):
	var1 = request1[0].decode()
	var2 = request1[1].decode()
	var3 = request1[2].decode()
	line = " ".join([var1,var2,var3])

	if int(status_code/100) == 4 or int(status_code/100) ==5:#error conditions
		loginput2 = {'status': str(status_code),'ip_add': request1[4].decode(), 'user': request1[6].decode(),'request': line} 
		logger_input2 = logging.LoggerAdapter(logger2,loginput2)
		if status_code == 404:
			logger_input2.error('Not Found')
		elif status_code == 501:
			logger_input2.error('Method Not Implemented')
		elif status_code == 403:
			logger_input2.error('Forbidden')
		elif status_code == 414:	
			logger_input2.error('URI Too Long')

	elif int(status_code/100) == 1 or int(status_code/100) == 2 or int(status_code/100) == 3:
		loginput1 = {'status': str(status_code),'request': line,'ip_add': request1[4].decode(), 'user': request1[6].decode()}
		logger_input1 = logging.LoggerAdapter(logger1,loginput1)
		if status_code == 200:
			logger_input1.info('OK')
		elif status_code == 201:
			logger_input1.info('Created')
		elif status_code == 304:
			logger_input1.info('Not Modified')


#GET request
def GET_handler(request1,dt,request):
	
	filename = filename_detector(request1)
	
	if filename == 'favicon.ico':
		pass
	else:
		print(request)
		print("\n")

	if b'If-Modified-Since:' in request1:
		ind = request1.index(b'If-Modified-Since:')
		checkdate = request1[ind+1].decode() + " " + request1[ind+2].decode() + " " + request1[ind+3].decode() + " " + request1[ind+4].decode() + " " + request1[ind+5].decode()
		result = ifmodifiedsince(filename,checkdate)

		if result:
			status_code = 200
			r1_line = header_formation(status_code,request1,dt,filename)
			rb = body_formation(filename, status_code)
			b_line = b"\r\n"

			logfunction(status_code,request1)
			return b"".join([r1_line.encode(), b_line, rb])	
		else:
			status_code = 304
			r1_line = header_formation(status_code,request1,dt,filename)
			b_line = b"\r\n"
			logfunction(status_code,request1)
			return b"".join([r1_line.encode(), b_line])

	else:
		status_code = status_code_detector(filename)
		r1_line = header_formation(status_code,request1,dt,filename)

		rb = body_formation(filename, status_code)

		#blank line separator
		b_line = b"\r\n"

		logfunction(status_code,request1)
		return b"".join([r1_line.encode(), b_line, rb])
	

#POST request
def POST_handler(request1,dt,request):

	print(request)
	print("\n")

	try:
		status_code = 200
		ind = request1.index(b'Content-Type:')
		content_type = request1[ind + 1].decode()
	except:
		status_code = 404
		print("There is some error")
		
	if content_type == 'multipart/form-data;':
		
		try:
			file = open(post_file1_root, 'a')
			s = file.read()
			status_code = 200
		except IOError as x:
			if x.errno == errno.EACCES:
				status_code = 403
		if(status_code == 200):
			a = request1.index(b'multipart/form-data;') 
			boundary = request1[a+1].split(b"=")[1]
			form_data = request.split(boundary)[2:-1]
			file.write(dt + "\n")
			for entry in form_data:
				if b'Content-Type:' in entry:
					# Handle for file
					a = entry.index(b'\r\n\r\n')
					fname = entry[:a].split()[3].split(b'"')[1].decode()
					fdata = entry[a+4:]
					upload_file_path = uploads_file_path + fname
					try:
						f = open(upload_file_path, 'wb')
						f.write(fdata)
						f.close()
						rb = "<h1>successfully added your information</h1>".encode()
						status_code = 200
					except:
						rb = "<h1>There is some error</h1>".encode()
						status_code = 404
						
				else:
					temp_data = entry.decode().split()
					name = temp_data[2].split('"')[1] + ": "
					
					for i in range(3,len(temp_data) - 1):
						name += temp_data[i] + " "
		
					try:
						file.write(name + "\n")
					except:
						pass
		elif (status_code == 403):
			with open("noreadpermission.html",'rb') as f:
				rb = f.read()


	elif content_type == 'application/x-www-form-urlencoded':
		local = request1[-1].decode()
		local = local.split('&')
		try:
			file = open(post_file2_root,'a')
			s = file.read()
			status_code = 200
		except IOError as x:
			if x.errno == errno.EACCES:
				status_code = 403
			
		#dictionary for percent encoding 
		dict = {'%40':'@', '%2F':'/','%3F':'?','%23':'#', '%5B':'[', '%5D':']', "%3A":":", "%21":"!", "%24":"$", "%26":"&", "%27":"'", "%28":"(", "%29":")", "%2A":"*", "%2B":"+", "%2C":",", "%3B":";", "%3D":"=", "%25":"%", "%20":' '}	
		if status_code == 200:
			for i in range(0, len(local)):
				if '%' in local[i]:
					a = local[i].index('%')
					mid1 = local[i]
					mid2 = mid1[0 : a]
					mid3 = local[i]
					mid4 = mid3[a+3 : len(local[i])]
					mid5 = local[i]
					mid6 = mid5[a : a+3]
					final =  mid2 + dict[mid6] + mid4
					file.write(final + "\n")
				else:
					file.write(local[i] + "\n")
			
			rb = "<h1>successfully added your information</h1>".encode()		
			file.close()
		
		elif status_code == 403:
			with open("noreadpermission.html",'rb') as f:
				rb = f.read()
		
	else:
		pass
	
	if content_type == 'multipart/form-data;':
		r1_line = header_formation(status_code,request1,dt,post_file1_root)
	else:
		r1_line = header_formation(status_code,request1,dt,post_file2_root)
	
	b_line = b"\r\n"

	logfunction(status_code,request1)
	
	return b"".join([r1_line.encode(), b_line,rb])


#HEAD request
def HEAD_handler(request1,dt,request):
	
	filename = filename_detector(request1)

	if filename == 'favicon.ico':
		pass
	else:
		print(request)
		print("\n")


	if b'If-Modified-Since:' in request1:
		ind = request1.index(b'If-Modified-Since:')
		checkdate = request1[ind+1].decode() + " " + request1[ind+2].decode() + " " + request1[ind+3].decode() + " " + request1[ind+4].decode() + " " + request1[ind+5].decode()
		result = ifmodifiedsince(filename,checkdate)

		if result:
			status_code = 200
			r1_line = header_formation(status_code,request1,dt,filename)
			b_line = b"\r\n"

			logfunction(status_code,request1)
			return b"".join([r1_line.encode(), b_line])	
		else:
			status_code = 304
			r1_line = header_formation(status_code,request1,dt,filename)
			b_line = b"\r\n"
			
			logfunction(status_code,request1)
			return b"".join([r1_line.encode(), b_line])


	else:
		status_code = status_code_detector(filename)	

		r1_line = header_formation(status_code,request1,dt,filename)

		b_line = b"\r\n"

		logfunction(status_code,request1)
		return b"".join([r1_line.encode(), b_line])	

#DELETE request
def DELETE_handler(request1,dt,request):
	
	filename = filename_detector(request1)

	if filename == 'favicon.ico':
		pass
	else:
		print(request)
		print("\n")


	status_code = status_code_detector(filename)	

	r1_line = header_formation(status_code,request1,dt,filename)

	if (status_code == 200):
		if filename == '/':
			shutil.move('index.html',server_trash_root)
		else:
			shutil.move(filename,server_trash_root)
		message = '<h1>DELETED the file successfully!!!</h1>'
	elif (status_code == 404):
		message = '<h1>There is no such file to DELETE!!!</h1>'


	b_line = b"\r\n"

	logfunction(status_code,request1)
	return b"".join([r1_line.encode(),b_line,message.encode()])  	


#PUT request
def PUT_handler(request1,dt,request):
	filename = filename_detector(request1)

	if filename == 'favicon.ico':
		pass
	else:
		print(request)
		print("\n")


	try:
		with open(filename,'rb') as file:
			status_code = 200
	except FileNotFoundError:
		status_code = 201
	

	r1_line = header_formation(status_code,request1,dt,filename)
	local = request1[-1].decode()
	local = local.split('&')
	file = open(filename,'w')
	#dictionary for percent encoding 
	dict = {'%40':'@', '%2F':'/','%3F':'?','%23':'#', '%5B':'[', '%5D':']', "%3A":":", "%21":"!", "%24":"$", "%26":"&", "%27":"'", "%28":"(", "%29":")", "%2A":"*", "%2B":"+", "%2C":",", "%3B":";", "%3D":"=", "%25":"%", "%20":' '}	
	for i in range(0, len(local)):
		if '%' in local[i]:
			a = local[i].index('%')
			mid1 = local[i]
			mid2 = mid1[0 : a]
			mid3 = local[i]
			mid4 = mid3[a + 3:  len(local[i])]
			mid5 = local[i]
			mid6 = mid5[a:a+3]
			final =  mid2 + dict[mid6] + mid4
			file.write(final + "\n")
		else:
			file.write(local[i] + "\n")
		
	file.close()

	b_line = b"\r\n"
	
	logfunction(status_code,request1)
	return b"".join([r1_line.encode(),b_line])	


def OTHER_handler(request1,dt,request):
	
	print(request)
	print("\n")

	filename = 'notimplemented.html'
	status_code = 501	
	
	r1_line = header_formation(status_code,request1,dt,filename)
	rb = body_formation(filename,status_code)
	b_line = b"\r\n"
	
	logfunction(status_code,request1)
	return b"".join([r1_line.encode(), b_line, rb]) 


#funtion for the length detection of the request
def uri_length(uri):
    l = len(uri)
    if(l > int(length)):
        return True
    else:
        return False


#URI length handling
def URI_handler(request1,dt,request):
	print(request)
	print("\n")

	filename = 'urilong.html'
	status_code = 414	
	r1_line = header_formation(status_code,request1,dt,filename)
	rb = body_formation(filename,status_code)
	b_line = b"\r\n"
	logfunction(status_code,request1)
	return b"".join([r1_line.encode(), b_line, rb])


#all the requests pass through here
def request_handler(connsocket,addr):
	size = 8192

	#bytes request
	request = b""
	request = connsocket.recv(size)

	request1 = request.split()

	method = request1[0].decode()
	uri = request1[1].decode()

	dt = time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())

	if len(request) >= 0.90 * size:
		while True:
			buffer_size = connsocket.recv(size)
			request += buffer_size
			if len(buffer_size) <= size * 0.9:
				break


	methods = {"GET":GET_handler, "POST" :POST_handler, "PUT":PUT_handler, "HEAD":HEAD_handler,"DELETE":DELETE_handler}

	if (uri_length(uri)):
		server_response = URI_handler(request1,dt,request)
	elif method == 'GET' or method == 'POST' or method == 'PUT' or method == 'HEAD' or method == 'DELETE':
		server_response = methods[method](request1,dt,request)
	else:
		server_response = OTHER_handler(request1,dt,request)


	connsocket.sendall(server_response)
	connsocket.close()


#for stopping the server
def server_stop():
	while(True):
		command = input()
		if(command == 'stop'):
			print("HTTP server turning off !!!")
			os._exit(os.EX_OK)


quit = threading.Thread(target = server_stop)
quit.start()


#config file formation and reading
config = ConfigParser()
config.read("configfile.ini")
info = config["INFO"]
post = config["POST"]
log = config["LOGGING"]
clength = config["LENGTH"]


#path formation
cookie_file_root = info["cookie"]
server_trash_root = info["trash"]
post_file1_root = post["post1"]
post_file2_root = post["post2"]
logging_file1_path = log["access_logging"]
logging_file2_path = log["error_logging"]
uploads_file_path = post["upload"]
length = clength["length"]


#access file log
logger1 = logging.getLogger("ACCESS")
logger1.setLevel(logging.INFO)
handler1 = logging.FileHandler(logging_file1_path)
file1 = logging.Formatter('%(status)s  "%(request)s"  %(ip_add)s  %(asctime)s  %(user)s %(message)s')
handler1.setFormatter(file1)
logger1.addHandler(handler1)


#error file Log
logger2 = logging.getLogger("error")
logger2.setLevel(logging.ERROR)
handler2 = logging.FileHandler(logging_file2_path)
file2 = logging.Formatter('%(status)s  "%(request)s"  %(ip_add)s  %(asctime)s  %(user)s  %(message)s')
handler2.setFormatter(file2)
logger2.addHandler(handler2)


#request acceptance and threading
while True:
	connsocket, addr = s.accept()
	print("New connection received from : {} ".format(addr))
	th = threading.Thread(target = request_handler, args = (connsocket,addr))
	th.start()
