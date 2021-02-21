#!/usr/bin/env python3

from base64 import b64decode
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver import ActionChains
from time import sleep
from wget import download as wget_download
import pyautogui


driver_path = "/usr/bin/chromedriver"
brave_path = "/usr/bin/brave"

def make_page(url, page):
    return ''.join(url[::-1].split("?")[1:])[::-1] + "?page=" + str(page)

class PronoteBot():
    def __init__(self, firefox_profile=None):
        if firefox_profile != None:
            print("[log] Using Firefox Profile : `"+firefox_profile+"`")
            self.driver = webdriver.Firefox(firefox_profile=firefox_profile)
        else:
            self.driver = webdriver.Firefox()
        self.driver.fullscreen_window()

    def start(self, username, password, page_number=None, download=False):
        self.driver.get('https://0752539c.index-education.net/pronote/eleve.html')
        print("[log] Waiting")
        # sleep(100)
        print(f"username : `{username}`")
        title="Saisissez votre identifiant."
        while 1:
            try:
                username_entry = self.driver.find_element_by_css_selector("[title^='"+title+"']")
            except NoSuchElementException:
                sleep(1)
                continue
            break

        print("[log] Writing Username")
        username_entry.send_keys(username)
        print("[log] Writing Password")
        title="Saisissez votre mot de passe."
        self.driver.find_element_by_css_selector("[title^='"+title+"']").send_keys(str(b64decode(password.encode("UTF-8")).decode("UTF-8")))
        print("[log] Clicking on connect")
        title='Cliquez sur le bouton "Se connecter".'
        self.driver.find_element_by_css_selector("[title^='"+title+"']").click()
        sleep(2)

        if page_number != None:
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

        if download:
            # Clicking on Vie Scolaire
            for b in self.driver.find_elements_by_tag_name("div"):
                try:
                    attr_id = b.get_attribute("id")
                except:
                    print("Invalid div, skipping...")
                if attr_id[::-1][:6][::-1] == 'Combo5':
                    print("Found : `"+attr_id+"`")
                    b.click()
                    sleep(1)
                    ActionChains(self.driver).move_to_element_with_offset(b, 200, 0).perform()
                    sleep(1)
                    break

            # Clicking on pdf
            for b in self.driver.find_elements_by_tag_name("i"):
                try:
                    attr_id = b.get_attribute("id")
                except:
                    print("Invalid div, skipping...")
                if attr_id[::-1][:6][::-1] == 'Bouton':
                    print("Found : `"+attr_id+"`")
                    screenWidth, screenHeight = pyautogui.size()
                    pyautogui.moveTo(screenWidth-30, 90)
                    pyautogui.click()
                    sleep(1)
                    break

            # Fill download form
            self.driver.find_elements_by_name("55_1_rbChoixAnnuel")[1].find_element_by_xpath("..").find_elements_by_tag_name("span")[0].click()
            self.driver.find_elements_by_name("55_1_rbPortrait")[1].find_element_by_xpath("..").find_elements_by_tag_name("span")[0].click()
            self.driver.find_elements_by_name("55_1_rbRenvois")[1].find_element_by_xpath("..").find_elements_by_tag_name("span")[0].click()
            sleep(0.5)
            for b in self.driver.find_elements_by_tag_name("button"):
                try:
                    attr_id = b.get_attribute("id")
                except:
                    print("Invalid div, skipping...")
                if attr_id[::-1][:6][::-1] == 'btns_1':
                    print("Found : `"+attr_id+"`")
                    b.click()
                    sleep(1)
                    break

            # Download pdf with direct link
            self.driver.switch_to_window(self.driver.window_handles[1])
            sleep(1)
            current_url = self.driver.current_url
            while current_url == 'about:blank':
                sleep(0.5)
                current_url = self.driver.current_url
                print("Trying current url : `"+current_url+"`")
            print("current url : `"+current_url+"`")
            filename = wget_download(current_url)
            print("\nPdf downloaded at : `"+filename+"`")

