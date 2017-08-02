
# coding: utf-8

# # Export awoiaf.westeros.org
# 
# This script will use the mediawiki export page to get all the data from http://awoiaf.westeros.org/index.php/Special:Export
# 
# Author:
#     Shubhanshu Mishra
# 

# In[1]:

from urllib.parse import parse_qs, urlparse
import requests
from bs4 import BeautifulSoup


# In[2]:

BASE_URL="http://awoiaf.westeros.org"
BASE_PATH=BASE_URL+"/index.php?title=Category:A_Song_of_Ice_And_Fire_chapters"


# ## Download process (manual)
# 
# Go to `BASE_URL` and then in the console type the following:
# 
# ```
# $("#mw-pages > div > table > tbody > tr a").each(function(i, a){console.log($(a).attr("href"));})
# ```
# 
# This should print the list of 200 pages on this category pages.
# 
# Get the link to the next page using
# ```
# $($("#mw-pages > a")[1]).attr("href")
# ```

# In[3]:

response = requests.get(BASE_PATH)


# In[4]:

soup = BeautifulSoup(response.text, "lxml")


# In[5]:

for link in soup.select("#mw-pages > div > table > tr a")[:10]:
    print(link.attrs["href"].rsplit("/", 1)[-1])


# In[6]:

soup.select("#mw-pages > a")[0].attrs


# In[7]:

parse_qs(urlparse(soup.select("#mw-pages > a")[0].attrs["href"]).query)


# In[8]:

response = requests.get(BASE_URL+soup.select("#mw-pages > a")[0].attrs["href"])
soup = BeautifulSoup(response.text, "lxml")
soup.select("#mw-pages > a")[0].attrs["href"]


# In[9]:

parse_qs(urlparse(soup.select("#mw-pages > a")[0].attrs["href"]).query)


# In[10]:

from urllib.parse import parse_qs, urlparse
('/index.php?title=Category:A_Song_of_Ice_And_Fire_chapters&pagefrom=A+Game+of+Thrones%3A+Chapter+09%0AA+Game+of+Thrones-Chapter+9#mw-pages')


# In[11]:

soup.select("#mw-pages > a")[0].text.strip().startswith("previous")


# In[12]:

soup.select("#mw-pages > a")[0].attrs


# In[13]:

def get_titles(base_path, final_titles=None, BASE_URL=""):
    if final_titles is None:
        final_titles = set([])
        
    print("Processing {}".format(base_path))
    response = requests.get(base_path)
    soup = BeautifulSoup(response.text, "lxml")
    next_page = soup.select("#mw-pages > a")[-1]
    is_last_page = next_page.text.strip().startswith("previous")
    counter = 0
    for link in soup.select("#mw-pages > div > table > tr a"):
        link = link.attrs["href"].rsplit("/", 1)[-1]
        final_titles.add(link)
        counter += 1
    print("Found {} titles. Total titles = {}".format(counter, len(final_titles)))
    if not is_last_page:
        base_path = BASE_URL + next_page.attrs["href"]
        final_titles = get_titles(base_path, final_titles, BASE_URL)
    return final_titles


# In[14]:

final_titles = get_titles(BASE_PATH, BASE_URL=BASE_URL)


# In[15]:

def get_wikiXML(titles, base_path):
    print(base_path)
    data = {
        "pages": "\r\n".join(titles),
        "curonly": 1,
        "wpDownload": 0
    }
    response = requests.post(base_path, data=data)
    output_file = requests.utils.parse_header_links(
        response.headers['Content-disposition']
    )[0]["filename"]
    with open(output_file, "w+") as fp:
        print(response.content, file=fp)
    print("Content saved to {}".format(output_file))


# In[16]:

EXPORT_PATH=BASE_URL+"/index.php?title=Special:Export&action=submit"
get_wikiXML(final_titles, EXPORT_PATH)


# In[ ]:



