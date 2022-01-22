#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

import time
import subprocess
import requests
from bs4 import BeautifulSoup
import os
import re

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from rich import print
from rich import box
from rich.progress import track
from rich.console import Console
from rich.table import Table

def clear_screen():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix': 
        _ = os.system('clear')
   else: # for windows platfrom
        _ = os.system('cls')

class Course():
    def __init__(self, course_name, user, passwd, args):
        
        self.course_name = re.sub('http.*://.*?/.*?/','', course_name)
        self.course_url = f"https://maktabkhooneh.org/course/{self.course_name}"
        self.user = user
        self.passwd = passwd
        self.driver = None
        self.chapter_urls = []  # url for each chapters
        self.chapter_titles = [] # title of each chapters
        self.chapter_downloadlinks = []  # download link of the chapter's video
        self.exclude_list = set()  # saves the list of lessons to be included
        self.args = args

    def extract(self):
        self._showChapters()
        self.driver = Firefox()
        self.driver.get(self.course_url)
        self._login()
        self._getChapters()  # gets chapters of the course
        self._getExclusion()  # sets the exclude list
        self._getChapterLinks()  # makes the download urls of the inlcluded lesson(s)
        if not self.args.axel:
            self._saveChapterLinks()
        else:
            self._saveChapterVideos()
        return self.chapter_downloadlinks

    def _showChapters(self):
        page = requests.get(self.course_url)
        if page.status_code != 200:
            print(f'[red] Course {self.course_url} was not found.[/red]')
            exit()
        soup = BeautifulSoup(page.text, 'html.parser')
        chapters = [ item.get_text().replace('\n','').split('"')[0].strip() 
                    for item in soup.find_all('a',class_='chapter__unit') ]
        self._tablular(chapters[:len(chapters)//2])
        print('Be Patient ...', end='')


    def _getExclusion(self):
        getRange = lambda x: set(range(int(x), int(x) + 1) if len(x.split('-')) == 1 
                        else range(int(x.split('-')[0]), int(x.split('-')[1]) + 1))
        if not self.args.interactive: return  # there would be no exclusion
        print(
            '==> Press the Enter key to download all lessons, Type `end` to exit the application.',
            '    Lesson(s) to exclude: (e.g.: "1 2 3", "1-3", "^4"),',
            sep='\n', end=' ' 
        )
        lineInput = input("==> ").strip().lower()
        if lineInput == 'end': exit()
        exc = set(lineInput.strip().lower().split())
        if exc == set(): 
            return  # there would be no exclusion
        for item in exc:
            if item[0]=='^': self.exclude_list.update(getRange(item[1:]))
        self.exclude_list = set(range(1, len(self.chapter_urls) + 1)).difference(self.exclude_list)
        for item in exc: 
            if item[0]!='^': self.exclude_list.update(getRange(item))

    def _login(self):
        submit = self.driver.find_element(By.CLASS_NAME, 'button')
        submit.click()
        elem = self.driver.find_element(By.NAME, 'tessera')
        elem.send_keys(self.user)
        elem.send_keys(Keys.ENTER)
        time.sleep(2)
        elem = self.driver.find_element(By.NAME, 'password')
        elem.send_keys(self.passwd)
        elem.send_keys(Keys.ENTER)
        time.sleep(3)

    def _tablular(self, data, header=True, reverse=False):
        Console().print()
        table = Table(show_header=header, header_style='bold', 
                    row_styles=["none", "dim"], box=box.DOUBLE,)
        for col,style,justify in zip( ('Description', 'Lesson'), ('green', 'bold cyan'), ('right', 'center') ):
            table.add_column(f"[{style}]{col}", style=style, no_wrap=False, justify=justify)
        for i, row in enumerate(data,1):
            if reverse: table.add_row( *(str(i), row) )
            else: table.add_row( *(row, str(i)) )
        Console().print(table)
        #print()


    def _getChapters(self):
        clear_screen()
        chapter_units = self.driver.find_elements(By.CLASS_NAME, 'chapter__unit')
        for i, chapter in enumerate(chapter_units):
            self.chapter_urls.append(chapter.get_attribute("href"))
            self.chapter_titles.append(chapter.get_attribute("text").split('"')[0].strip())
        self._tablular(self.chapter_titles)    


    def _getChapterLinks(self):
        for i in track(range(1, len(self.chapter_urls)+1), description="Downloading the Lesson(s) ..."):
            if i in self.exclude_list: 
                continue
            self.driver.get(self.chapters[i-1])
            chapter = self.driver.find_elements(By.LINK_TEXT,
                'دانلود')[0 if self.args.quality.upper() == "H" else 1]
            self.chapter_downloadlinks.append(chapter.get_attribute("href"))
            self._tablular([self.chapter_titles[i-1],], header=False, reverse=True)
            Console().print(self.chapter_downloadlinks[-1])

    def _saveChapterLinks(self):
        f = open(f"{self.args.path}/urls", 'w')
        f.write('\n'.join(self.chapter_downloadlinks))
        f.close()

    def _saveChapterVideos(self):
        for href in self.chapters_url:
            cmd = ['axel', '-Ncvn4', href]
            proc = subprocess.Popen(cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            o, e = proc.communicate()
            print("    Output:" + o.decode('ascii').split('\n')[-2])
            if e:
                print(f"    Error: {e.decode('ascii')}")
            if proc.returncode:
                print(f"    code: {str(proc.returncode)}")

    def dc(self):
        self.driver.close()

    @property
    def chapters(self):
        return self.chapter_urls

    @property
    def chapters_url(self):
        return self.chapter_downloadlinks
