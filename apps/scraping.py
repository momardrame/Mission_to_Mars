{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import Dependencies\n",
    "import pandas as pd\n",
    "import datetime as dt\n",
    "from datetime import datetime"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Import splinter and BeautifulShop dependicies\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\tenle\\Anaconda3\\lib\\site-packages\\splinter\\driver\\webdriver\\__init__.py:528: FutureWarning: browser.find_link_by_partial_text is deprecated. Use browser.links.find_by_partial_text instead.\n",
      "  FutureWarning,\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'news_title': \"How NASA's Perseverance Mars Team Adjusted to Work in the Time of Coronavirus \", 'news_paragraph': 'Like much of the rest of the world, the Mars rover team is pushing forward with its mission-critical work while putting the health and safety of their colleagues and community first.', 'featured_image': 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA22831_hires.jpg', 'facts': '<table border=\"1\" class=\"dataframe\">\\n  <thead>\\n    <tr style=\"text-align: right;\">\\n      <th></th>\\n      <th>Mars</th>\\n    </tr>\\n    <tr>\\n      <th>Description</th>\\n      <th></th>\\n    </tr>\\n  </thead>\\n  <tbody>\\n    <tr>\\n      <th>Equatorial Diameter:</th>\\n      <td>6,792 km</td>\\n    </tr>\\n    <tr>\\n      <th>Polar Diameter:</th>\\n      <td>6,752 km</td>\\n    </tr>\\n    <tr>\\n      <th>Mass:</th>\\n      <td>6.39 × 10^23 kg (0.11 Earths)</td>\\n    </tr>\\n    <tr>\\n      <th>Moons:</th>\\n      <td>2 (Phobos &amp; Deimos)</td>\\n    </tr>\\n    <tr>\\n      <th>Orbit Distance:</th>\\n      <td>227,943,824 km (1.38 AU)</td>\\n    </tr>\\n    <tr>\\n      <th>Orbit Period:</th>\\n      <td>687 days (1.9 years)</td>\\n    </tr>\\n    <tr>\\n      <th>Surface Temperature:</th>\\n      <td>-87 to -5 °C</td>\\n    </tr>\\n    <tr>\\n      <th>First Record:</th>\\n      <td>2nd millennium BC</td>\\n    </tr>\\n    <tr>\\n      <th>Recorded By:</th>\\n      <td>Egyptian astronomers</td>\\n    </tr>\\n  </tbody>\\n</table>', 'last_modified': datetime.datetime(2020, 4, 24, 14, 58, 44, 302799)}\n"
     ]
    }
   ],
   "source": [
    "\n",
    "def scrape_all():\n",
    "    # Initiate headless driver for deployment\n",
    "    browser = Browser(\"chrome\", executable_path=\"chromedriver\", headless=True)\n",
    "\n",
    "    news_title, news_paragraph = mars_news(browser)\n",
    "    # Run all scraping functions and store results in dictionary\n",
    "    data = {\n",
    "        \"news_title\": news_title,\n",
    "        \"news_paragraph\": news_paragraph,\n",
    "        \"featured_image\": featured_image(browser),\n",
    "        \"facts\": mars_facts(),\n",
    "        \"last_modified\": dt.datetime.now()\n",
    "        }\n",
    "    return data\n",
    "\n",
    "def mars_news(browser):\n",
    "    # Featured Article \n",
    "    # Visit the mars nasa news site\n",
    "    url = 'https://mars.nasa.gov/news/'\n",
    "    browser.visit(url)\n",
    "    # Optional delay for loading the page\n",
    "    browser.is_element_present_by_css(\"ul.item_list li.slide\", wait_time=1)\n",
    "    # Set up the HTML parser:\n",
    "    html = browser.html\n",
    "    news_soup = BeautifulSoup(html, 'html.parser')\n",
    "    # Add try/except for error handling\n",
    "    try:\n",
    "        slide_elem = news_soup.select_one('ul.item_list li.slide')\n",
    "        # Chain .find onto our previously assigned variable, \"slide_elem.\"\n",
    "        slide_elem.find(\"div\", class_='content_title')\n",
    "        # Use the parent element to find the first `a` tag and save it as `news_title`\n",
    "        news_title = slide_elem.find(\"div\", class_='content_title').get_text()\n",
    "        # Use the parent element to find the paragraph text\n",
    "        news_p = slide_elem.find('div', class_=\"article_teaser_body\").get_text()\n",
    "        \n",
    "    except AttributeError:\n",
    "        return None, None\n",
    "    return news_title, news_p\n",
    "\n",
    "def featured_image(browser):\n",
    "    # Featured Images\n",
    "    # # Visit URL\n",
    "    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "    browser.visit(url)\n",
    "    # Find and click the full image button\n",
    "    full_image_elem = browser.find_by_id('full_image')\n",
    "    full_image_elem.click()\n",
    "    # Find the more info button and click that\n",
    "    browser.is_element_present_by_text('more info', wait_time=1)\n",
    "    more_info_elem = browser.find_link_by_partial_text('more info')\n",
    "    more_info_elem.click()\n",
    "    # Parse the resulting html with soup\n",
    "    html = browser.html\n",
    "    img_soup = BeautifulSoup(html, 'html.parser')\n",
    "    try:\n",
    "        # Find the relative image url\n",
    "        img_url_rel = img_soup.select_one('figure.lede a img').get(\"src\")\n",
    "        \n",
    "    except AttributeError:\n",
    "        return None\n",
    "        # Use the base URL to create an absolute URL\n",
    "    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'\n",
    "    return img_url\n",
    "\n",
    "def mars_facts():\n",
    "    # Add try/except for error handling\n",
    "    try:\n",
    "        # Use 'read_html' to scrape the facts table into a dataframe\n",
    "        df = pd.read_html('http://space-facts.com/mars/')[0]\n",
    "\n",
    "    except BaseException:\n",
    "        return None\n",
    "    # Assign columns and set index of dataframe\n",
    "    df.columns=['Description', 'Mars']\n",
    "    df.set_index('Description', inplace=True)\n",
    "    # Convert dataframe into HTML format, add bootstrap\n",
    "    return df.to_html()\n",
    "    \n",
    "if __name__ == \"__main__\":\n",
    "        # If running as script, print scraped data\n",
    "        print(scrape_all())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Automate chrome browser with Splinter\n",
    "# unpacking dicitionary\n",
    "executable_path = {'executable_path': 'chromedriver.exe'} \n",
    "# display all browser actions\n",
    "browser = Browser('chrome',**executable_path, headless=False) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Assign the url and instruct the browser to visit it.\n",
    "# Visit the mars nasa news site\n",
    "url = 'https://mars.nasa.gov/news/'\n",
    "browser.visit(url)\n",
    "# Optional delay for loading the page\n",
    "browser.is_element_present_by_css(\"ul.item_list li.slide\", wait_time=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Set the HTML parser\n",
    "html = browser.html\n",
    "news_soup = BeautifulSoup(html, 'html.parser')\n",
    "slide_elem = news_soup.select_one('ul.item_list li.slide')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<div class=\"content_title\"><a href=\"/news/8654/how-nasas-perseverance-mars-team-adjusted-to-work-in-the-time-of-coronavirus/\" target=\"_self\">How NASA's Perseverance Mars Team Adjusted to Work in the Time of Coronavirus </a></div>"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Scrape the article title\n",
    "# Chain slide.elm variable to the find function\n",
    "# The specific data is in a <div /> with a class of 'content_title\n",
    "slide_elem.find(\"div\", class_='content_title')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Use the parent element to find the first `a` tag and save it as `news_title`\n",
    "# We’re also stripping the additional HTML attributes and tags with the use of .get_text().\n",
    "news_title = slide_elem.find(\"div\", class_='content_title').get_text()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'Like much of the rest of the world, the Mars rover team is pushing forward with its mission-critical work while putting the health and safety of their colleagues and community first.'"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Use the parent element to find the paragraph text\n",
    "news_p = slide_elem.find('div', class_=\"article_teaser_body\").get_text()\n",
    "news_p"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "\"### Featured Images\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visit URL\n",
    "url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'\n",
    "browser.visit(url)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Find and click the full image button\n",
    "full_image_elem = browser.find_by_id('full_image')\n",
    "full_image_elem.click()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\tenle\\Anaconda3\\lib\\site-packages\\splinter\\driver\\webdriver\\__init__.py:528: FutureWarning: browser.find_link_by_partial_text is deprecated. Use browser.links.find_by_partial_text instead.\n",
      "  FutureWarning,\n"
     ]
    }
   ],
   "source": [
    "# Find the more info button and click that\n",
    "browser.is_element_present_by_text('more info', wait_time=1)\n",
    "more_info_elem = browser.find_link_by_partial_text('more info')\n",
    "more_info_elem.click()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "With the new page loaded onto our automated browser, it needs to be parsed so we can continue and scrape the full-size image URL."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Parse the resulting html with soup\n",
    "html = browser.html\n",
    "img_soup = BeautifulSoup(html, 'html.parser')"
   ]
  },
  {
   "cell_type": "raw",
   "metadata": {},
   "source": [
    "We’ll use all three of these tags (<figure />, <a />, and <img />) to build the URL to the full-size image."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'/spaceimages/images/largesize/PIA22831_hires.jpg'"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Find the relative image url\n",
    "img_url_rel = img_soup.select_one('figure.lede a img').get(\"src\")\n",
    "img_url_rel"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'/spaceimages/images/largesize/PIA22831_hires.jpg'"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Find the relative image url\n",
    "img_url_rel = img_soup.select_one('figure.lede a img').get(\"src\")\n",
    "img_url_rel"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Scrape Mars Data: Mars Facts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>value</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>description</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>Equatorial Diameter:</th>\n",
       "      <td>6,792 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Polar Diameter:</th>\n",
       "      <td>6,752 km</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Mass:</th>\n",
       "      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Moons:</th>\n",
       "      <td>2 (Phobos &amp; Deimos)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Orbit Distance:</th>\n",
       "      <td>227,943,824 km (1.38 AU)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Orbit Period:</th>\n",
       "      <td>687 days (1.9 years)</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Surface Temperature:</th>\n",
       "      <td>-87 to -5 °C</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>First Record:</th>\n",
       "      <td>2nd millennium BC</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Recorded By:</th>\n",
       "      <td>Egyptian astronomers</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                              value\n",
       "description                                        \n",
       "Equatorial Diameter:                       6,792 km\n",
       "Polar Diameter:                            6,752 km\n",
       "Mass:                 6.39 × 10^23 kg (0.11 Earths)\n",
       "Moons:                          2 (Phobos & Deimos)\n",
       "Orbit Distance:            227,943,824 km (1.38 AU)\n",
       "Orbit Period:                  687 days (1.9 years)\n",
       "Surface Temperature:                   -87 to -5 °C\n",
       "First Record:                     2nd millennium BC\n",
       "Recorded By:                   Egyptian astronomers"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# we’re going to scrape the entire table with Pandas’ .read_html() function\n",
    "import pandas as pd\n",
    "df = pd.read_html('http://space-facts.com/mars/')[0]\n",
    "df.columns=['description', 'value']\n",
    "df.set_index('description', inplace=True)\n",
    "df"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Export to Python"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
