# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup

# Define funtion to visit site and scrap for hemisphere name and image url and store results in dictionnary
def scrape_all():
    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path)
    
    # visit the Astropedia Mars Hemisphere site
    url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    
    # Allow delay for loading the page
    browser.is_element_present_by_css("div.description", wait_time=10)

    # Parse the HTML with BeautifulSoup
    html = browser.html
    b_soup = BeautifulSoup(html, "html.parser") 
    
    # find the parent element for the hemisphere title
    title_elem = b_soup.select("div.description")
    
    # Declare a dictionnary for titles and image urls
    data = {}
    
    # Use the parent element to find all the "h3" tags and save them in a titles list
    title_list = title_elem.find_all("h3").get_text()
        
    # Call functions to get title and img_url for all the titles
    for title in title_list:
     
        # Store titles and img_url's to dictionnary
        data = data.update({
            "title" : title,
            "img_url" : get_image(browser, b_soup)        
            })
        
        # Return to the Astropedia Mars Hemisphere site
        browser.visit(url)
        
    # If running as script, print scraped data
    if __name__== "__main__":
        print(scrape_all())
        
    # End the browser session
    browser.quit()
    
    return data

# Define the enhanced image urls function
def get_image(browser, b_soup):

    # Find and click the thumnnail image to get to enhanced image page
    image_elem = browser.find_next("img", class_="thumb")
    image_elem.click()
    
    # Allow delay for loading the enhanced image page
    browser.is_element_present_by_text("Original", wait_time=30)
        
    # Parse the HTML with BeautifulSoup
    html = browser.html
    img_soup = BeautifulSoup(html, "html.parser") 
    
    try:
        # Find the urls for the enhanced images
        img_url = img_soup.find(text="Original").get("href")
                
    except AttributeError:
        return None
        
    return img_url