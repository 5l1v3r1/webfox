#!/usr/bin/python3

import socket, threading
import optparse
import requests
import os
import time
from time import gmtime, strftime

a = """

██╗    ██╗███████╗██████╗ ███████╗ ██████╗ ██╗  ██╗
██║    ██║██╔════╝██╔══██╗██╔════╝██╔═══██╗╚██╗██╔╝
██║ █╗ ██║█████╗  ██████╔╝█████╗  ██║   ██║ ╚███╔╝ 
██║███╗██║██╔══╝  ██╔══██╗██╔══╝  ██║   ██║ ██╔██╗ 
╚███╔███╔╝███████╗██████╔╝██║     ╚██████╔╝██╔╝ ██╗
 ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝                                                 
"""
print(a)
print("*****************************************************")
print("Version: 1.2\nContact: bilgi@sercanyilmaz.com.tr")
print("*****************************************************")
time.sleep(3)

def user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t", "--target", dest="target_address", help= "Enter domain")
    options = parse_object.parse_args()[0]
    
    if not options.target_address:
        print("-i, you must enter your target IP")
    
    return options
    

host_info = user_input()
target = host_info.target_address

#ColorsPalet
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

urlfile = open("common_urllist.txt")
u = urlfile.read()
hiddenurls = u.splitlines()



def find_hiddenurls(target):
    print(WARNING + "\n[!] Hidden Directory Scanner Started!" + ENDC)
    for hiddenurl in hiddenurls:
        h_url = f"http://{target}/{hiddenurl}"
        try:
            rr = requests.get(h_url)

        except requests.ConnectionError:
            pass
        else:
            if str(rr.status_code) == "200":
                print(OKGREEN + "\n[+] Discovered url:", h_url + ENDC)


subfile = open("subdomains.txt")
su = subfile.read()
subdomains = su.splitlines()

def find_subdomains(target):
    print(WARNING + "\n[!] Subdomain Scanner Started!" + ENDC)
    for subdomain in subdomains:
        url = f"http://{subdomain}.{target}"
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print(OKGREEN + "\n[+] Discovered subdomain:", url + ENDC)
            

def TCP_connect(target, port_number, delay, output):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        TCPsock.connect((target, port_number))
        output[port_number] = 'is open'
    except:
        output[port_number] = ''


def scan_ports(target, delay):
    print(WARNING + "\n[!] Port Scanner Started!\n" + ENDC)

    threads = []
    output = {}

    for i in range(10000):
        t = threading.Thread(target=TCP_connect, args=(target, i, delay, output))
        threads.append(t)

    for i in range(10000):
        threads[i].start()

    for i in range(10000):
        threads[i].join()

    for i in range(10000):
        if output[i] == 'is open':
            print(OKGREEN + "[+] Port "+ str(i) + " is open" + ENDC)

def scan_common_vulns(target):
    try:
        print(WARNING+"\n[!] Scanning known common vulnerabilities for: " + str(target)+"\n"+ENDC)
        print(WARNING+"Warning! It can take a moment.\n"+ENDC)
        time.sleep(1)
        command = ("nmap -Pn --script vuln " + target)
        process = os.popen(command)
        results = str(process.read())
        logs = "logs/nmap_vulns" + strftime("%Y-%m-%d_%H:%M:%S", gmtime())
        print(OKGREEN + results + logs + ENDC)
    except KeyboardInterrupt:
        print(FAIL + "\n[!] Stopped by user interruption" + ENDC)
        time.sleep(1)



def main():
    host_ip = target
    delay = int(5)   
    scan_ports(host_ip, delay)

if __name__ == "__main__":
    main()

scan_common_vulns(target)
find_hiddenurls(target)
find_subdomains(target)
