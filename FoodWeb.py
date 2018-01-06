from flask import Flask, render_template, redirect, jsonify, url_for, request, session
from flask_restful import Api
from flask_wtf import Form
from flask_wtf.csrf import CsrfProtect
from wtforms import SelectField, StringField
import sqlite3


# initalize server
#initializing our folders...we renamed our template_folder (Which holds our html files) from the default name flask gives it to views
app = Flask(__name__, template_folder = 'views', static_folder = 'public')
api = Api(app)
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
CsrfProtect(app)

@app.route('/', methods = ['GET', 'POST'])
def about():
	return render_template('About_Us.html')
	
# create connection object using wrapper class @app.route()
@app.route('/views', methods = ['GET', 'POST'])
def view():
	#creating a class which inherits from the Form class and helps us render our forms on the html
	class ViewSelectForm(Form):		
		#newarr is a list that has multiple tuples which store the (value, *name displayed on the dropdown*)
		newarr = [('MajorInfo', 'Major Information'), ('ProteinManu_Protein', 'Dense Protein Food Manufacturers'),('HeavyProtein_protein', 'Heavy Protein Food'),('FoodManufacturers', 'Food Manufacturers'),('HeavyProtein_LowCarb', 'Heavy Protein and Carbs Food'),('AverageRatings', 'Average Ratings'),('HighlyRated', 'Highly Rated Food'),('CommonNutrients', 'Common Nutrients'),('MostReviewed', 'Most Reviewed'),('RecentReviews', 'Recent Reviews')]
		#SelectField is a class so we're defining name as an object of the SelectField class which helps us create dropdowns in the html document
		name = SelectField(coerce=str, choices = newarr)
		
	#creating a form object which we can pass to the html file
	form = ViewSelectForm()
	#to debug possible errors
	print(form.errors)
	
	#view handles our requests, this if statement is for handling POST requests
	if request.method == 'POST' and form.validate():
		
		#session[] is a global variable which we can use to pass values between methods in this file, we're saving the data returned by the form with name "name"
		session['selectedViews'] = form.name.data #form.name.data gets data from the form...NOTE: the .name here is related to the "name" variable of the "form" object.."name" is an object of the SelectField class so it has "data" defined inside its class definition
		
		#saving contents of the global variable into a variable
		det = session['selectedViews']

		#establishing connection
		connection = sqlite3.connect('data.db')
		
		#creating a cursor
		cursor = connection.cursor()
		
		'''
		this portion her is to decide what data we want to send to the page we render after our post request...we use data returned from the select field called name and compare 
		save it in det then compare it with the strings which are in this case our Food Group names. It executes the select from the database for the query passed to it and renders it in our html file
		'''
		
		if(det == 'MajorInfo'):
			#writing a query which we want to be executed using the cursor.execute method
			query = 'SELECT * FROM MajorInfo'
		if(det == 'ProteinManu_Protein'):
			query = 'SELECT * FROM ProteinManu_Protein'
		if(det == 'HeavyProtein_protein'):
			query = 'SELECT * FROM HeavyProtein_protein'
		if(det == 'FoodManufacturers'):
			query = 'SELECT * FROM FoodManufacturers'
		if(det == 'HeavyProtein_LowCarb'):
			query = 'SELECT * FROM HeavyProtein_LowCarb'
		if(det == 'AverageRatings'):
			query = 'SELECT * FROM AverageRatings'
		if(det == 'HighlyRated'):
			query = 'SELECT * FROM HighlyRated'
		if(det == 'CommonNutrients'):
			query = 'SELECT * FROM CommonNutrients'
		if(det == 'MostReviewed'):
			query = 'SELECT * FROM MostReviewed'
		if(det == 'RecentReviews'):
			query = 'SELECT * FROM RecentReviews'
			
		#saving into result a list which holds the (tuples which is a data structure that holds the values of column for each row) this list holds multiple tuples we grab...in view 1 of result we have the first row from our result and so on...
		result = cursor.execute(query)
		items = []
		#for each tuple saved in the result list, we want to save it into an array...this is pretty redundant but this is done because we want to really make sure we were passing a list to the html file
		for row in result:
			items.append(row)
		#close our connection, good practice
		connection.close()	
		
		#rendering html file "views.html" and passing it the items array and the foodgroup name which is saved in det...
		#items and check are variables in the html file. 
		#check is used in the html file inside if statements that render our correct table based on name in check equals the name we compare it with in the if statement
		#(Jinja allows us to use these inside our html)
		return render_template("views.html", items = items, check = det ) 
	
	#this is the template renderd on a get request and we just pass it the form we want to show when page loads
	return render_template("index.html", form = form)

#search link so users can be able to search
@app.route('/search', methods = ['GET', 'POST'])
def search():
	#Defining form class to hold form methods 
	class SearchForm(Form):
		nameoffood = StringField('Food')
		nameofmanu = StringField('Food')
	
	#creating form SearchForm objects
	form = SearchForm()
	form2 = SearchForm()
	
	#Selecting Foodname for each food saved in the database
	connection = sqlite3.connect('data.db')
	cursor = connection.cursor()
	query = 'SELECT FoodName FROM Food'
	results = cursor.execute(query)
	food = [] #food is a list item we pass to our html file for it to iterate through all food names
	#we append all food names into the food array
	for row in results:
		#the reason we make both tuples the same is, the value for food that's returned from the form is the same as the name displayed...eases what we need in terms of comparing the returned value in our python file
		tuple = (row[0],row[0])
		food.append(tuple)
	connection.close()
	
	#same logic as previous select statement and for loop except now we do it for our manufacturer names
	connection = sqlite3.connect('data.db')
	cursor = connection.cursor()
	query2 = 'SELECT Name FROM Manufacturer'
	results2 = cursor.execute(query2)
	food2 = []
	#result are saved to list "food2" and is passed as options2 to the html file
	for row2 in results2:
		tuple2 = (row2[0],row2[0])
		food2.append(tuple2)
	connection.close()
	
	#connectiong to the database to select reviews in order to display them
	connection = sqlite3.connect('data.db')
	cursor = connection.cursor()
	query = 'SELECT f.ID as "Food ID", f.FoodName as "Food", f.GroupName as "Category", f.ManufacturerName as "Manufacturer", AVG(r.Rating) as "Rating", COUNT(r.rating) as "# of Reviews", n.Energy as "Calories" FROM Food f left outer join Ratings r on f.ID = r.FoodID inner join Nutrients n on f.ID = n.FoodID GROUP BY f.ID, f.FoodName, f.GroupName, f.ManufacturerName, n.Energy ORDER BY f.FoodName'
	result = cursor.execute(query)
	something = [] 
	#results are saved to a variable for us to use in the html file "something" is passed to "items" when we render
	for next in result:
		something.append(next)
	connection.close()
	
	
	print(form.errors)
	#if statement to handle post requests
	if request.method == 'POST' and form.validate():
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()
		query = 'SELECT f.ID as "Food ID", f.FoodName as "Food", f.GroupName as "Category", f.ManufacturerName as "Manufacturer", AVG(r.Rating) as "Rating", COUNT(r.rating) as "# of Reviews", n.Energy as "Calories" FROM Food f left outer join Ratings r on f.ID = r.FoodID inner join Nutrients n on f.ID = n.FoodID WHERE f.FoodName LIKE "%{}%" AND f.GroupName LIKE "%{}%" AND f.ManufacturerName LIKE "%{}%" GROUP BY f.ID, f.FoodName, f.GroupName, f.ManufacturerName, n.Energy HAVING AVG(r.Rating) >= {} ORDER BY f.FoodName'.format(form.nameoffood.data, request.form['foodgroups'], form2.nameofmanu.data, float(request.form['rating']))
		results = cursor.execute(query)
		foods = []
		for row in results:
			foods.append(row) #saving all tuples into the food list so we can render it on the html
		return render_template("search.html", options = food, options2 = food2, form = form, form2 = form2, items = foods)
		connection.close()
		
	#on a get request we send them the search.html file
	return render_template("search.html",options = food, options2 = food2, form = form, form2 = form2, items = something)

#this is another route we are taken to to display a certain foods attributes
@app.route('/search/<string:foodname>', methods = ['GET', 'POST'])
def click(foodname):
	#RatingForm class
	class Ratingform(Form):
		name = SelectField()
	form = Ratingform()
	#handling post requests, this is for when a user submits a rating
	if request.method == 'POST':
		if not request.form['rating']:
			error = 'You have to input a rating'
			print(error)
		else:
			connection = sqlite3.connect('data.db')
			cursor = connection.cursor()
			#selecting the last rating id so we can update the database with correct rating id's that increment
			query = 'SELECT MAX(RatingID) FROM Ratings'
			answer = cursor.execute(query)
			#to access the value stored in answer we use the for loop and save it to digit
			for row in answer:
				digit = row[0]
			#the tuple we insert into the table. digit+1 is how we increment the id..."request.form['rating']" accesses value sent by the form that is named name "rating"
			#earlier we used "form.name.data" but this only works when we define the form object from our own server, however in this case we define a form and assign it tne name "rating" in the html and not in the server
			tuple = (request.form['foodid'],(digit+1),request.form['rating'],request.form['message'],request.form['name'])
			query = 'INSERT INTO Ratings VALUES(?,?,?,?,?)'
			cursor.execute(query,tuple)
			connection.commit()
			connection.close()
			#redirecting to the same page so user can see if their comment is uploaded
			return redirect('/search/<{}>'.format(foodname))
	
	connection = sqlite3.connect('data.db')
	cursor = connection.cursor()
	
	#this is the section that gets run for GET requests
	query = 'select * from majorinfo'
	idget = cursor.execute(query)
	foodname = foodname[1:-1] #just truncating the first and element in the string daved in foodname
	#retrieving the id of the object we want by comparing the foodname sent to us with the foodname of all results we get, when we find a match we take its id which is in column5 in table/index4 of the tuple structure 
	for idrow in idget:
		id_retrieval = idrow[4]
		if(idrow[0] == foodname):
			id_retrieval = idrow[4]
			break;
	
	#this retrieves the 3 most recent ratings from the database
	query = 'select r.displayname, r.rating, r.review from ratings r where r.foodid = {} order by r.ratingid desc limit 3'.format(int(id_retrieval))
	ratingtable = cursor.execute(query)
	ratings = []
	for eachrow in ratingtable:
		ratings.append(eachrow)	
	
	#based on the foodname we are sent through the url, we retrieve information from the database and compare the name with all names retrieved, if the name is matched, we render all its values on this page
	query = 'select food.foodname, food.*, nutrients.*, round(avg(ratings.rating),1), count(ratings.rating) from food join nutrients on food.id = nutrients.foodid left join ratings on food.id = ratings.foodid group by food.id'
	results = cursor.execute(query)
	foods = []
	print(foodname)
	for row in results:
		if(row[0] == foodname):
			foods.append(row)
			return render_template("results.html", items = foods, form = form, ratings = ratings)
	return "Cant Find it are you sure that food exists"
	connection.close()

@app.route('/api/<foodid>', methods = ['GET'])
def api(foodid):
	connection = sqlite3.connect('data.db')
	cursor = connection.cursor();
	query = 'Select * from Food WHERE ID = {}'.format(int(foodid))
	ratingtable = cursor.execute(query)
	foodtable = []
	dict = {}
	for eachrow in ratingtable:
		dict['{}'.format(eachrow[1])] = {'id': '{}'.format(eachrow[0]),'foodname': "{}".format(eachrow[1]),'ingredients': "{}".format(eachrow[2]),'shortdesc': "{}".format(eachrow[3]),'scientificname': "{}".format(eachrow[4]),'commercialName': "{}".format(eachrow[5]),'lastIngUpdate':"{}".format(eachrow[6]),'DBsource': "{}".format(eachrow[7]),'Groupname': "{}".format(eachrow[8]),'manu': "{}".format(eachrow[9])}

	return jsonify({'foodinfo': dict})
	connection.close()

#	return render_template("search.html",options = food, form = form)
if __name__ == '__main__':
	app.run(debug = True, host = 'localhost')