__author__ = ['[Paulo Hennig](https://github.com/pahennig/)']
# pip3 install google
# pip3 install requests

from googlesearch import search
import urllib.request
import requests
import sys
import time



# Declaring vars for future usage
storage=[]
checkingvul=[]
vuls=[]

# Getting URIs
def searchinggoogle():
    print("Avoid massive scan of more than 50 results. Otherwise, Google might block your session...\n\n")
    time.sleep(3)
    total = int(input("How many pages you wish to look for? "))
    dork = input("Google dork (e.g., inurl noticias.php?id= and site:starbucks.com)? ")
    Language = input("Language (e.g., pt-br)? ")
    try:
        for url in search(dork, lang=Language, stop=total):
                storage.append(url)
    except:
        print ("Google just blocked your access for a while...")
        sys.exit()

# Saving URIs to a list with '
def results():
    print ("\n[*] Search results'\n")
    for i in storage:
        print (i)
        checkingvul.append(i+"'")
    return storage,checkingvul

def comparing():
    print("\n[*] Parsing errors\n")
    y=0
    comparative = ['syntax', 'SQL', 'Row']
    httpcodes='403400401404503'
    try:
        while True:
            try:
                r = requests.head(checkingvul[y], timeout=8)
                s = str(r).lower()
                if s[-5:-2] in httpcodes:
                    print ("$ HTTP response error from ",checkingvul[y])
                else:
                    try:
                        opening=urllib.request.urlopen(checkingvul[y])
                        page=str(opening.read())
                        for i in comparative:
                            if i in page:
                                showing=checkingvul[y]
                                vuls.append(checkingvul[y])
                    except (urllib.error.HTTPError):
                        print ("$ Something went wrong with ",checkingvul[y])
                    except(requests.exceptions.Timeout):
                        print ("Timeout for: ",checkingvul[y])
                    except Exception:
                        print("*Exception at: ",checkingvul[y])
            except(requests.exceptions.Timeout):
                print ("Timeout for: ",checkingvul[y])
            except Exception:
                print("*Exception at: ",checkingvul[y])
            y+=1
    except (IndexError):
        pass
    return vuls

def printingvuls(vuls):
    vuls=comparing()
    print("\n[*] Checking SQL Injection vulnerabilities\n")
    vuls=set(vuls)
    for i in vuls:
        print ("Seems Vulnerable:",i)
    print ("\n[*] Goodbye")
    time.sleep(3)

def comparingproxied(vuls):
    proxyquestion=input("Type a proxy address using HTTP/HTTPS (e.g., http://63.150.152.151:8080) to use one or ignore this warning by pressing enter\nProxy: ")
    if proxyquestion[0:4] == 'http':
        proxyDict = {
              "http"  : proxyquestion,
              }
    elif proxyquestion[0:5] == 'https':
        proxyDict = {
              "https"  : proxyquestion,
              }
    elif proxyquestion == '':
        proxyDict = {
            }
    print("\n[*] Parsing errors\n")
    y=0
    comparative = ['syntax', 'SQL', 'Row']
    httpcodes='403400401404503'
    try:
        while True:
            try:
                r = requests.head(checkingvul[y],proxies=proxyDict, timeout=8)
                s = str(r).lower()
                if s[-5:-2] in httpcodes:
                    print ("$ HTTP response error from ",checkingvul[y])
                else:
                    try:
                        opening=requests.get(checkingvul[y],proxies=proxyDict)
                        page=str(opening.content)
                        for i in comparative:
                            if i in page:
                                showing=checkingvul[y]
                                vuls.append(checkingvul[y])
                    except (urllib.error.HTTPError):
                        print ("$ Something went wrong with ",checkingvul[y])
                    except(requests.exceptions.Timeout):
                        print ("Timeout for: ",checkingvul[y])
                    except Exception:
                        print("*Exception at: ",checkingvul[y])
            except(requests.exceptions.Timeout):
                print ("Timeout for: ",checkingvul[y])
            except Exception:
                print("*Exception at: ",checkingvul[y])
            y+=1
    except (IndexError):
        pass

if __name__ == "__main__":
    searchinggoogle()
    results()
    wishproxy=str(input("\n[*] Do you want to use a proxy to access and test the saved URLs (e.g., http://63.150.152.151:8080)[Y/n]: "))
    if wishproxy == 'y' or wishproxy == 'Y':
        comparingproxied(vuls)
    else:
        comparing()
    printingvuls(vuls)
