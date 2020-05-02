#!/usr/bin/env python
# coding: utf-8

# In[14]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


# In[15]:


#
def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver.exe", headless=True)
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scrapping functions and store results in dictionnary
    data = {
            "news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "last_modified": dt.datetime.now()
        
            }
    if __name__== "__main__":
        # If running as scrip, print scraped data
        print(scrape_all())
    
    return
    


# In[16]:


# Set the executable path and initialize the chrome browser in splinter


# In[17]:


def mars_news(browser):
    
    # visit the Mars NASA news site
    url ="https://mars.nasa.gov/news"
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    
    # Parse the HTML with BeautifulSoup
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        slide_elem.find("div", class_="content_title")
    
        # Use the parent element to find the first "a" tag and save it as "news_title"
        news_title = slide_elem.find("div", class_="content_title").get_text()
    
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None
        
    return news_title, news_p 


# ### Featured Images

# In[18]:


def featured_image(browser):
    # Visit url
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    
    # Find and click the full image button
    full_image_elem = browser.find_by_id ("full_image")
    full_image_elem.click()
    
    # Find the more info button and click that
    browser.is_element_present_by_text ("more info", wait_time=1)
    more_info_elem = browser.find_link_by_partial_text ("more info")
    more_info_elem.click()
    
    # Parse the resulting HTML with BeautifulSoup
    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser")
    
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one ("figure.lede a img").get("src")
        
    except AttributeError:
        return None
    
    # Use the base URL to create an absolute URL
    img_url = f"https://www.jpl.nasa.gov{img_url_rel}"
    
    return img_url


# In[19]:


def mars_facts():
    # Add try/except for error handling
    try:
        # Use "read_html" to scrape the facts table into a DataFrame
        df = pd.read_html("https://space-facts.com/mars/")[0]
        
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)

    # Convert dataframe into HTML
    return df.to_html()


# In[20]:


# End the browser session
browser.quit()


# In[ ]:




