#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

import time
import subprocess
import urllib.parse

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from rich import print
from rich.progress import track


class Course():
    def __init__(self, course_name, user, passwd, args):
        self.course_name = course_name
        self.course_url = f"https://maktabkhooneh.org/course/{self.course_name}"
        self.user = user
        self.passwd = passwd
        self.driver = None
        self.chapter_urls = []  # url for each chapters
        self.chapter_downloadlinks = []  # download link of the chapter's video
        self.exclude_list = set() # saves the list of lessons to be excluded
        self.args = args

    def extract(self):
        self.driver = Firefox()
        self.driver.get(self.course_url)
        self._login()
        self._getChapters() # gets chapters of the course
        self._excludeList() # sets the exclude list
        self._getChapterLinks() # makes the download urls of the inlcluded lesson(s)
        if not self.args.axel:
            self._saveChapterLinks()
        else:
            self._saveChapterVideos()
        return self.chapter_downloadlinks
    def _excludeList(self):
        getRange = lambda x: set( range(int(x), int(x)+1) if len(x.split('-'))==1
                        else range(int(x.split('-')[0]), int(x.split('-')[1])+1) )
        if not self.args.interactive: return  # there would be no exclusion
        print('==> Lesson(s) to exclude: (e.g.: "1 2 3", "1-3", "^4"); to download all lessons just press the Enter key')
        exc = set(input("==> ").strip().split())
        if exc == set(): return # there would be no exclusion
        for item in exc:
            if '^' in item: continue
            else: self.exclude_list.update(getRange(item))
        inc = set() # included via ^ mark
        for item in exc:
            if '^'==item[0]: inc.update(getRange(item[1:]))
        self.exclude_list = self.exclude_list.difference(inc).union(set(range(1,len(self.chapter_urls)+1)).difference(inc))

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
        time.sleep(3)

    def _getChapters(self):
        self.chapter_urls = []
        chapter_units = self.driver.find_elements_by_class_name(
            'chapter__unit')
        for i, chapter in enumerate(chapter_units):
            self.chapter_urls.append(chapter.get_attribute("href"))
            url = urllib.parse.unquote(self.chapter_urls[-1]).replace(
                self.course_url, '')
            print(f"[red]Lesson {i+1:2}[/red]: {url}")
        print()

    def _getChapterLinks(self):
        for i, url in enumerate(
                track(self.chapters, description="Downloading the URLs ...")):
            if i+1 in self.exclude_list:
                continue
            self.driver.get(url)
            chapter = self.driver.find_elements_by_link_text('دانلود')[0 if self.args.quality.upper()=="H" else 1]
            self.chapter_downloadlinks.append(chapter.get_attribute("href"))
            url = urllib.parse.unquote(self.chapter_urls[i]).replace(
                self.course_url, '').split('/')[-2]
            print(f"[red]Lesson {i+1:2}[/red]: {url}")
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
