import os
import re
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def open_poems(nb_poems, author_dir):
    """ Opens each link towards a poem and create a new file for each """
    for i in range(nb_poems):
        try:
            link = driver.find_elements(By.CSS_SELECTOR, 'td.title > a')[i]
        except:
            continue

        print(i, link.get_attribute("href"))
        
        link.click()

        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.select(".KonaBody p")
        raw_title = soup.find('h1').get_text()
        title = re.sub(' - .*', '', raw_title)

        raw_html_poem = ''.join(str(results)).split('<br/>')
        cleaner_poem = [i.strip() for i in raw_html_poem]
        write_poem(cleaner_poem, title, author_dir)
        driver.execute_script("window.history.go(-1)")
        driver.implicitly_wait(1)


def write_poem(cleaner_poem, title, author_dir):
    """ Write poem into a file, removing html tags and indents """

    write_raw_poem(cleaner_poem, author_dir, title)

    with open(os.path.join(author_dir, title + '.txt'), 'r+', 
                    encoding='utf-8') as poem:
            content = poem.readlines()
            poem.seek(0)
            
            for line in content: 
                if '[<p>' in line:
                    new_line = line.replace('[<p>', '')

                    if not new_line.isspace():
                        poem.write(new_line)

                elif '</p>]' in line: 
                    new_line = line.replace('</p>]', '')
                    
                    if not new_line.isspace():
                        poem.write(new_line)

                elif line == content[-2]:
                    poem.write(line.rstrip())

                elif line == content[1]:
                    poem.write(line.lstrip())

                else:
                    poem.write(line)
            poem.truncate()


def write_raw_poem(cleaner_poem, author_dir, title):
    """ Write the poem a first time, leaving the remaining html tags
    and indents"""
    with open(os.path.join(author_dir, title + '.txt'), 'w', 
                    encoding='utf-8') as file:
        for line in cleaner_poem:
            file.write(line + '\n')


if __name__ == "__main__":
    with open('./urls.txt', 'r', encoding='utf-8') as file:
        urls = file.readlines()
        
    for url in urls:
        author = re.search('(?<=.com/).*(?=/poems)', url)
        author_dir = os.path.join('./corpus/'+
                    author.group(0).replace('-', '_'))

        if not os.path.exists(author_dir):
            os.makedirs(author_dir)

        # disable image loading
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so',
                    'false')

        # set the browser as headless 
        firefox_options = Options()
        firefox_options.add_argument('-headless')
            
        driver = webdriver.Firefox(firefox_profile=firefox_profile, firefox_options=firefox_options)

        try: 
            driver.get(url)
        except requests.exceptions.RequestException as err:
            print(err)
        else: 
            nb_pages = len(driver.find_elements(By.XPATH, 
                        '//div[@class="pagination mb-15"]/ul/li'))

            for i in range(1, nb_pages):
                new_url = url + 'page-' + str(i)
                driver.get(new_url)

                nb_poems = len(driver.find_elements(By.XPATH,
                        '//td[@class="title"]'))

                open_poems(nb_poems, author_dir)
            driver.quit()