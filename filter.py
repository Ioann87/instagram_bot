import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


def xpath_existence(url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence


login = "**********"
password = "*********"

days = 60
account_subscriptions = 350
publication = 5
limit_person = 400
today = datetime.now()

browser = webdriver.Chrome(r"C:\Users\Ioann\Documents\django\instagram_bot\chromedriver.exe")
browser.get("http://www.instagram.com/accounts/login")
time.sleep(10)

browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(
    login)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(
    password)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]").click()
time.sleep(5)

f = open(r"C:\Users\Ioann\Documents\django\instagram_bot\persons_list.txt", 'r')
file_list = []
for line in f:
    file_list.append(line)
    if line == limit_person:
        break
f.close()

filtered_list = []
i = 0
j = 0

for person in file_list:
    j += 1
    browser.get(person)
    time.sleep(10)

    element = "//section/main/div/div/article/div[1]/div/h2"
    if xpath_existence(element) == 1:
        try:
            if browser.find_element_by_xpath(element).text == "This Account is Private" or "Это закрытый аккаунт":
                print(j, "Private account")
                continue
        except StaleElementReferenceException:
            print("Error, code error: 1")

    element = "//section/main/div/header/section/ul/li[3]/a/span"
    if xpath_existence(element) == 0:
        print(j, "Error, code error: 2")
        continue
    status = browser.find_element_by_xpath(element).text
    status = re.sub(r"\s", "", status)
    if int(status) > account_subscriptions:
        print(j, "A lot of subscriptions")
        time.sleep(2)
        continue

    element = "//section/main/div/header/section/div[2]/a"
    if xpath_existence(element) == 1:
        print(j, "There is a link to the website")
        time.sleep(3)
        continue

    element = "//section/main/div/header/section/ul/li[1]/span/span"
    if xpath_existence(element) == 0:
        print(j, "Error, code error: 4")
        time.sleep(3)
        continue
    status = browser.find_element_by_xpath(element).text
    status = re.sub(r'\s', "", status)
    if int(status) < publication:
        print(j, "Account has too few posts")
        time.sleep(3)
        continue

    element = "//section/main/div/header/div/div/span/img"
    if xpath_existence(element) == 0:
        print(j, "Error, code error: 5")
        time.sleep(3)
        continue
    status = browser.find_element_by_xpath(element).get_attribute("src")
    if status.find("s150x150") == -1:
        print(j, "Profile without avatar")
        time.sleep(3)
        continue

    element = "//a[contains(@gref, '/p/')]"
    if xpath_existence(element) == 0:
        print(j, "Error, code error: 6")
        time.sleep(3)
        continue
    status = browser.find_element_by_xpath(element).get_attribute("href")
    browser.get(status)
    post_date = browser.find_element_by_xpath("//time").get_attribute("datetime")
    year = int(post_date[0:4])
    month = int(post_date[5:7])
    day = int(post_date[8:10])
    post_date = datetime(year, month, day)
    period = today - post_date
    if period.days > days:
        print((j, "Last post was many days ago"))
        continue

    filtered_list.append(person)
    print(j, "Add a new user ", person)
    i += 1

f = open(r"C:\Users\Ioann\Documents\django\instagram_bot\filtered_list_users.txt", 'w')
for line in filtered_list:
    f.write(line)
f.close()
print("add", i, "users")

browser.quit()
