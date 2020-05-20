from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
from download_folder import download_path
import os

class Downloader():
    def __init__(self, choice):

        self.choice = choice
        self.file_path = download_path() 
        self.titles = []
        self.video_url = ''
        self.browser_name = ''

        # Firefox Options
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
        from selenium.webdriver.firefox.options import Options
        self.profile = webdriver.FirefoxProfile()
        self.profile.set_preference("browser.download.manager.showWhenStarting", False)
        self.profile.set_preference("browser.download.manager.showAlertOnComplete", False)
        self.profile.set_preference("media.volume_scale", "0.0")
        self.profile.set_preference("browser.download.dir", self.file_path)
        if choice == 'mp3':
            self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/mpeg")
        elif choice == 'mp4':
            self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "video/mp4");
        self.firefox_options = Options()
        self.firefox_options.set_headless()
        assert self.firefox_options.headless
        self.firefox_options.add_argument('disable-gpu')
        self.firefox_options.set_preference("dom.webnotifications.enabled", False)

        # Chrome Options
        from selenium.webdriver.chrome.options import Options
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.file_path,
            "download.prompt_for_download": False,
        })
        self.chrome_options.add_argument("headless")
        self.chrome_options.add_argument('disable-gpu')
        self.chrome_options.add_argument('--disable-extensions')
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);

        try:
            self.browser = webdriver.Firefox(executable_path = os.getcwd() + "\\Drivers\\geckodriver.exe", firefox_profile = self.profile, options = self.firefox_options)
            self.browser_name = 'Firefox'
        except:
            try:
                self.browser = webdriver.Chrome(executable_path = os.getcwd() + "\\Drivers\\80\\chromedriver.exe", chrome_options = self.chrome_options)
                self.browser_name = 'Chrome'
            except:
                try:
                    self.browser = webdriver.Chrome(executable_path = os.getcwd() + "\\Drivers\\79\\chromedriver.exe", chrome_options = self.chrome_options)
                    self.browser_name = 'Chrome'
                except:
                    print("Problem with browser")

    def launch_youtube(self):
        url = 'https://youtube.com'
        connected = False
        while not connected:
            try:
                self.browser.get(url)
                connected = True
            except:
                time.sleep(1)

    def search_youtube(self, string):
        connected = False
        while not connected:
            try:
                box = self.browser.find_element_by_name('search_query')
                connected = True
            except:
                time.sleep(1)
        box.send_keys(string)
        time.sleep(2)

        connected = False
        while not connected:
            try:
                button = self.browser.find_element_by_id('search-icon-legacy')
                connected = True
            except:
                time.sleep(1)
        button.click()
        time.sleep(2)

        self.browser.get(self.browser.current_url)
        time.sleep(2)

    def get_titles(self):
        connected = False
        while not connected:
            try:
                titles = self.browser.find_elements_by_xpath('//*[@id="video-title"]')
                connected = True
            except:
                time.sleep(1)
        i = 0
        for title in titles:
            name = title.get_attribute('title')
            # Unicode Protection
            for char in name:
                if (ord(char) > 65536):
                    name = ''

            self.titles.append(name)
            if (i == 4):
                break
            i += 1

    def find_video(self, path):
        connected = False
        while not connected:
            try:
                video = self.browser.find_element_by_xpath(path)
                video.click()
                connected = True
            except:
                time.sleep(2)
        self.video_url = self.browser.current_url


    def launch_downloader(self):
        url = 'https://ytmp3.cc/en13/'
        connected = False
        while not connected:
            try:
                self.browser.get(url)
                connected = True
            except:
                time.sleep(2)


    def download(self):
        if (self.choice == 'mp3'):
            mp3 = self.browser.find_element_by_xpath('//*[@id="mp3"]')
            mp3.click()
            time.sleep(2)
        elif (self.choice == 'mp4'):
            mp4 = self.browser.find_element_by_xpath('//*[@id="mp4"]')
            mp4.click()
            time.sleep(2)
        
        connected = False
        while not connected:
            try:
                search = self.browser.find_element_by_id('input')
                search.send_keys(self.video_url)
                time.sleep(2)
                button = self.browser.find_element_by_id('submit')
                button.click()
                connected = True
            except:
                time.sleep(2)

        connected = False
        while not connected:
            try:
                download = self.browser.find_element_by_link_text('Download')
                connected = True
            except:
                time.sleep(2)
        download.click()
        print('Downloading...')
        time.sleep(2)

        # Download time

        if self.browser_name == 'Firefox':
            word = ".part"
        else:
            word = ".crdownload"

        import os

        entries = os.listdir(self.file_path)

        while True:
            val = True
            for entry in entries:
                if word in entry:
                    val = False
                    time.sleep(2)
            if val:
                break

            entries = os.listdir(self.file_path)


    def close(self):
        print('Download Finished!')
        self.browser.quit()
