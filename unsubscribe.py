from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

login = "**********"
password = "*********"

unsubscribe_time = 3
count_unsubscribe = 20

browser = webdriver.Chrome(r"C:\Users\Ioann\Documents\django\instagram_bot\chromedriver.exe")


def xpath_existence(url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence


browser.get("http://www.instagram.com/accounts/login")
time.sleep(3)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(
    login)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(
    password)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]").click()
time.sleep(5)

file_list = []
f = open(r"C:\Users\Ioann\Documents\django\instagram_bot\my_subscribtions.txt", 'r')
for line in f:
    file_list.append(line)
f.close()

i = 0
for line in file_list:
    i += 1
    if i == count_unsubscribe + 1:
        break
    browser.get(line)
    element = "//div[1]/div[2]/span/span[1]/button"
    if xpath_existence(element) == 0:
        print("Error 1: button search error")
        continue
    try:
        button = browser.find_element_by_xpath(element)
    except StaleElementReferenceException:
        print("Error 2: button search error")
        continue

    status = browser.find_element_by_xpath(element).get_attribute("aria_label")
    if status.find("Подписки") == 1:
        try:
            button.click()
        except StaleElementReferenceException:
            print("Error 3: button search error")
            continue

    time.sleep(1)
    element = "//body/div[4]/div/div/div[3]/button[1]"
    if xpath_existence(element) == 0:
        print("Error 4: button search error ")
        continue
    button = browser.find_element_by_xpath(element)
    try:
        button.click()
    except StaleElementReferenceException:
        print("Error 5: push-button")
        continue
    print("Unsubscribe from ", line)
    time.sleep(unsubscribe_time)

f = open(r"C:\Users\Ioann\Documents\django\instagram_bot\my_subscribtions.txt", 'w')
i = 0
for i in range(count_unsubscribe, len(file_list)):
    f.write(file_list[i])
    i += 1
f.close()

browser.quit()