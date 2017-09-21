#!/usr/bin/python3
from selenium import webdriver
import requests
import time
browser = webdriver.Firefox()
browser.get('http://10.10.1.27:8090/')
time.sleep(3)
if browser.current_url == 'http://10.10.1.27:8090/login?from=%2F':
	browser.find_element_by_xpath('//*[@id="j_username"]').send_keys('admin')
	browser.find_element_by_xpath('//*[@id="main-panel"]/div/form/table/tbody/tr[2]/td[2]/input').send_keys('admin')
	browser.find_element_by_xpath('//*[@id="yui-gen1-button"]').click()
else:
	pass
time.sleep(3)
browser.find_element_by_xpath('//*[@id="job_Build_YL50B71"]/td[3]/a').click()
time.sleep(2)
browser.find_element_by_xpath('//*[@id="tasks"]/div[6]/a[2]').click()
