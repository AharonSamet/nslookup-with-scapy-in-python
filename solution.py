"""
Aharon Samet

Objective: Build a server
commands:
1 - Enter a domain and print your IP (for example www.facbook.com)
2 - Enter IP and print domain (for example 157.240.20.15)
0 - to exit
"""
from django.contrib.gis import ptr
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP

print("Welcome to DNS server \n1: (Revers) or 2: (Mapping) 0: (exit)")
choice = '1'
try:
    while choice != '0':
        choice = input("Enter your choice\n")
        if choice == '1':
            try:
                domain = input("Enter the domain you want to lookup\n")
                dns_packet = IP(dst='8.8.8.8') / UDP(sport=12345, dport=53) / DNS(qdcount=1, rd=1) / DNSQR(qtype='A', qname=domain)
                response = sr1(dns_packet, verbose=0)
                temp = response[DNSRR]
                a_type = response[DNSRR].type
                i = 0
                while True:
                    if a_type == 1:
                        print(temp[DNSRR][i].rdata)
                        break
                    else:
                        i += 1
                        a_type = temp[DNSRR][i].type
                        if i == 20:
                            break
            except Exception as err:
                print(err)
        elif choice == '2':
            try:
                domain = input("Enter the domain you want to lookup\n")
                temp = domain.split('.')
                domain = temp[3] + '.' + temp[2] + '.' + temp[1] + '.' + temp[0]
                dns_packet = IP(dst='8.8.8.8') / UDP(sport=12345, dport=53) / DNS(qdcount=1, rd=1) / DNSQR(qtype='PTR', qname=(domain + '.in-addr.arpa'))
                response = sr1(dns_packet, verbose=0)
                ptr_type = response[DNSRR].type
                i = 0
                while True:
                    if ptr_type == 12:
                        print(response[DNSRR][i].rdata.decode())
                        break
                    else:
                        i += 1
                        a_type = response[DNSRR][i].type
            except Exception as err:
                print(err)
        elif choice == '0':
            print("Thank you for using our server")
            break
except Exception as err:
    print(err)

