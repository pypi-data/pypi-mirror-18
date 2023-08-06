#!/usr/bin/env python
from bs4 import BeautifulSoup
from os import path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep,time
from pync import Notifier 

def beginchat():
    print "Loading "

    driver_wa = webdriver.Chrome()
    driver_wa.get('https://web.whatsapp.com/')

    driver_bot = webdriver.PhantomJS(service_log_path=path.devnull)
    driver_bot.set_window_size(1280, 1024)
    driver_bot.get('http://www.cleverbot.com/')

    clever_bot_input = driver_bot.find_element_by_class_name('stimulus')

    raw_input("Ready?")

    driver_box = driver_wa.find_element_by_xpath('.//div[@class = "input"]')


    pre_cont = ""
    cont = ""
    content = ""




    while content != "exit()":
	    url = driver_wa.page_source
	    soup = BeautifulSoup(url,"html.parser")
	    post_content = soup.findAll('span',{'class' : 'emojitext selectable-text'})

	    last_div = None
	    for last_div in post_content:
		    pass
	    if last_div:
		    content = last_div.getText()

	    if content == pre_cont:
		    flag = False
	    else:
		    pre_cont = content
		    flag = True
    	


	    if flag:
		    clever_bot_input.send_keys(content)
		    clever_bot_input.send_keys(Keys.RETURN)
		    sleep(3)
		    for elem in driver_bot.find_elements_by_xpath('.//span[@class = "bot"]'):
			    cont = elem.text
		    pre_cont = cont
		    notif_mess = cont
		#send_notifications(notif_mess,"Suggestions")
		    driver_box.send_keys(cont)
		    driver_box.send_keys(Keys.RETURN)

		

	    sleep(10)

    driver_bot.quit()
    driver_wa.quit()

    print "\nChat ended"
