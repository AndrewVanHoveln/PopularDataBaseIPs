## Python Script to get all ips used by the top 3 cloud service providers and seperate them by line into 
# respective text files. Each provider (Amazon, Microsoft, Goolgle) 
# has ipv4 and ipv6 addresses

## uploads the text files to GitHub

## Created by Andrew Van Hoveln


import requests
from bs4 import BeautifulSoup

# AWS IPV4 and 6 --------------------------------------------------------------

f = open('AWSIPV4.txt', 'w')
d = open('AWSIPV6.txt', 'w')

r = requests.get('https://ip-ranges.amazonaws.com/ip-ranges.json')

AWSdata = r.json()

ipv4AWSData = AWSdata['prefixes']

ipv6AWSData = AWSdata['ipv6_prefixes']


for i in range(len(ipv4AWSData)):
    f.write(ipv4AWSData[i]['ip_prefix'] + "\n")

for i in range(len(ipv6AWSData)):
    d.write(ipv6AWSData[i]['ipv6_prefix'] + "\n")




f.close()
d.close()


# AZURE IPV4 --------------------------------------------------------------

g = open('AzureIPV4.txt', 'w')

# request page
URL = "https://www.microsoft.com/en-us/download/confirmation.aspx?id=56519"
page = requests.get(URL)

# parse HTML to get the real link
soup = BeautifulSoup(page.content, "html.parser")
link = soup.find('a', {'data-bi-containername':'download retry'})['href']

# download
file_download = requests.get(link)

AzureData = file_download.json()

realAzureData = AzureData['values']

for i in range(len(realAzureData)):
    for j in range(len(realAzureData[i]['properties']['addressPrefixes'])):
        if ":" not in realAzureData[i]['properties']['addressPrefixes'][j]:
            g.write(realAzureData[i]['properties']['addressPrefixes'][j] + "\n")

g.close()


# AZURE IPV6 --------------------------------------------------------------

h = open('AzureIPV6.txt', 'w')

for i in range(len(realAzureData)):
    for j in range(len(realAzureData[i]['properties']['addressPrefixes'])):
        if ":" in realAzureData[i]['properties']['addressPrefixes'][j]:
            h.write(realAzureData[i]['properties']['addressPrefixes'][j] + "\n")

h.close()

# Google IPV4 and 6 --------------------------------------------------------------

k = open('GoogleIPV4.txt', 'w')
p = open('GoogleIPV6.txt' , 'w')

l = requests.get('https://www.gstatic.com/ipranges/cloud.json')

Googledata = l.json()

realGoogleData = Googledata['prefixes']


for i in range(len(realGoogleData)):
    if 'ipv4Prefix' in realGoogleData[i]:
        k.write(realGoogleData[i]['ipv4Prefix'] + "\n")
    elif 'ipv6Prefix' in realGoogleData[i]:
        p.write(realGoogleData[i]['ipv6Prefix'] + "\n")
    
p.close()
k.close()

##### UPLOADS FILES TO GITHUB ######


## This part of the script only works with a non-empty repository
## So add a readme file or something

import glob
from github import Github

# gets all text files in current directory 
my_files = glob.glob('*.txt')

## github login
token = "YOUR TOKEN HERE"
g = Github(token)

# name of repository
TEXT_FILES = "NAME YOUR REPOSITORY HERE"
repo = g.get_user().get_repo(TEXT_FILES)

# look through all files in repo
all_files = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

# look through local text files
for i in range (len(my_files)):
    with open(my_files[i], 'r') as file:
        content = file.read()
    # Upload to github
    git_prefix = 'IP_Text/'
    git_file = git_prefix + my_files[i]
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", content, contents.sha, branch="master")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "committing files", content, branch="master")
        print(git_file + ' CREATED')


## deletes text files from local directory
import os

filesToDelete = glob.glob('*.txt')

print("Sucessfully uploaded " + str(filesToDelete) + " to GitHub")

for i in range(len(filesToDelete)):
    os.remove(filesToDelete[i])


