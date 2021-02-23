from io import StringIO
from html.parser import HTMLParser
import bs4 as bs
import urllib.request
import lxml
# -*- coding: utf-8 -*-

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
	
f = open("output.txt", "w")
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




	
############################### Practical code ######################################## DO NOT TOUCH IT WORKS OK
name = input("Enter Name of the player: ")
f = open("nosc.txt", "r")
nosc = f.read()
x = nosc.split("\n")

for i in range(2):
 splicer = strip_tags(x[i+1])
 splice = splicer.split("\n")
 
 if i == 0:
   if "-" in splice[13]:
    print("Date: " + splice[13] + "\nName: " + name + "\n\n" + 'Luigi Circuit nosc: ' + splice[8] + " ", file=open("output.txt", "a"))
    print(" ", file=open("output.txt", "a"))
	
 if i == 1:
   if "-" in splice[5]: 
    print("Date: " + splice[5] + "\nName: " + name + "\n\n" + "Luigi Circuit nosc flap: " + splice[1] + " ", file=open("output.txt", "a"))
    print(" ", file=open("output.txt", "a"))

counter = 1

for i in range(62):
 splicer = strip_tags(x[i+3]) 
 splice = splicer.split("\n")
 counter+=1
 
 if (counter % 2) == 0:
  track = splice[0]
  if "-" in splice[6]: 
   print("\nDate: " + splice[6] + "\nName: " + name + "\n\n" + track + " nosc: " + splice[1] + " ", file=open("output.txt", "a"))
   print(" ", file=open("output.txt", "a"))
  
 else:
  if "-" in splice[5]:
   print("\nDate: " + splice[5] + "\nName: " + name + "\n\n" + track + " nosc flap: " + splice[1] + " ", file=open("output.txt", "a"))
   print(" ", file=open("output.txt", "a"))
 
g = open("glitch.txt", "r")
glitchtable = g.read()
y = glitchtable.split("\n")

print("\n\nGlitch times:\n", file=open("output.txt", "a")) 
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
   if "-" in gsplice[6]: 
    print("\nDate: " + gsplice[6] + "\nName: " + name + "\n\n" + track + " g: " + gsplice[1] + " ", file=open("output.txt", "a"))
    print(" ", file=open("output.txt", "a"))
  
 else:
  if gsplice[1] != splice[1]:
   if "-" in gsplice[5]:
    print("\nDate: " + gsplice[5] + "\nName: " + name + "\n\n" + track + " g flap: " + gsplice[1] + " ", file=open("output.txt", "a"))
    print(" ", file=open("output.txt", "a"))

f.close()