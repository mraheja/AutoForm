import time
import random
import requests





lol = open("config.txt",'r')

data = []
options = []

ind = -1
for e in lol:
	e = e.replace("\n","")
	if(len(e) == 0):
		continue
	
	if("URL" in e):
		URL = e.replace("URL = ","").strip()
	elif("RESPONSES" in e):
		RESPONSES = int(e.replace("RESPONSES = ","").strip())
	elif("TIME" in e):
		TIME = int(e.replace("TIME = ","").strip())
	elif("NUM QUESTIONS" in e):
		numQuestions = int(e.replace("NUM QUESTIONS = ","").strip())
		for i in range(numQuestions):
			data.append([])
	elif("Q" in e and ":" in e):
		ind += 1
		options.append(e[e.index(":")::].strip())
	else:
		data[ind].append(e.replace(" ","+"))
		option = options[-1] #not used yet

	

read = requests.get(URL)


elems = []


print("Finding Elements")

tot = ""
for f in read:
	tot += str(f)
	
x = 0
while("entry" in tot[(x+1)::]):
	x = tot.index("entry",x+1)
	elems.append(tot[x:tot.index('"',x)].replace("'b'",""))
		
print("Found Elements")

assert len(elems) == numQuestions

URLn = URL
URLn = URLn.replace("viewform","formResponse")

URLn += "?"


def makeURL():
	URLt = URLn
	for i in range(0,len(elems)):
		URLt += elems[i]
		URLt += "="
		URLt += ans[i]
		URLt += "&"

	return URLt

def makeAns(respNum):
	ans = []
	for i in range(numQuestions):
		if("SEQUENCE" in options[i]):
			ans.append(data[i][respNum%len(data[i])])
		else:
			randInd = random.randint(0,len(data[i])-1)
			ans.append(data[i][randInd])
	
	return ans
			
			

times = []
times.append(0)

for i in range(RESPONSES):
	times.append(random.randint(1,TIME * 60))
	
times = sorted(times)

print(times)

for i in range(RESPONSES):
	ans = makeAns(i)
	URLt = makeURL()
	print("Submitting Response " + str(i+1))
	requests.get(URLt)
	time.sleep(times[i+1]-times[i])



