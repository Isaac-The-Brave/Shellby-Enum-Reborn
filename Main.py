#!/bin/python3
import sublist3r
import httpx
import os
import nmap


banner = """
                                                                         bbbbbbbb
   SSSSSSSSSSSSSSS hhhhhhh                                lllllll lllllllb::::::b
 SS:::::::::::::::Sh:::::h                                l:::::l l:::::lb::::::b
S:::::SSSSSS::::::Sh:::::h                                l:::::l l:::::lb::::::b
S:::::S     SSSSSSSh:::::h                                l:::::l l:::::l b:::::b
S:::::S             h::::h hhhhh           eeeeeeeeeeee    l::::l  l::::l b:::::bbbbbbbbb yyyyyyy           yyyyyyy
S:::::S             h::::hh:::::hhh      ee::::::::::::ee  l::::l  l::::l b::::::::::::::bby:::::y         y:::::y
 S::::SSSS          h::::::::::::::hh   e::::::eeeee:::::eel::::l  l::::l b::::::::::::::::by:::::y       y:::::y
  SS::::::SSSSS     h:::::::hhh::::::h e::::::e     e:::::el::::l  l::::l b:::::bbbbb:::::::by:::::y     y:::::y
    SSS::::::::SS   h::::::h   h::::::he:::::::eeeee::::::el::::l  l::::l b:::::b    b::::::b y:::::y   y:::::y
       SSSSSS::::S  h:::::h     h:::::he:::::::::::::::::e l::::l  l::::l b:::::b     b:::::b  y:::::y y:::::y
            S:::::S h:::::h     h:::::he::::::eeeeeeeeeee  l::::l  l::::l b:::::b     b:::::b   y:::::y:::::y
            S:::::S h:::::h     h:::::he:::::::e           l::::l  l::::l b:::::b     b:::::b    y:::::::::y
SSSSSSS     S:::::S h:::::h     h:::::he::::::::e         l::::::ll::::::lb:::::bbbbbb::::::b     y:::::::y
S::::::SSSSSS:::::S h:::::h     h:::::h e::::::::eeeeeeee l::::::ll::::::lb::::::::::::::::b       y:::::y
S:::::::::::::::SS  h:::::h     h:::::h  ee:::::::::::::e l::::::ll::::::lb:::::::::::::::b       y:::::y
 SSSSSSSSSSSSSSS    hhhhhhh     hhhhhhh    eeeeeeeeeeeeee llllllllllllllllbbbbbbbbbbbbbbbb       y:::::y
                                                                                                y:::::y
                                                                                               y:::::y
                                                                                              y:::::y
                                                                                             y:::::y
                                                                                            yyyyyyy
"""


print(banner)
domain = input("Enter Domain or IP: ")
os.system('clear')
print(banner)
print("Enumerating Subdomains:"
subDomains = sublist3r.main(domain, 10, '{}_SubDomains.txt'.format(domain), ports=None, silent=False, verbose=False, enable_bruteforce=False, engines=None)
#read subdomains file line by line, do some cleaning and get it ready for further processing
myFile1 = open('{}_SubDomains.txt'.format(domain), 'w')
myFile1.write(domain)
myFile1.close()
myFile1 = open('{}_SubDomains.txt'.format(domain), 'r')
myFile2 = open('{}_SubDomains1.txt'.format(domain), 'w')

for line in myFile1:
    if not line.isspace():
       myFile2.write(line)

myFile1.close()
myFile2.close()
os.remove('{}_SubDomains.txt'.format(domain))
os.system('clear')


#Search for HTTPS or HTTP and save results if requests are successful
print(banner)
print("Testing Domain - {}".format(domain))
print("[]Finished Enumerating Subdomains")
print("Testing Subdomains for HTTP and HTTPS:")

subDomainsList = open('{}_SubDomains1.txt'.format(domain), 'r')
httpSubDomains = open('{}_httpSubDomains.txt'.format(domain), 'w')

for subDomain in subDomainsList:
    r = httpx.get('https://{}'.format(subDomain))
    f = httpx.get('http://{}'.format(subDomain))
    if r.status_code or f.status_code == 200:
      httpSubDomains.write('https://{}'.format(subDomain))
    else:
        print('{} Failed'.format(subDomain))

httpSubDomains.close()
subDomainsList.close()

os.remove('{}_SubDomains1.txt'.format(domain))
os.system('clear')


#WebCrawl httpSubDomains
print(banner)
print("Testing Domain - {}".format(domain))
print("[]Finished Enumerating Subdomains")
print("[]Finished Testing Subdomain availability")
print("Using GoSpider and Wayback Machine to Crawl for weblinks:")

httpSubDomains2 = open('{}_httpSubDomains.txt'.format(domain), 'r')

for httpDomain in httpSubDomains2:
 os.system("gospider -s {} -c 10 -d 5 --blacklist '.(jpg|jpeg|gif|css|tif|tiff|png|ttf|woff|woff2|ico|pdf|svg|txt)' >> {}_crawled.txt".format(httpDomain,domain))
 os.system("waybackpy --url {} --user-agent 'fockdju' --limit 5 --cdx >> {}_crawled.txt".format(httpDomain,domain))

httpSubDomains2.close()
os.system('clear')

#Find Possibly Vulnerable Links
print(banner)
print("Testing Domain - {}".format(domain))
print("[]Finished Enumerating Subdomains")
print("[]Finished Testing Subdomain availability")
print("[]Finished Crawling for weblinks")
print("Searching URL's for possibly vulnerable end-points:")

isExist = os.path.exists('VulnLinks')
if not isExist:
  os.makedirs('VulnLinks')

os.system("cat {}_crawled.txt | gf urls | grep '{}' | grep -v ']' | qsreplace -a | sort -u | gf xss >> VulnLinks/{}_xss_VulnLinks.txt".format(domain,domain,domain))
os.system("cat {}_crawled.txt | gf urls | grep '{}' | grep -v ']' | qsreplace -a | sort -u | gf sqli >> VulnLinks/{}_sqli_VulnLinks.txt".format(domain,domain,domain))

os.remove('{}_httpSubDomains.txt'.format(domain))
os.system("clear")

#Run Vulnerability Tests on Acquired Links
print(banner)
print("Testing Domain - {}".format(domain))
print("[]Finished Enumerating Subdomains")
print("[]Finished Testing Subdomain availability")
print("[]Finished Crawling for weblinks")
VulnCount = sum(1 for line in open('VulnLinks/{}_xss_VulnLinks.txt'.format(domain)))
print("[]Found {} Possible End Points".format(VulnCount))
print("Attempting to Exploit End Points with XSS")

isExist = os.path.exists('Results')
if not isExist:
  os.makedirs('Results')

os.system("cat VulnLinks/{}_xss_VulnLinks.txt | gf urls | grep -v ']' | sort -u | dalfox pipe --silence -o Results/{}_xss_results.txt".format(domain,domain))
os.system("clear")

#Fin
print(banner)
print("Tested Domain - {}".format(domain))
print("[]Finished Enumerating Subdomains")
print("[]Finished Testing Subdomain availability")
print("[]Finished Crawling for weblinks")
print("[]Found {} Possible End Points".format(VulnCount))
VulnCount2 = sum(1 for line in open('Results/{}_xss_results.txt'.format(domain)))
print("[]Successfully Tested end Points for XSS Vulnerabilities - Found {} Vulnerabilities".format(VulnCount2))
print("[]Scan Finished Successfuly")
