#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, render_template
from flask_pymongo import PyMongo

#import scraping


# In[2]:


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# In[3]:


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


# In[4]:


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"


# In[ ]:


if __name__ == "__main__":
    app.run()


# In[ ]:


__name__


# In[ ]:




