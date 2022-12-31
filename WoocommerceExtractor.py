from bs4 import BeautifulSoup
from requests import get
from datetime import datetime
import csv
import math
import sys
import re

def buildURL(domain,entryTitle, entryID):
    s = re.sub('[^0-9a-zA-Z]+', '-', entryTitle+"-"+entryID)
    if s[-1] == '-':
        s = s[:-1]
    url = f"https://{domain}/product/{s}"
    return url

if __name__ == '__main__':
    catalog = []
    page_number = 1
    page_limit = 2
    if len(sys.argv) == 2:
        domain = sys.argv[1]
    else:
        print("Usage: 'python3 WoocommerceExtractor.py only-domain.com '")
        exit()
        
    while page_number <= page_limit:
        url = f"https://{domain}/page/{page_number}/?s=&post_type=product"
        response = get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        
        if page_number == 1:
            limits = soup.find_all('p',class_='woocommerce-result-count')
            
            print("Detect page limit...")
            limits_text = '\n'.join([str(ele) for ele in limits])
            limits_nums = [int(i) for i in limits_text.split() if i.isdigit()]
            
            websitePageLimit = 0
            
            if (websitePageLimit <= 0):
              page_limit = (math.ceil(limits_nums[0]/16))
            else:
              page_limit = websitePageLimit
            
            print(page_limit)
            
        # Get Title            
        products = soup.find_all('h2', class_='woocommerce-loop-product__title')
        if not products:
            products = soup.find_all('p', class_='product-title')
            
        # Get Price            
        prices = soup.find_all('span', class_='woocommerce-Price-amount')
        
        # Get Thumbnail            
        thumbnailProduct = soup.find_all('img', class_='attachment-woocommerce_thumbnail')
        
        for thumbnail in thumbnailProduct:
            thumb = thumbnail.get('src').replace(".jpg_",".jpg|")
            thumbnailNormalized = thumb
            
        print(thumbnailNormalized)
        
        print("scrapping page: ",page_number,"/",page_limit)
        for (item,entryPrice) in zip(products,prices):
            keywords = item.text.split()
            entryID = keywords.pop()
            item = ' '.join(keywords)
            entryPrice = entryPrice.text
            url = buildURL(domain,item,entryID)
            catalog.append( (item,entryID,entryPrice,url, thumbnailNormalized) )
        page_number += 1

    # Build CSV File
    print("Export to CSV ...")
    with open(f"{domain}_{datetime.now().date()}.csv",'w') as csvfile:
        fwriter = csv.writer(csvfile)
        
        fwriter.writerow(["Product","Product ID","Price","URL", "Thumbnail"])
        
        for (entryTitle, entryID,entryPrice,url, thumbnailNormalized) in catalog:
            fwriter.writerow([entryTitle,entryID,entryPrice,url, thumbnailNormalized])
    csvfile.close()

