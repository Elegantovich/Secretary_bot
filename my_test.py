from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome('C:/Dev/my_test/chromedriver')
driver.get('http://qa-assignment.oblakogroup.ru/board/9113002017')
driver.find_element_by_id('add_new_todo').click()
select = Select(driver.find_element_by_id('select_category'))
select.select_by_visible_text('Прочее')
textt = driver.find_element_by_id('project_text')
textt.send_keys(Keys.CONTROL, 'a')
textt.send_keys('Масло')
ok = driver.find_element_by_id('submit_add_todo')
ok.click()


""""
block = driver.find_element_by_id('project_text').send_keys('привет')
driver.find_element_by_id('submit_add_todo').click()

block.send_keys('привет')
print(block)"""
