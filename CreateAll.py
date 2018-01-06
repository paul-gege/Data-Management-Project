import urllib  as urllib2
import json
import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
query = 'CREATE TABLE IF NOT EXISTS Food(ID INTEGER PRIMARY KEY NOT NULL,\
FoodName VARYING CHARACTER(255),\
Ingredients VARYING CHARACTER(1000),\
ShortDescription VARYING CHARACTER(1000),\
ScientificName VARYING CHARACTER(1000),\
CommercialName VARYING CHARACTER(1000),\
LastIngredientUpdate DATE,\
DBSource VARYING CHARACTER(20),\
GroupName VARYING CHARACTER(255) REFERENCES FoodGroups(GroupName) ON UPDATE NO ACTION ON DELETE NO ACTION,\
ManufacturerName VARYING CHARACTER(255) REFERENCES Manufacturer(ManufacturerName) ON UPDATE NO ACTION ON DELETE NO ACTION)'

cursor.execute(query)
connection.commit()

query = 'CREATE TABLE IF NOT EXISTS Manufacturer(Name VARYING CHARACTER(255) PRIMARY KEY NOT NULL, ID INTEGER NOT NULL)'

cursor.execute(query)
connection.commit()

query = 'CREATE TABLE IF NOT EXISTS Nutrients (FoodID INTEGER PRIMARY KEY NOT NULL REFERENCES Food(ID) ON UPDATE NO ACTION ON DELETE NO ACTION, Water REAL, Energy REAL, Protein REAL,\
"Total lipid fat" REAL, Carbohydrate REAL, Fiber REAL, "Total Sugar" REAL, Lactose REAL,\
Calcium REAL, Iron REAL, Potassium REAL, Sodium REAL, Zinc REAL,\
"Vitamin C" REAL, "Vitamin B12" REAL, "Vitamin D" REAL, "Cholesterol" REAL)'
cursor.execute(query)
connection.commit()

query = 'CREATE TABLE IF NOT EXISTS FoodGroup (id INTEGER PRIMARY KEY, GroupName VARYING CHARACTER(255))'
cursor.execute(query)
connection.commit()

query = 'CREATE TABLE IF NOT EXISTS Ratings(FoodID INTEGER NOT NULL REFERENCES Food(ID) ON UPDATE CASCADE ON DELETE CASCADE, RatingID INTEGER PRIMARY KEY NOT NULL, Rating INTEGER NOT NULL, Review VARYING CHARACTER(1000), DisplayName VARYING CHARACTER(50))'
cursor.execute(query)
connection.commit()

query1 = 'CREATE VIEW MajorInfo AS SELECT f."FoodName",round(AVG(r.Rating),1) AS "Average Rating", f."Ingredients", g."GroupName", n."FoodID", n."Water", n."Energy", n."Protein", n."Total lipid fat", n."Carbohydrate", n."Fiber", n."Total Sugar", n.Lactose, n."Calcium", n."Iron", n."Potassium", n."Sodium", n."Zinc", n."Vitamin C", n."Vitamin B12", n."Vitamin D", n."Cholesterol" FROM "Food" f Left JOIN "FoodGroup" g ON f."GroupName" = g."GroupName" JOIN "Nutrients" n ON f."ID" = n."FoodID" LEFT JOIN Ratings r ON f.ID = r.FoodID GROUP BY f."FoodName", f."Ingredients", g."GroupName", n."FoodID", n."Water", n."Energy", n."Protein", n."Total lipid fat", n."Carbohydrate", n."Fiber", n."Total Sugar", n.Lactose, n."Calcium", n."Iron", n."Potassium", n."Sodium", n."Zinc", n."Vitamin C", n."Vitamin B12", n."Vitamin D", n."Cholesterol";'
cursor.execute(query1)

query2 = 'CREATE VIEW ProteinManu_Protein AS SELECT m."Name", count(*) AS count FROM "Manufacturer" m, "Food" f WHERE m."Name" = f."ManufacturerName" AND (f."ID" IN (SELECT "Nutrients"."FoodID" FROM "Nutrients" WHERE "Nutrients"."Protein" > .1)) GROUP BY m."Name";'
cursor.execute(query2)

query3 = 'CREATE VIEW HeavyProtein_protein AS SELECT f."FoodName" FROM "Food" f WHERE (f."ID" IN ( SELECT "Nutrients"."FoodID" FROM "Nutrients" WHERE "Nutrients"."Protein" > .1));'
cursor.execute(query3)

query4 = 'CREATE VIEW FoodManufacturers AS   SELECT f."FoodName", ma."Name"  FROM   "food" f  LEFT JOIN "manufacturer" ma  ON f."manufacturername" = ma."name"   UNION   SELECT f."foodname",  ma."name"  FROM   "manufacturer" ma LEFT JOIN "food" f ON f."manufacturername" = ma."name";'
cursor.execute(query4)

query5 = 'CREATE VIEW HeavyProtein_LowCarb AS SELECT f."FoodName" FROM "Food" f WHERE (f."ID" IN ( SELECT "Nutrients"."FoodID" FROM "Nutrients" WHERE "Nutrients"."Protein" > .1)) INTERSECT SELECT f."FoodName" FROM "Food" f WHERE (f."ID" IN ( SELECT "Nutrients"."FoodID" FROM "Nutrients" WHERE "Nutrients"."Carbohydrate" < 20));'
cursor.execute(query5)

query6 = 'CREATE VIEW AverageRatings AS SELECT f."FoodName", f."ID", round(avg(r."Rating"),1) AS "AverageRating" FROM "Food" f, "Ratings" r WHERE r."FoodID" = f."ID" GROUP BY f."ID";'
cursor.execute(query6)

query7 = 'CREATE VIEW HighlyRated AS SELECT f."FoodName", avg(r."Rating") AS "Average Rating" FROM "Food" f JOIN "Ratings" r ON f."ID" = r."FoodID" GROUP BY f."ID" HAVING avg(r."Rating") >= 5;'
cursor.execute(query7)

query8 = 'CREATE VIEW CommonNutrients AS SELECT f."FoodName", f."Ingredients", g."GroupName", n."Energy" AS calories, n."Protein", n."Total lipid fat", n."Carbohydrate", n."Fiber", n."Total Sugar" FROM "Food" f LEFT JOIN "FoodGroup" g ON f."GroupName" = g."GroupName" JOIN "Nutrients" n ON f."ID" = n."FoodID";'
cursor.execute(query8)

query9 = 'CREATE VIEW MostReviewed AS SELECT f."FoodName", round(avg(r."Rating"),1) AS "Average Rating", count(r."Review") AS "Number of Ratings" FROM "Food" f JOIN "Ratings" r ON f."ID" = r."FoodID" GROUP BY f."FoodName" ORDER BY (count(r."Review")) DESC;'
cursor.execute(query9)

query10 = 'CREATE VIEW RecentReviews as SELECT f."FoodName",    r."Rating",    r."Review",    r."DisplayName" AS "User"   FROM "Food" f     JOIN "Ratings" r ON f."ID" = r."FoodID"  WHERE r."RatingID" >= (( SELECT max(r2."RatingID")-10 AS max      FROM "Ratings" r2          WHERE f."ID" = r."FoodID"));'
cursor.execute(query10)

connection.commit()
connection.close()