import urllib  as urllib2
import json
import sqlite3

def check(name,x,y):
	try:
		key = name[x][y]
	except KeyError:
		# Key is not present
		key = " "
		pass
	return key
	
def checks(name,x):
	try:
		key = name[x]
	except KeyError:
		# Key is not present
		key = " "
		pass
	return key

	
	

def Load(number):
	url = 'https://api.nal.usda.gov/ndb/V2/reports?ndbno={}&type=f&format=json&api_key=MtlqoEXPRApbdd2EMbOieweSnv7WfhfCxFhFLPSw'.format(number)
	json_obj = urllib2.urlopen(url)

	str_response = json_obj.read().decode('utf8')

	#this is a dictionary
	data = json.loads(str_response)

	cursor = connection.cursor()
	query = 'INSERT INTO Food VALUES (?,?,?,?,?,?,?,?,?,?)'
	tuple = (data['foods'][0]['food']['desc']['ndbno'],data['foods'][0]['food']['desc']['name'], check(data['foods'][0]['food'],'ing','desc'),\
	check(data['foods'][0]['food'],'desc','sd'),check(data['foods'][0]['food'],'desc','sn'),check(data['foods'][0]['food'],'desc','cn'),check(data['foods'][0]['food'],'ing','upd'),\
	check(data['foods'][0]['food'],'desc','ds'),check(data['foods'][0]['food'],'desc','fg'),check(data['foods'][0]['food'],'desc','manu'))
	cursor.execute(query,tuple)
	
	water = 0
	energy = 0
	protein = 0
	lipidfat = 0
	carb = 0
	fiber = 0
	sugar = 0
	lactose = 0
	calcium = 0
	iron = 0
	potas = 0
	sodium = 0
	zinc = 0
	vitc = 0
	vitb12 = 0
	vitd = 0
	chol = 0
	
	for x in (data['foods'][0]['food']['nutrients']):
		temp = checks(x,'nutrient_id')
		if int(temp) == 255:
			water = x['value']
		if int(temp) == 208:
			energy = x['value']
		if int(temp) == 203:
			protein = x['value']
		if int(temp) == 204:
			lipidfat = x['value']
		if int(temp) == 205:
			carb = x['value']
		if int(temp) == 291:
			fiber = x['value']
		if int(temp) == 269:
			sugar = x['value']
		if int(temp) == 213:
			lactose = x['value']
		if int(temp) == 301:
			calcium = x['value']
		if int(temp) == 303:
			iron = x['value']
		if int(temp) == 306:
			potas = x['value']
		if int(temp) == 307:
			sodium = x['value']
		if int(temp) == 309:
			zinc = x['value']
		if int(temp) == 401:
			vitc = x['value']
		if int(temp) == 418:
			vitb12 = x['value']
		if int(temp) == 324:
			vitd = x['value']
		if int(temp) == 601:
			chol = x['value']

		
	cursor = connection.cursor()
	tuple = (data['foods'][0]['food']['desc']['ndbno'], water, energy, protein, lipidfat, carb, fiber, sugar, lactose, calcium, iron, potas, sodium, zinc, vitc, vitb12, vitd, chol)
	query = 'INSERT INTO Nutrients VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
	cursor.execute(query,tuple)
	

	cursor = connection.cursor()
	tuple = (check(data['foods'][0]['food'],'desc','manu'), number)
	query = 'INSERT INTO Manufacturer VALUES (?,?)'
	cursor.execute(query,tuple)
		

connection = sqlite3.connect('data.db')	
for x in range(45001524 ,45327989 , 1200):
	try:
		Load(x)
	except:
		continue
for x in range(35001 ,35240 , 8):
	try:
		Load(x)
	except:
		continue

for x in range(42073 ,44265 , 11):
	try:
		Load(x)
	except:
		continue

for x in range(18000 ,18999 , 33):
	try:
		Load(x)
	except:
		continue
		
for x in range(13000,13999 , 33):
	try:
		Load(x)
	except:
		continue
		
for x in range(14000,14640 , 21):
	try:
		Load(x)
	except:
		continue
		
for x in range(20000,20657, 21):
	try:
		Load(x)
	except:
		continue
		
for x in range(21002,21611,20):
	try:
		Load(x)
	except:
		continue
	
for x in range(15001,15274,9):
	try:
		Load(x)
	except:
		continue
		
for x in range(17000,17464,15):
	try:
		Load(x)
	except:
		continue
		
for x in range(16001,16619,20):
	try:
		Load(x)
	except:
		continue
		
for x in range(22899,22999,3):
	try:
		Load(x)
	except:
		continue
		
for x in range(12001,12220,7):
	try:
		Load(x)
	except:
		continue
		
for x in range(10000,10999,33):
	try:
		Load(x)
	except:
		continue
		
for x in range(36000,36061,2):
	try:
		Load(x)
	except:
		continue

connection.commit()
connection.close()

