#!/usr/bin/env python3

from base64 import b64decode
from selenium import webdriver
from time import sleep

driver_path = "/usr/bin/chromedriver"
brave_path = "/usr/bin/brave"

def make_page(url, page):
    return ''.join(url[::-1].split("?")[1:])[::-1] + "?page=" + str(page)

class PronoteBot():
    def __init__(self):
        self.driver = webdriver.Firefox(firefox_profile='/home/scott/.mozilla/firefox/hrgxfoc4.default-release')
        self.driver.fullscreen_window()

    def start(self, page_number, username, password):
        self.driver.get('https://0752539c.index-education.net/pronote/eleve.html')

        sleep(1)

        print("[log] Writing Username")
        title="Saisissez votre identifiant."
        self.driver.find_element_by_css_selector("[title^='"+title+"']").send_keys(username)
        print("[log] Writing Password")
        title="Saisissez votre mot de passe."
        self.driver.find_element_by_css_selector("[title^='"+title+"']").send_keys(str(b64decode(password.encode("UTF-8")).decode("UTF-8")))
        print("[log] Clicking on connect")
        title='Cliquez sur le bouton "Se connecter".'
        self.driver.find_element_by_css_selector("[title^='"+title+"']").click()

        if page_number != None:
            sleep(2)
            # Connected to pronote
            print("[log] Clicking on physique-chimie book")
            content='Physique chimie 1re, éd. 2019 - Manuel numérique PREMIUM élève'
            script = self.driver.find_element_by_xpath("//span[.='"+content+"']").find_element_by_xpath("../..").get_attribute("onclick")
            print("Opening educhadoc window with script : `"+script+"`")
            self.driver.execute_script(script)

            sleep(8)

            # Switch to educadhoc tab
            tabs = self.driver.window_handles
            # self.driver.switch_to.window(tabs[0])
            # self.driver.close()
            self.driver.switch_to.window(tabs[1])

            sleep(4)
            # Educhadoc opened
            current_url = self.driver.current_url
            print("current url : `"+current_url+"`")
            page = make_page(current_url, page_number)
            if page != current_url:
                print("Going to page : `"+page+"`")
                self.driver.get(page)
                # self.driver.execute_script('window.open("'+page+'")')

            # sleep(3)
            # # Clicking on download button
            # for b in self.driver.find_elements_by_tag_name("button"):
            #     if ("oneclick" in b.get_attribute("class")):
            #         print(b.get_attribute("class"))
            #         b.click()
            #         break

