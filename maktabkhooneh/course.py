#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

import time
import subprocess
import urllib.parse

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from rich import print
from tqdm import tqdm

class Course():

    def __init__(self, course_name, user, passwd, args):
        self.course_name = course_name
        self.course_url = f"https://maktabkhooneh.org/course/{self.course_name}"
        self.user = user
        self.passwd = passwd
        self.driver = None
        self.chapter_urls = [] # url for each chapters
        self.chapter_downloadlinks = [] # download link of the chapter's video
        self.args = args

    def extract(self):
        self.driver = Firefox()
        self.driver.get(self.course_url)
        self._login()
        self._getChapters()
        self._getChapterLinks()
        if not self.args.axel:
            self._saveChapterLinks()
        else:
            self._saveChapterVideos()
        return self.chapter_downloadlinks

    def _login(self):
        submit = self.driver.find_element_by_class_name('button')
        submit.click()
        elem = self.driver.find_element_by_name('tessera')
        elem.send_keys(self.user)
        elem.send_keys(Keys.ENTER)
        time.sleep(2)
        elem = self.driver.find_element_by_name('password')
        elem.send_keys(self.passwd)
        elem.send_keys(Keys.ENTER)
        time.sleep(2)

    def _getChapters(self):
        self.chapter_urls = []
        chapter_units = self.driver.find_elements_by_class_name(
            'chapter__unit')
        for i, chapter in enumerate(chapter_units, 1):
            self.chapter_urls.append(chapter.get_attribute("href"))
            url = urllib.parse.unquote(self.chapter_urls[-1]).replace(self.course_url, '')
            print(f"[red]Lesson {i:2}[/red]: {url}")

    def _getChapterLinks(self):
        for url in tqdm(self.chapters):
            self.driver.get(url)
            chapter = self.driver.find_element_by_link_text('دانلود')
            self.chapter_downloadlinks.append(chapter.get_attribute("href"))
            print(self.chapter_downloadlinks[-1])

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