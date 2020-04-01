from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_agg


app = Flask(__name__)

# Use PyMongo to establish Mongo connection
news_mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_News")
weather_mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_weather")
hemi_mongo = PyMongo(app,uri="mongodb://localhost:27017/Mars_Hemi")


@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_news_data = news_mongo.db.mars_news.find_one()
    # mars_img_data = img_mongo.db.img_urls.find_one()
    mars_weather_data = weather_mongo.db.weather.find_one()
    # Return template and data
    mars_hemi_data = hemi_mongo.db.hemisphere.find(limit = 4)
    return render_template("index.html", 
    news_mars = mars_news_data,
    weather_mars = mars_weather_data, 
    mars_hemi_data = mars_hemi_data )


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    news_data = scrape_mars_agg.scrape_mars_news_fun()

    for d in news_data:    

        # Update the Mongo database using update and upsert=True
        news_mongo.db.mars_news.update({}, d, upsert=True)

    weather_data = scrape_mars_agg.scrape_mars_weather_fun()

    for d in weather_data:    
        
        # Update the Mongo database using update and upsert=True
        weather_mongo.db.weather.update({}, d, upsert=True)
    
    hemi_data = scrape_mars_agg.scrape_mars_hemi_fun()

    for d in hemi_data:    
        
        # Update the Mongo database using update and upsert=True
        hemi_mongo.db.hemisphere.update({}, d, upsert=True)
            
    # Redirect back to home page
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)
