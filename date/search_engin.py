from os import write
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import json
# from date.urls import list_urls
import time
# EXE_PATH это путь до ранее загруженного нами файла chromedriver.exe


class Search:
    def __init__(self):
        EXE_PATH = r'C:/temp/chromedriver.exe'
        send_command = ('POST', '/session/$sessionId/chromium/send_command')
        self.driver = webdriver.Chrome(executable_path=EXE_PATH)
        # self.driver = webdriver.Chrome()
        self.driver.set_window_size(1400, 1500)
        self.driver.command_executor._commands['SEND_COMMAND'] = send_command
        # time.sleep(200)
        # self.driver.execute('SEND_COMMAND', dict(cmd='Network.clearBrowserCookies', params={}))

    def search_yandex(self, url_list):
        results_name_sites = {
            url_list['name']: {
                'good': {},
                'bad': {}
            }
        }
        for urls in url_list['urls']:
            self.driver.execute('SEND_COMMAND', dict(
                cmd='Network.clearBrowserCookies', params={}))
            urls = urls.replace(' ', '+')
            if 'ереповец' not in urls:
                url = f'https://yandex.ru/search/?text={urls}+череповец'
            else:
                url = f'https://yandex.ru/search/?text={urls}'
            self.driver.get(url)
            res = self.driver.find_elements_by_class_name('organic__subtitle')
            print(len(res))
            list_cheker_urls = []
            for i in res[0:4]:
                try:
                    name_sites = i.find_element_by_tag_name('b').text
                except NoSuchElementException:
                    print(name_sites)
                list_cheker_urls.append(name_sites)
            # print(url)
            # print(list_cheker_urls)
            # for ind in url_list['top']:
                # print(ind)
            if list_cheker_urls[0] not in url_list['top'][0]:
                results_name_sites[url_list['name']
                                   ]['bad'][url] = list_cheker_urls
                self.driver.save_screenshot(f'screenshot/{urls}.png')
            else:
                # self.driver.save_screenshot(f'screenshot/{urls}.png')
                results_name_sites[url_list['name']
                                   ]['good'][url] = list_cheker_urls
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results_name_sites, f, ensure_ascii=False, indent=4)

    def search_google(self, list_urls):
        for url in list_urls['urls']:
            list_cheker_urls = []
            # url = url.replace("+", ' ').split().replace(' ', '+')
            url = url.replace(" ", '')
            if url[0] == "+":
                url = url[1::]
            if 'ереповец' not in url:
                url = url + '+череповец'
            # print(url)

            res_url = f'https://www.google.com/search?q={url}'
            self.driver.execute('SEND_COMMAND', dict(
                    cmd='Network.clearBrowserCookies', params={}))
            self.driver.get(res_url)
            reklama = self.driver.find_element_by_id('taw')
            if reklama:
                res = self.driver.find_element_by_xpath("//span[@role='text']").text
                list_cheker_urls.append(res)
            res = self.driver.find_elements_by_tag_name('cite')
            for i in res:
                list_cheker_urls.append(i.text)
            list_cheker_urls = [i for i in list_cheker_urls if i != '']
            # print(url)
            # print(list_cheker_urls)
            flag = False
            for i in list_urls['top'][0]:
                if i not in list_cheker_urls[0]:
                    pass
                else:
                    flag = True
            if flag == False:
                self.driver.save_screenshot(f'screenshot/{url}.png')
                print(f"{res_url} Запрос не соотвецтвует требованиям")

        # time.sleep(200)

    def close_driver(self):
        self.driver.close()
