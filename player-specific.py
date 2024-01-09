from io import StringIO
from html.parser import HTMLParser
import bs4 as bs
import urllib.request
import json
# -*- coding: utf-8 -*-

def appendEntry(date, name, track, time, flap, glitch):
    timeArr = time.replace("\"","'").split("'")
    data = {"date": date, "name": name, "track": track, "m": int(timeArr[0]), "s": int(timeArr[1]), "ms": int(timeArr[2]), "flap": flap, "glitch": glitch}
    everything.append(data)

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
f.write("")
f.close()


url = input("Enter the URL of the profile: ")
source = urllib.request.urlopen(url).read()
soup = bs.BeautifulSoup(source,'lxml')
table = soup.find_all('table')
nosc=table[-3]
glitch=table[-5]
print(nosc, file=open("nosc.txt", "w", encoding='utf-8'))
print(glitch, file=open("glitch.txt", "w", encoding='utf-8')) 

everything = []




	
############################### Practical code ######################################## DO NOT TOUCH IT WORKS OK
name = input("Enter Name of the player: ")
f = open("nosc.txt", "r")
nosc = f.read()
x = nosc.split("\n")

for i in range(2):
 splicer = strip_tags(x[i+1])
 splice = splicer.split("\n")
 
 if i == 0:
   if "-" in splice[14]:
    appendEntry(splice[14], name, "Luigi Circuit", splice[8], False, False)
 if i == 1:
   if "-" in splice[6]: 
    appendEntry(splice[6], name, "Luigi Circuit", splice[1], True, False)

counter = 1

for i in range(62):
 splicer = strip_tags(x[i+3]) 
 splice = splicer.split("\n")
 counter+=1
 
 if (counter % 2) == 0:
  track = splice[0]
  if "-" in splice[7]: 
    appendEntry(splice[7], name, track, splice[1], False, False)
  
 else:
  if "-" in splice[6]:
    appendEntry(splice[6], name, track, splice[1], True, False)
 
g = open("glitch.txt", "r")
glitchtable = g.read()
y = glitchtable.split("\n")
gcounter = 1
 
for i in range(63):
 gsplicer = strip_tags(y[i+3]) 
 gsplice = gsplicer.split("\n")
 
 splicer = strip_tags(x[i+3]) 
 splice = splicer.split("\n")
 
 gcounter+=1
 
 if (gcounter % 2) == 0:
  track = gsplice[0]
  
  if gsplice[1] != splice[1]:
   if "-" in gsplice[7]: 
    appendEntry(gsplice[7], name, track, gsplice[1], False, True)
  
 else:
  if gsplice[1] != splice[1]:
   if "-" in gsplice[6]:
    appendEntry(gsplice[6], name, track, gsplice[1], True, True)

f = open("output.json", "w")
f.write(json.dumps(everything))
f.close()