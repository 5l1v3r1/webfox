#!/usr/bin/python3

import socket, threading
import optparse
import requests
import time

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
print("Version: 1\nContact: bilgi@sercanyilmaz.com.tr")
print("*****************************************************")
time.sleep(3)

def user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i", "--ip", dest="ip_address", help= "Enter target IP")
    options = parse_object.parse_args()[0]
    
    if not options.ip_address:
        print("-i, you must enter your target IP")
    
    return options

host_info = user_input()
ip = host_info.ip_address

# ColorsPalet
OKGREEN = '\033[92m'
ENDC = '\033[0m'
BOLD = '\033[1m'
WARNING = '\033[93m'

urlfile = open("YOUR_FILE_PATH\common_urllist.txt")
u = urlfile.read()
hiddenurls = u.splitlines()

subfile = open("YOUR_FILE_PATH\subdomains.txt")
su = subfile.read()
subdomains = su.splitlines()

def find_hiddenurls(ip):
    print(WARNING + "\n[!] Hidden Directory Scanner Started!" + ENDC)
    for hiddenurl in hiddenurls:
        h_url = f"http://{ip}/{hiddenurl}"
        try:
            rr = requests.get(h_url)

        except requests.ConnectionError:
            pass
        else:
            if str(rr.status_code) == "200":
                print(OKGREEN + "\n[+] Discovered url:", h_url + ENDC)
                print (OKGREEN + h_url + "'s status code => "+ str(rr.status_code) + ENDC)

def find_subdomains(ip):
    print(WARNING + "\n[!] Subdomain Scanner Started!" + ENDC)
    for subdomain in subdomains:
        url = f"http://{subdomain}.{ip}"
        try:
            r = requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print(OKGREEN + "\n[+] Discovered subdomain:", url + ENDC)
            print (OKGREEN + url + "'s status code => "+ str(r.status_code) + ENDC)
            

def TCP_connect(ip, port_number, delay, output):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        TCPsock.connect((ip, port_number))
        output[port_number] = 'is open'
    except:
        output[port_number] = ''


def scan_ports(ip, delay):
    print(WARNING + "\n[!] Port Scanner Started!\n" + ENDC)

    threads = []
    output = {}

    for i in range(10000):
        t = threading.Thread(target=TCP_connect, args=(ip, i, delay, output))
        threads.append(t)

    for i in range(10000):
        threads[i].start()

    for i in range(10000):
        threads[i].join()

    for i in range(10000):
        if output[i] == 'is open':
            print(OKGREEN + "[+] Port "+ str(i) + " is open" + ENDC)

def main():
    host_ip = ip
    delay = int(5)   
    scan_ports(host_ip, delay)

if __name__ == "__main__":
    main()

find_subdomains(ip)
find_hiddenurls(ip)
