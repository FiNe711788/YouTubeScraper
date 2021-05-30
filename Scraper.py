import time
import json
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

site = 'https://www.youtube.com/c/StevetheBartenderAUS/videos'
browser = webdriver.Chrome()
browser.get(site)
time.sleep(20)

# imgs = browser.find_elements_by_xpath('//div[@id="primary"]//div[@id="items"]//*[@id="thumbnail"]//*[@id="img"]')
# for i, img in enumerate(imgs):
#     src = img.get_attribute('src')
#     if not src:
#         ActionChains(browser).key_down(Keys.PAGE_DOWN).perform()
#         time.sleep(1)
#         src = img.get_attribute('src')
#     urlretrieve(src, "cocktails\\" + str(i + 1) + ".png")

data = {}
# data['Ingredient'] = []
with open('data.txt') as f:
    data = json.load(f)

links = browser.find_elements_by_xpath('//*[@id="thumbnail"]')
for i, link in enumerate(links):
    if (i < 444):
        continue
    try:
        ActionChains(browser).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
    except:
        time.sleep(1)
        ActionChains(browser).key_down(Keys.CONTROL).click(link).key_up(Keys.CONTROL).perform()
    handles = browser.window_handles
    browser.switch_to_window(handles[1])
    url = browser.current_url

    time.sleep(3)
    title = browser.find_element_by_xpath('//div[@id="columns"]//div[@id="primary-inner"]//div[@id="info"]//div[@id="info-contents"]//div[@id="container"]//h1[@class="title style-scope ytd-video-primary-info-renderer"]//*[@class="style-scope ytd-video-primary-info-renderer"]').text
    time.sleep(1)
    try:
        expand = browser.find_element_by_xpath('//div[@id="columns"]//div[@id="primary-inner"]//div[@id="meta-contents"]//*[@id="more"]').click()
    except:
        print("No element found")
    spans = browser.find_elements_by_xpath('//div[@id="columns"]//div[@id="primary-inner"]//div[@id="meta-contents"]//*[@class="content style-scope ytd-video-secondary-info-renderer"]//span')
    time.sleep(1)
    description = ""
    for span in enumerate(spans):
        text = span[1].text
        description += text + "\n"
    time.sleep(3)

    ActionChains(browser).key_down(Keys.CONTROL).send_keys("w").key_up(Keys.CONTROL).perform()
    browser.close()
    browser.switch_to_window(handles[0])
    time.sleep(1)

    data['Ingredient'].append({
        'id': str(i + 1),
        'url': url,
        'title': title,
        'description': description
    })
    datafile = open('data.txt', 'w')
    datafile.write(json.dumps(data, sort_keys=True, indent=4))
    if (i == 509):
        break

datafile = open('data.txt', 'w')
datafile.write(json.dumps(data, sort_keys=True, indent=4))

browser.close()