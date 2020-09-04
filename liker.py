import random
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException

random.seed()

login = "*******"
password = "*********"

like_time = 10
all_likes = 600
all_subscriptions = 130
hour_like = 40
hour_subscription = 20
random_sleep = random.randint(2, 20)
likes = 0
subscriptions = 0


def xpath_existence(url):
    try:
        browser.find_element_by_xpath(url)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence


browser = webdriver.Chrome(r"C:\Users\Ioann\Documents\django\instagram_bot\chromedriver.exe")

browser.get("http://www.instagram.com/accounts/login")
time.sleep(10)

browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(
    login)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(
    password)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]").click()
time.sleep(5)

f = open(r"C:\Users\Ioann\Documents\django\instagram_bot\\filtered_list_users.txt", 'r')
file_list = []
for line in f:
    file_list.append(line)
f.close()

subscription_list = []
f1 = open(r"C:\Users\Ioann\Documents\django\instagram_bot\my_subscribtions.txt", 'r')
for line in f1:
    subscription_list.append(line)
f1.close()

j = 0
n = 0
next_person = 0
start_time = time.time()

for person in file_list:
    if likes >= all_likes:
        print("Like limit reached")
        break
    if subscriptions >= all_subscriptions:
        print("Like limit reached")
        break

    if time.time() - start_time <= 3600 and hour_subscription <= subscriptions:
        print("Subscription limit per hour reached")
        print("Wait...", int(3600 - (time.time() - start_time / 60)), "min")

        f = open(r"C:\Users\Ioann\Documents\django\instagram_bot\\filtered_list_users.txt")
        for i in range(j, len(file_list)):
            f.write(file_list[i])
        f.close()

        time.sleep(3600 - (time.time() - start_time))
        start_time = time.time()
        subscriptions = 0
        likes = 0

    if time.time() - start_time <= 3600 and hour_like <= likes:
        print("Like limit per hour reached")
        print("Wait ", int(3600 - (time.time() - start_time / 60)), "min")

        f = open(r"C:\Users\Ioann\Documents\django\instagram_bot\\filtered_list_users.txt")
        for i in range(j, len(file_list)):
            f.write(file_list[i])
        f.close()

        time.sleep(3600 - (time.time() - start_time))
        start_time = time.time()
        subscriptions = 0
        likes = 0

    if time.time() - start_time >= 3600:
        start_time = time.time()
        subscriptions = 0
        likes = 0

    for line in subscription_list:
        next_person = 0
        if person == line:
            next_person = 1
            print(j + 1, "\tAlready subscribed to this person")
            j += 1
            n += 1
            break
    if next_person == 1:
        continue

    j += 1
    print("\n" + str(j - n) + ": ")

    browser.get(person)
    time.sleep(random_sleep)

    element = "//section/main/div/header/section/div[1]/div[1]/span/span[1]/button"
    if xpath_existence(element) == 1:
        try:
            follow_status = browser.find_element_by_xpath(element).text
        except StaleElementReferenceException:
            print(j, "Error, code error: 1.0")
            continue
        if follow_status == "Following" or follow_status == "Подписки":
            print("Already subscribed to this person\n")
            continue

        element = "//a[contains(@href, '/p/')]"
        if xpath_existence(element) == 0:
            print(j, "Error, code error: 1.1")
            continue
        posts = browser.find_elements_by_xpath(element)
        i = 0
        for post in posts:
            posts[i] = post.get_attribute("href")
            i += 1
        rand_post = random.randint(0, 5)
        for i in range(2):
            browser.get(posts[rand_post + i])
            time.sleep(1)
            browser.find_element_by_xpath(
                "//section/main/div/div/article/div[2]/section[1]/span[1]/button").click()
            likes += 1
            print("+1 like")
            time.sleep(like_time)

        try:
            element = "//section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button"
            if xpath_existence(element) == 0:
                print(j, "Error, code error: 2.0")
            try:
                browser.find_element_by_xpath(element).click()
            except StaleElementReferenceException:
                print(j, "Error, code error: 2.1")
                continue
        except ElementClickInterceptedException:
            print(j, "Error, code error: 2.2")
            continue

        subscriptions += 1
        print("+1 Subscription", person[0:len(person) - 1])
        time.sleep(random_sleep)

        f = open(r"C:\Users\Ioann\Documents\django\instagram_bot\my_subscribtions.txt", 'a')
        f.write(person)
        f.close()

f = open(r"C:\Users\Ioann\Documents\django\instagram_bot\my_subscribtions.txt", 'w')
for i in range(j, len(file_list)):
    f.write(file_list[i])
f.close()

browser.quit()
