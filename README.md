# Data Project
Repository to hold final project for data management course

#Windows Setup
- Install [Python 2.7](https://www.python.org/downloads/release/python-2712/)
```
Note: Python 3 can be used, but then "import urllib as urllib2" should be changed to
"import urllib.request as urllib2" in the CreateAll.py and AddFoodsNutrientsManu.py code
```
- Download Virtualenv
```
pip install virtualenv
```
- Change directories to the project folder and run 
```
virtualenv py3
```
- Activate the virtual environment
```
.\py3\Scripts\activate
```
- Install Flask as well using 
```
pip install flask
```
- When you have flask install WTF-forms using commands 
```
pip install WTForms
```
- Install RESTful using 
```
pip install flask-restful
```
- Install WTForms using 
```
pip install flask_wtf 
```
- After Completing Python installation, open Windows Command Prompt **cmd**
- Using **cd** command go to file location, Ensure you have **FoodWeb.py** and **datab.db**, next to **view** folder. The **view** folder contains the following;
**_base.html**, **index.html**, **results.html**, **search.html**, **views.html**, **About_Us.html**)

- While still in **Windows Command Prompt** Proceed by typing
```
python FoodWeb.py
```
  into the Command Prompt 
- If this does not work run try typing 
```
FoodWeb.py
```
  in the command prompt instead, or run it in **PyCharm** if this does not work.

- In your browser, view the whole application using
```
localhost:5000
```
- To use our api, go to
```
localhost:5000/api/<food_id> 
```
make sure to replace **<food_id>** with a number of your choice
