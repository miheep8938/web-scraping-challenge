from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from config import password

import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, f"mongodb+srv://mihee:{password}@cluster0.fkk74.mongodb.net/mars_db?retryWrites=true&w=majority")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_dictionary = mongo.db.mars_dictionary.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_dictionary)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars_dictionary = mongo.db.mars_dictionary
    # Run the scrape function
    mars_data = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_dictionary.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code = 302)


if __name__ == "__main__":
    app.run(debug=True)
