#!/usr/bin/env python

# Import Splinter, BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path)

#visit thr Mars NASA news site
url ="https://mars.nasa.gov/news"
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Parse the HTML with BeautifulSoup
html = browser.html
news_soup = BeautifulSoup(html, "html.parser")
slide_elem = news_soup.select_one("ul.item_list li.slide")

# Use the parent element to find the first "a" tag and save it as "news_title"
news_title = slide_elem.find("div", class_="content_title").get_text()

# Use the parent element to find the first "a" tag and save it as "news_title"
news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

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

# Parse the resulting hitml with soup
html = browser.html
img_soup = BeautifulSoup(html, "html.parser")

# Find the relative image url
img_url_rel = img_soup.select_one ("figure.lede a img").get("src")
img_url_rel

# Use the base URL to create an absolute URL
img_url = f"https://www.jpl.nasa.gov{img_url_rel}"
img_url

# Read the HTML table into a DataFrame
df = pd.read_html("https://space-facts.com/mars/")[0]
df.columns=["Description", "Value"]
df.set_index("Description", inplace=True)
df

# Convert DataFrame to HTML format
df.to_html()

# Quit the browser session
browser.quit()