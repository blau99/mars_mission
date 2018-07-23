# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/db"
mongo = PyMongo(app)


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars=mars)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    news = scrape_mars.scrape_news()
    featured = scrape_mars.scrape_featured()
    weather = scrape_mars.scrape_weather()
    table = scrape_mars.scrape_table()
    images = scrape_mars.scrape_images()

    mars_data = {
        "news_title": news["news_title"],
        "news_p": news["news_p"],
        "featured_image_url": featured["featured_image_url"],
        "weather": weather["mars_weather"],
        "table": table["mars_table"],
        "images": images["hemisphere_image_url"]
    }
    # Insert forecast into database
    mongo.db.collection.insert_one(mars_data)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
