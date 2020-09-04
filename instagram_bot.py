from selenium import webdriver
import time

browser = webdriver.Chrome(r"C:\Users\Ioann\Documents\django\instagram_bot\chromedriver.exe")
browser.get("http://www.instagram.com")

login = "**********"
password = "*********"

all = 10000

browser.implicitly_wait(5)
browser.get("http://www.instagram.com/accounts/login")

browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(
    login)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(
    password)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]").click()
time.sleep(5)

browser.get("https://www.instagram.com/minsk_news/")
time.sleep(5)
browser.find_element_by_xpath("//section/main/div/header/section/ul/li[2]/a").click()
time.sleep(4)
element = browser.find_element_by_xpath("/html/body/div[4]/div/div[2]")

browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 6, element)
time.sleep(1.2)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 4, element)
time.sleep(1.1)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 3, element)
time.sleep(1)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 2, element)
time.sleep(1.5)
browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight/%s" % 1.4, element)
time.sleep(1)

persons = []
t = 0.9
num_scroll = 0
p = 0

while len(persons) < all:
    num_scroll += 1
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)

    if num_scroll % 10 == 0:
        print("!")

        count_persons = browser.find_elements_by_xpath(
            "//div[@role='dialog']/div[2]/ul/div/li/div/div/div/div/a[@title]")
        for i in range(len(count_persons)):
            persons.append(str(count_persons[i].get_attribute('href')))
    time.sleep(t)

    if len(persons) > (2000 + 1000 * p):
        print("\nWaiting ... 10 minuts")
        time.sleep(600)
        p += 1

f = open(r"C:\Users\Ioann\Documents\django\instagram_bot\persons_list.txt", 'w')
for person in persons:
    f.write(person)
    f.write("\n")
f.close()

browser.quit()
