import random
import sqlite3

def addReviews(start, num, idArray):
	length=len(idArray)
	connection = sqlite3.connect('data.db')	
	cursor = connection.cursor()
	list=[]
	for i in range(0, num):
		food_id = idArray[random.randrange(0, length,1)]
		print (food_id)
		rating = random.randrange(1, 10)+float(random.randrange(0,2))/2
		tuple = (food_id, start, rating, '', 'Anonymous')
		print (tuple)
		list.append(tuple)
		start+=1

	values= ', '.join(map(str,list))
	query = 'INSERT INTO Ratings VALUES {}'.format(values)
	cursor.execute(query)
	connection.commit()
	connection.close()
	return start
	
	
	
def main():


	connection = sqlite3.connect('data.db')
	cursor = connection.cursor()

	query = 'Select ID From FOOD'
	result=cursor.execute(query)
	idArray=[]
	for row in result:
		idArray.append(row[0])
	
	connection.commit()
	connection.close()
	
	start = 0 
	addReviews(start,500,idArray)	
	
main()