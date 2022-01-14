username =         # add your username (nitc mail id) here
password =         # no worries, its safe here, enter password 

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time 
import sys

browser = webdriver.Firefox()

#compare present time to upper and lower limits of attendnace
def time_in_range(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

#wait for 10 sec after each click, due to our lagserver!

strt_time = datetime.now()
browser.get('https://eduserver.nitc.ac.in/')
username = browser.find_element_by_id("username").send_keys(username)
password = browser.find_element_by_id("password").send_keys(password)
browser.find_element_by_xpath ("//button[contains(text( ), 'Log in')]").click()
browser.implicitly_wait(10)
calendar = browser.find_element_by_xpath("//*[@id='inst16319']")
attendance = calendar.find_elements_by_xpath ("//a[contains(text( ), 'Attendance')]/parent::*")
flag =0
nearest = datetime(2020, 1, 1)

while flag==0:
	# go through all and find an attendance that can be marked at present
	for i in attendance:
		timerow = i.find_element_by_class_name('date')
		timerow = timerow.text.split( )
		#only look for today's attendance
		if timerow[0] != 'Today,':
			continue
		upper = timerow[1]+' '+timerow[2]
		upper = datetime.strptime(upper, '%I:%M %p')
		upper = datetime.now().replace(hour=upper.hour, minute = upper.minute)
		if abs(nearest-datetime.now()) > abs(upper-datetime.now()):
			nearest = upper
		lower = upper + timedelta(minutes=30)
		# if there is attendance to be marked (within 30 mins of starting of attendance), mark attendance
		if time_in_range(upper, lower, datetime.now()):
			i.find_element_by_xpath (".//a[contains(text( ), 'Attendance')]").click()
			WebDriverWait(browser, 1000000).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text( ), 'Go to activity')]"))).click()
			#WebDriverWait(browser, 10).until(browser.find_element_by_xpath ("//a[contains(text( ), 'Go to activity')]"))
			#browser.implicitly_wait(20)
			#browser.find_element_by_xpath (".//a[contains(text( ), 'Go to activity')]").click()
			browser.implicitly_wait(20)
			browser.find_element_by_xpath ("//a[contains(text( ), 'Submit attendance')]").click()
			browser.implicitly_wait(20)
			attendance_box = browser.find_element_by_xpath ("/html/body/div[1]/div[3]/div/div[3]/div/section/div/form/fieldset/div/div/div[2]/fieldset/div")
			attendance_one = attendance_box.find_element_by_xpath (".//input").click()
			browser.implicitly_wait(20)
			submit_button = browser.find_element_by_xpath ("//input[@value='Save changes']").click()
			browser.implicitly_wait(20)
			flag =1
			browser.implicitly_wait(20)
			browser.close()
	#end script after trying for 10 minutes maximum or if there is no attendance to mark in 45 mins
	if datetime.now()-strt_time > timedelta(minutes=10) or abs(nearest-datetime.now())>timedelta(minutes=45):
		browser.close()
		sys.exit()
	#wait for 1 min if there is no attendance to be marked at present, and try again
	elif flag==0:
		print('waiting')
		time.sleep(60)
			
sys.exit()
			
			
			


		
		
		






	


