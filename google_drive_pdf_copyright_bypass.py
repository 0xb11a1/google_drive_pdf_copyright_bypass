#!/usr/bin/python3
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import time
import os
import warnings

# ignore deprecation warnings 
warnings.filterwarnings("ignore", category=DeprecationWarning) 


google_drive_url = ""
google_drive_img_link = ""

# get url input
google_drive_url = input("Enter Google Drive PDF URL : ")

# running a porxy server and requesting the pdf link to get the page_image URL
dict = {'port': 8090}
server = Server(
    path="./browsermob-proxy", options=dict)
server.start()
time.sleep(1)
proxy = server.create_proxy()
time.sleep(1)
profile = webdriver.FirefoxProfile()
selenium_proxy = proxy.selenium_proxy()
profile.set_proxy(selenium_proxy)
driver = webdriver.Firefox(firefox_profile=profile)
proxy.new_har("google")
driver.get(google_drive_url)


# get book name based on url title
page_title = driver.title
book_name = page_title[:page_title.find(".pdf")].replace(" ", "_")

# delay for the page to finish loading 
time.sleep(20)
# scroll down - to force the page to request the page_image URL for capturing it 
html = driver.find_element_by_tag_name('body')
html.send_keys(Keys.END)


time.sleep(1)
# get number of pages 
page_number = int(driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[3]/div[1]/div[3]").text)
# delay for the page to finish loading the new pages 
time.sleep(10)

# search for page_image url from the capured data 
for req in proxy.har['log']['entries']:
    # global google_drive_img_link
    if 'https://drive.google.com/viewerng/img?id=' in req['request']['url']:
        google_drive_img_link = req['request']['url']
        print("found img url : {}".format(req['request']['url']))
        break


page_indx = google_drive_img_link.find("page=") + 5

# get leading zeros count
page_number_digit_count = 0
page_number_tmp = page_number
while page_number_tmp > 0:
    page_number_digit_count += 1
    page_number_tmp //= 10

# make directory to save the results in it 
os.system("mkdir -p {}/imgs/".format(book_name))


# downloading each page as an image
for i in range(page_number):
    google_drive_img_link_modified = google_drive_img_link[:page_indx] + str(i) + "&w=1600"
    print("downloading page {}".format(i+1))
    urllib.request.urlretrieve(google_drive_img_link_modified, "./{bookname}/imgs/page_{counter}.png".format(
        bookname=book_name,counter="{:0{}d}".format(i, page_number_digit_count)))

# converting the images to pdf file 
os.system("img2pdf  ./{bookname}/imgs/*.png -o ./{bookname}/{bookname}.pdf".format(bookname=book_name))
server.stop()
driver.quit()