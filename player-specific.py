from io import StringIO
from html.parser import HTMLParser
import bs4 as bs
import urllib.request
import json
# -*- coding: utf-8 -*-

def appendEntry(date, name, track, time, flap, glitch, video):
    timeArr = time.replace("\"","'").split("'")
    data = {"date": date, "name": name, "track": track, "m": int(timeArr[0]), "s": int(timeArr[1]), "ms": int(timeArr[2]), "flap": flap, "glitch": glitch, "video": video}
    times.append(data)

def findVideo(rowString):
  soup = bs.BeautifulSoup(rowString)
  for link in soup.findAll('a'):
    if("http//:" in str(link.get("href")) or "https://" in str(link.get("href"))):
      return link.get("href")

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d + "\n")
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

f = open("output.json", "w")
f.write("[")
f.close()

urlBase = "https://www.mariokart64.com/mkw/profile.php?pid="
for i in range (1118, 1119):
    url = urlBase + str(i)
    source = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(source,'lxml')
    table = soup.find_all('table')
    nosc=table[-3]
    glitch=table[-5]
    info=table[-7]
    print(nosc, file=open("nosc.txt", "w", encoding='utf-8'))
    print(glitch, file=open("glitch.txt", "w", encoding='utf-8')) 
    print(info, file=open("info.txt", "w", encoding='utf-8')) 

    profile = {}
    f = open("info.txt", "r")
    info = f.read()
    x = info.split("\n")

    splicer = strip_tags(x[1])
    splice = splicer.split("\n")
    if len(splice) < 3:
        continue
    name = splice[1]

    splicer = strip_tags(x[2])
    splice = splicer.split("\n")
    country = splice[1]

    splicer = strip_tags(x[3])
    splice = splicer.split("\n")
    town = splice[1]

    splicer = strip_tags(x[5])
    splice = splicer.split("\n")
    otherInfo = splice[1]
    if(otherInfo == "Unknown ("):
        otherInfo = "Unknown"

    splicer = strip_tags(x[6])
    splice = splicer.split("\n")
    proofStatus = splice[1]

    info = {"name": name, "country": country, "town": town, "otherInfo": otherInfo, "proofStatus": proofStatus}
    profile["info"] = info

    times = []
    ############################### Practical code ######################################## DO NOT TOUCH IT WORKS OK
    f = open("nosc.txt", "r")
    nosc = f.read()
    x = nosc.split("\n")

    for i in range(2):
        splicer = strip_tags(x[i+1])
        splice = splicer.split("\n")
        
        if i == 0:
            if(splice[8] == "NT"):
                continue

            if "-" in splice[13] and "/" in splice[12]:
                appendEntry(splice[13], name, "Luigi Circuit", splice[8], False, False, "")
            else:
                video = findVideo(x[i+1])
                appendEntry(splice[14], name, "Luigi Circuit", splice[8], False, False, video)
        if i == 1:
            if(splice[1] == "NT"):
                continue

            if "-" in splice[5] and "/" in splice[4]: 
                appendEntry(splice[5], name, "Luigi Circuit", splice[1], True, False, "")
            else:
                video = findVideo(x[i+1])
                appendEntry(splice[6], name, "Luigi Circuit", splice[1], True, False, video)

    counter = 1

    for i in range(62):
        splicer = strip_tags(x[i+3]) 
        splice = splicer.split("\n")
        counter+=1
        
        if (counter % 2) == 0:
            track = splice[0]
            if(splice[1] == "NT"):
                continue
            if "-" in splice[6] and "/" in splice[5]: 
                appendEntry(splice[6], name, track, splice[1], False, False, "")
            else:
                video = findVideo(x[i+3])
                appendEntry(splice[7], name, track, splice[1], False, False, video)
        else:
            if(splice[1] == "NT"):
                continue
            if "-" in splice[5] and "/" in splice[4]:
                appendEntry(splice[5], name, track, splice[1], True, False, "")
            else:
                video = findVideo(x[i+3])
                appendEntry(splice[6], name, track, splice[1], True, False, video)
        
        g = open("glitch.txt", "r")
        glitchtable = g.read()
        y = glitchtable.split("\n")
        gcounter = 1
    
    for i in range(62):
        gsplicer = strip_tags(y[i+3]) 
        gsplice = gsplicer.split("\n")
        
        splicer = strip_tags(x[i+3]) 
        splice = splicer.split("\n")
        
        gcounter+=1
        
        if (gcounter % 2) == 0:
            track = gsplice[0]
            if(gsplice[1] == "NT"):
                continue
            if gsplice[1] != splice[1]:
                if "-" in gsplice[6] and "/" in gsplice[5]: 
                    appendEntry(gsplice[6], name, track, gsplice[1], False, True, "")
                else:
                    video = findVideo(y[i+3])
                    appendEntry(gsplice[7], name, track, gsplice[1], False, True, video)
        else:
            if(gsplice[1] == "NT"):
                continue
            if gsplice[1] != splice[1]:
                if "-" in gsplice[5] and "/" in gsplice[4]:
                    appendEntry(gsplice[5], name, track, gsplice[1], True, True, "")
                else:
                    video = findVideo(y[i+3])
                    appendEntry(gsplice[6], name, track, gsplice[1], True, True, video)

    profile["times"] = times

    f = open("output.json", "a")
    if(name != "Alex Penev"):
        f.write(", ")
    f.write(json.dumps(profile))
    f.close()

f = open("output.json", "a")
f.write("]")
f.close()