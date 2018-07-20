from optparse import OptionParser
from bs4 import BeautifulSoup
import requests
import pprint

base_search_url = 'https://miami.craigslist.org/search/'
pp = pprint.PrettyPrinter(indent=2)

def get_category_path_from_user():
    category = raw_input("Enter a craigslist category to use as a reference: ")
    return category

def get_craigslist_data(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise ValueError("Something went wrong getting that category")
    data = r.text
    return data

def get_listings_rows(soup):
    sortable_res_cont = soup.find(id="sortable-results")
    listing_rows = sortable_res_cont.find_all('li', class_="result-row")
    return listing_rows

"""
    get_listings_dicts returns a list of dictionaries, each dict 
    contains the listing title, and the url path to the actual listing
    e.g
    {
        url: '/mcd/pet/d/labrador-retrievers/62546415616.html',
        title: 'Labrador Retrievers puppy!!'
    }
"""
def get_listings_dicts(listing_rows):
    listings = []
    for row in listing_rows:
        listing_href = row.find('p', class_="result-info").find('a', class_="result-title")
        title = listing_href.text
        link = listing_href.attrs['href']
        listings.append({
            "title": title,
            "url": link
        })
    return listings

def get_craigslist_url(category_path):
    return base_search_url + category_path

##
# Main
def main():
    # print "Welcome. We'll generate a craigslist style posting for you. \n"
    # category = get_category_path_from_user()
    # url = get_craigslist_url(category)
    # try: 
    #     raw_data = get_craigslist_data(url)
    # except ValueError as err:
    #     print err
    # soup = BeautifulSoup(raw_data, "html.parser")
    # listing_rows = get_listings_rows(soup)
    
    # listings = get_listings_dicts(listing_rows)
    # pp.pprint(listings)
    parser = OptionParser()
    parser.add_option("-s", "--source", 
        dest="source",
        help="The source file for the text to be analyzed")
    parser.add_option("-n", "--ngraml",
        dest="ngraml",
        help="The ngram length to be use")
    options, args = parser.parse_args()
    print(options, args)

if __name__ == "__main__":
    main()