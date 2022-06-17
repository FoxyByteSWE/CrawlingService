import os, subprocess

def killChromeDriverProcess():
    subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe'])


os.chdir('C:/Users/marco/Desktop/FoxyByte/Crawler')

processRetCode = None
while processRetCode != 0:
    process = subprocess.run(["python", "crawler.py"])
    processRetCode = process.returncode
    # i need a way to kill the last chromedriver instance opened before opening another one
    killChromeDriverProcess()




