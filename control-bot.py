import os
import time
import telebot
from selenium import webdriver

options = webdriver.ChromeOptions()

options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')

browser = webdriver.Chrome('chromedriver.exe', options=options)
browser.set_window_size(1280,1024)

browser.get('https://accounts.google.com/signin/oauth/identifier?response_type=code&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email&openid.realm&access_type=offline&include_granted_scopes=true&redirect_uri=storagerelay%3A%2F%2Fhttps%2Faccount.habr.com%3Fid%3Dauth356479&client_id=472084966048-ut99mpprfh1n8ees0r26kr1183u1q4r0.apps.googleusercontent.com&ss_domain=https%3A%2F%2Faccount.habr.com&gsiwebsdk=shim&state=40eaf1759c7a851ef3c330f92b5d62a8&o2v=1&as=Sc0bQgml6wT_wcGPs14mkA&flowName=GeneralOAuthFlow')

username = browser.find_element_by_xpath('//input[@type="email"]')
username.send_keys(usernameStr)

nextButton = browser.find_element_by_xpath('//input[@type="submit"]')
nextButton.click()

password = browser.find_element_by_xpath('//input[@type="password"]')
password.send_keys(passwordStr)

signin = browser.find_element_by_xpath('//input[@type="submit"]')
signin.click()

browser.get('https://www.youtube.com/feed/history')

token = '1180587416:AAHVkTo7Tj4B_DfDBV7wWv7Ob3YFLRm2VyE'
bot = telebot.TeleBot(token)

channel_name_path = '//a[@class="yt-simple-endpoint style-scope yt-formatted-string"]'

@bot.message_handler(commands=['start'])
def send_message(message):
    go = True
    while go:

        f = open('forbidden-channels.txt', 'r', encoding='utf-8')
        trash = f.read().split('\n')
        f.close()

        channel_name = browser.find_element_by_xpath(channel_name_path).text
        channel_link = browser.find_element_by_link_text(channel_name).get_attribute("href")
        if channel_name in trash:
            bot.send_message(message.chat.id, channel_name+'\n'+channel_link)

        browser.refresh()
        time.sleep(60)

@bot.message_handler(content_types=['text'])
def add_and_delete_trash(message):
    f = open('forbidden-channels.txt', 'r', encoding='utf-8')
    trash = f.read().split('\n')
    f.close()

    if 'add' in message.text.lower() and message.text.split(' ', 1)[1] not in trash:
        f = open('forbidden-channels.txt', 'a', encoding='utf-8')
        f.write(message.text.split(' ', 1)[1]+'\n')
        f.close()

    elif 'del' in message.text.lower() and message.text.split(' ', 1)[1] in trash:
        f = open('forbidden-channels.txt', 'r', encoding='utf-8')
        content = f.read().split('\n')
        f.close()

        ch = message.text.split(' ', 1)[1]
        if ch in content:
            for i in content:
                if i == ch:
                    del content[content.index(i)]

        f = open('forbidden-channels.txt', 'w', encoding='utf-8')
        f.write('\n'.join(content))
        f.close()

bot.polling()
#browser.quit()
