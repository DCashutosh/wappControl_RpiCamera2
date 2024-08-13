from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config as Config

class Wapp_apps:
    
    #whatsapp-sender-user(controller)
    user = None
    driver = None
    msg_count = 1

    def __init__(self,user,driver):
        self.user = user
        self.driver = driver

    def search_contact(self):

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH,Config.contact_search))
        )

        # Search for the contact
        search_box = self.driver.find_element(By.XPATH, Config.contact_search)
        search_box.click()
        search_box.send_keys(self.user)
        search_box.send_keys(Keys.ENTER)
    
    def click_chat(self):
            
        # Find and click on the chat
        #used CSS selector as XPATH was not working
        title = "span[title='"+self.user+"']"
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, title))
        )
        chat = self.driver.find_element(By.CSS_SELECTOR, title)
        chat.click()


    def send_msg(self, message):

        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH,Config.message_box))
        )

        # Locate the message input box
        message_box = self.driver.find_element(By.XPATH, Config.message_box)
        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
    
    def read_msg(self):
        try:
            # Wait for messages to load
            time.sleep(2)
            
            # Get the last 'message_count' messages
            messages = self.driver.find_elements(By.CSS_SELECTOR, "span.selectable-text")
            latest_messages = [msg.text for msg in messages[-self.msg_count:]]
            
            return latest_messages
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def send_file(self,file_path):

        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH,Config.attach_file))
        )
        attach_btn = self.driver.find_element(By.XPATH, Config.attach_file)
        attach_btn.click()

        #select file type
        # WebDriverWait(self.driver, 30).until(
        #     EC.presence_of_element_located((By.XPATH, Config.select_file))
        # )
        # select_file = self.driver.find_element(By.XPATH,Config.select_file)

        # Wait for the file input to appear and upload the file
        file_input = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(file_path)

        # Wait for the send button to appear and click it
        send_btn = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, Config.file_send))
        )
        send_btn.click()
        

