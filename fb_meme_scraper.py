from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from PIL import Image

import urllib.request

import time
import os

# TODOs:
# - Make images square (for Instagram)
# - Select top images/interface for that (saying already posted, do not want)
# - Store link as well to ensure there are not duplicates
# - Comment being caption? Get that as well?

# make data directory (if does not exist)
save_dir = ("data")
if not os.path.isdir(save_dir): os.makedirs(save_dir)

# get FB meme page
browser = webdriver.Chrome('/Users/nikhilmurthy/Dropbox (MIT)/School/2019-2020/Projects/chromedriver')
browser.get('https://www.facebook.com/groups/1638417209555402/')

# X paths for posts, pictures and like counts
post_begin_xpath1 = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[4]/div[4]/div/div[1]/div[1]/div["
post_begin_xpath2 = "/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div[4]/div[4]/div/div[1]/div["
picture_end_xpath = "]/div/div[2]/div[1]/div[2]/div[3]/div/div/div/div/a"
like_count_end_xpath = "]/div/div[2]/div[2]/form/div/div[2]/div[1]/div/div[1]/a/span[2]/span/span"

posts = []
num_posts = 500 # heuristic for number of posts (will be less as some indices are missing)

# scroll
for i in range(num_posts//10):
    browser.execute_script("window.scrollBy(0, 100000);")
    time.sleep(1.5)

# initial set of memes
for i in range(1, 20):
    try:
        picture = browser.find_element_by_xpath(post_begin_xpath1 + str(i) + picture_end_xpath)
        like_count = browser.find_element_by_xpath(post_begin_xpath1 + str(i) + like_count_end_xpath)
        posts.append((picture, like_count))
        print(i)
    except:
        continue

# majority of memes
for i in range(1, num_posts):
    try:
        picture = browser.find_element_by_xpath(post_begin_xpath2 + str(i) + picture_end_xpath)
        like_count = browser.find_element_by_xpath(post_begin_xpath2 + str(i) + like_count_end_xpath)
        posts.append((picture, like_count))
        print(i)
    except:
        continue

# convert like count string to int
def convertKtoNumber(number_str):
    try:
        # If in format [0-9]+
        return int(number_str)
    except:
        # If in format [0-9]+.[0-9]K
        if "." in number_str: 
            thousand, hundred = number_str.split(".")
            hundred = hundred[:-1]
            return int(thousand) * 1000 + int(hundred) * 100
        # If in format [0-9]+K
        else: 
            thousand = number_str[:-1]
            return int(thousand) * 1000

# save image given image url and file name
def saveImage(url, file_name):
    image = Image.open(urllib.request.urlopen(url))
    image.save(file_name)

# replace Selenium Web Elements with pic url and int
posts = [(pic.get_attribute("data-ploi"), convertKtoNumber(like.text)) for (pic, like) in posts]

# save data
i = 0
with open("meme_likes.txt", "w") as f:
    for pic, like in posts:
        file_name = "meme_" + str(i) + ".png"
        f.write(file_name + "," + str(like) + "\n")
        saveImage(pic, os.path.join(save_dir, file_name))
        i += 1

print("Processed " + str(len(posts)) + " memes!")
browser.quit()

