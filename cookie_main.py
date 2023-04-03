import time
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


Chrome_Dev_path= "E:\Python Udemy\Day 48\Chrome Dev Tools\chromedriver.exe"
driver=Service(Chrome_Dev_path)
option=webdriver.ChromeOptions()
option.add_experimental_option("detach",True)
browser = webdriver.Chrome(service=driver,options=option)
url="http://orteil.dashnet.org/experiments/cookie/"

browser.get(url)

start_time = time.time()
elapsed_time = time.time() - start_time

END= 5*60
end_start_time = time.time()
end_timeer=time.time() - end_start_time


item_ids = []
item_price=[]

def update_price():
    error=False
    global item_ids,item_price
    item_ids_back=item_ids.copy()
    item_price_back = item_price.copy()
    item_ids.clear()
    item_price.clear()
    price_list = (browser.find_elements(By.CSS_SELECTOR, "#store div b"))
    for x in price_list:
        try:
            if x.text != '':
                temp_id=x.text.split("-")[0].strip()
                temp_price = x.text.split("-")[1]

                if temp_id != 'Alchemy lab' and temp_id != 'Time machine':
                    temp_price=temp_price.replace(',', '').strip()
                    item_ids.append(temp_id)
                    item_price.append(int(temp_price))

        except Exception as e:
            error=True
            item_ids = item_ids_back
            item_price = item_price_back

            #print(f"An error occurred:")



    if error is  False:
        item_ids = item_ids[::-1]
        item_price = item_price[::-1]
        error=False
    #print(item_ids)
    #(item_price)


# item_ids.pop(4)
# item_ids.pop(6)
# item_price.pop(4)
# item_price.pop(6)
update_price()





def buy_item():
    global item_ids
    #("Call Buy Funtion")
    for i in range(len(item_ids)):
        unprocess_score=(browser.find_element(By.CSS_SELECTOR, '#money')).text

        score = int(unprocess_score.replace(',', '').strip())
        while score >= item_price[i]:

            #while score >= item_price[i]:
                try:
                    buy_click = browser.find_element(By.CSS_SELECTOR, f'#buy{item_ids[i]}')
                    buy_click.click()
                    #print(f'Buy {item_ids[i]}')
                    update_price()
                except StaleElementReferenceException:
                    #print("Erorr\n")
                    time.sleep(1)
                    buy_click = browser.find_element(By.CSS_SELECTOR, f'#buy{item_ids[i]}')
                    buy_click.click()
                    update_price()
                finally:
                    unprocess_score = (browser.find_element(By.CSS_SELECTOR, '#money')).text
                    score = int(unprocess_score.replace(',', '').strip())
    #print("end buy\n\n")


while end_timeer<=END:
    elapsed_time = time.time() - start_time
    end_timeer = time.time() - end_start_time
    cookie_click=browser.find_element(By.CSS_SELECTOR,'#cookie')
    cookie_click.click()
    score = (browser.find_element(By.CSS_SELECTOR, '#money')).text



    # print(end_timeer)
    # print(elapsed_time)
    if elapsed_time >= 5:
        buy_item()
        start_time = time.time()
    if end_timeer >= END:
        end_start_time = time.time()


    # print(score)

result=browser.find_element(By.XPATH,'//*[@id="cps"]').text
print(result)