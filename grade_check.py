import webbrowser
import requests
import selenium
import os
from selenium import webdriver
from selenium.webdriver import Chrome


def main():
    get_grades()
    # global webdriver
    # webdriver = selenium.webdriver
    # download_file("https://sisstudent.fcps.edu/")
    # grade book: https://sisstudent.fcps.edu/SVUE/PXP_Gradebook.aspx?AGU=0


def get_grades():
    driver = webdriver.Safari()
    driver.get('https://sisstudent.fcps.edu/')
    id_box = driver.find_element_by_name('username')
    id_box.send_keys('1442687')
    pass_box = driver.find_element_by_name('password')
    pass_box.send_keys('Jeremiah2911')
    login_button = driver.find_element_by_name('Submit1')
    login_button.click()
    # navigator = driver.find_element_by_name('sidenav')
    side_bar = driver.find_element_by_xpath("/html/body/form[1]/div[2]/table[1]/tbody/tr/td[0]/div/ul/li[5]")
    # side_bar = driver.find_element_by_xpath("//form[1]")
    # side_bar = driver.find_element_by_xpath("//form[@id='Form1']")
    # grade_book = driver.find_element_by_xpath("//form[input/@name='username']")
    # grade_book = driver.find_element_by_xpath("//form[@id='loginForm']/input[1]")
    # grade_book = driver.find_element_by_xpath("//input[@name='username']")
    # grade_book = driver.find_element_by_xpath("//a[@href='Grade Book']")
    # grade_book = driver.find_element_by_link_text('Grade Book')
    side_bar.click()
    # driver.get('https://sisstudent.fcps.edu/SVUE/PXP_Gradebook.aspx?AGU=0')
    period_1 = driver.find_element_by_link_text('1')
    period_1.click()



def download_file(download_url):
    #webbrowser.open('http://inventwithpython.com/')
    res = requests.get(download_url, auth=('1442687', 'Jeremiah2911'))
    print(type(res))
    res.raise_for_status()
    file = open('sis_2.txt', 'wb')
    for chunk in res.iter_content(100000):
        file.write(chunk)
    file.close()



if __name__ == "__main__":
    main()