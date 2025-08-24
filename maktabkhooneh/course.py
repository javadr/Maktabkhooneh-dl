#!/usr/bin/env python3

import os
import re
import subprocess

import requests
import textwrap
from bs4 import BeautifulSoup
from rich import box, print
from rich.console import Console
from rich.progress import track
from rich.table import Table
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clear_screen():
    # for mac and linux(here, os.name is 'posix')
    if os.name == "posix":
        os.system("clear")
    else:  # for windows platfrom
        os.system("cls")


class Course:
    def __init__(self, course_name, user, passwd, args):
        self.course_name = re.sub("http.*://.*?/.*?/", "", course_name)
        self.course_url = f"https://maktabkhooneh.org/course/{self.course_name}"
        self.user = user
        self.passwd = passwd
        self.driver = None
        self.wait = None
        self.chapter_urls = []  # url for each chapters
        self.chapter_titles = []  # title of each chapters
        self.chapter_downloadlinks = []  # download link of the chapter's video
        self.exclude_list = set()  # saves the list of lessons to be included
        self.args = args

    def extract(self):
        self._showChapters()
        self.driver = Firefox()
        self.driver.get(self.course_url)
        self.wait = WebDriverWait(self.driver, 15)
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
            print(f"[red] Course {self.course_url} was not found.[/red]")
            exit()
        soup = BeautifulSoup(page.text, "html.parser")
        chapters = [
            item.get_text().replace("\n", "").split('"')[0].strip()
            for item in soup.find_all("span", class_="font-medium ellipsis text-dark flex-1")
        ]
        self._tablular(chapters[: len(chapters)])
        print("Be Patient ...", end="")

    def _getExclusion(self):
        getRange = lambda x: set(
            range(int(x), int(x) + 1)
            if len(x.split("-")) == 1
            else range(int(x.split("-")[0]), int(x.split("-")[1]) + 1)
        )
        if not self.args.interactive:
            return  # there would be no exclusion
        print(
            "==> Press the Enter key to download all lessons, Type `end` to exit the application.",
            '    Lesson(s) to exclude: (e.g.: "1 2 3", "1-3", "^4"),',
            sep="\n",
            end=" ",
        )
        lineInput = input("==> ").strip().lower()
        if lineInput == "end":
            exit()
        exc = set(lineInput.strip().lower().split())
        if exc == set():
            return  # there would be no exclusion
        for item in exc:
            if item[0] == "^":
                self.exclude_list.update(getRange(item[1:]))

        self.exclude_list = set(range(1, len(self.chapter_urls) + 1)).difference(self.exclude_list)
        for item in exc:
            if item[0] != "^":
                self.exclude_list.update(getRange(item))

    def _login(self):
        # Click the login button (top-left)
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ورود')]")))
        login_button.click()

        # Wait for user form to appear and then Fill in credentials
        email_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tessera"]')))
        email_input.send_keys(self.user)

        ok_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'تایید')]")))
        ok_button.click()

        # Wait for password form to appear and then Fill in credentials
        password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_input.send_keys(self.passwd)

        login_submit = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-tag='ga-password-submit']"))
        )
        login_submit.click()

    def _tablular(self, data, header=True, reverse=False):
        Console().print()
        table = Table(show_header=header, header_style="bold", row_styles=["none", "dim"], box=box.DOUBLE)
        if len(data) > 1:
            for col, style, justify in zip(
                ("Description", "Lesson"),
                ("green", "bold cyan"),
                ("right", "center"),
            ):
                table.add_column(f"[{style}]{col}", style=style, no_wrap=False, justify=justify)
        else:
            table.add_column("[green]Description", style="green", no_wrap=False, justify="right")
        for i, row in enumerate(data, 1):
            if len(data) > 1:
                if reverse:
                    table.add_row(*(str(i), row))
                else:
                    table.add_row(*(row, str(i)))
            else:  # len(data)==1
                if reverse:
                    table.add_row(row)
                else:
                    table.add_row(row)
        Console().print(table)

    def _getChapters(self):
        clear_screen()

        chapter_units = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/ویدیو-']")))

        if len(chapter_units) == 0:
            print("You should register at first in the course in order to have acces to it.")
            exit()
        for i, chapter in enumerate(chapter_units):
            self.chapter_urls.append(chapter.get_attribute("href"))
            self.chapter_titles.append(chapter.get_attribute("text").split('"')[0].strip())

        self._tablular(self.chapter_titles)

    def _getChapterLinks(self):
        for i in track(range(1, len(self.chapter_urls) + 1), description="Downloading the Lesson(s) ..."):
            if i in self.exclude_list:
                continue
            self.driver.get(self.chapters[i - 1])
            chapter = self.driver.find_elements(By.LINK_TEXT, "دانلود")[0 if self.args.quality.upper() == "H" else 1]
            self.chapter_downloadlinks.append(chapter.get_attribute("href"))
            self._tablular([self.chapter_titles[i - 1]], header=False, reverse=True)
            Console().print(self.chapter_downloadlinks[-1])

    def _saveChapterLinks(self):
        with open(f"{self.args.path}/urls", "w") as f:
            f.write(
                "\n".join([url for i, url in enumerate(self.chapter_downloadlinks, 1) if i not in self.exclude_list]),
            )

        with open(f"{self.args.path}/download.sh", "w+") as f:
            f.truncate(0)
        with open(f"{self.args.path}/download.sh", "a+") as f:
            f.write(
                textwrap.dedent(r"""#!/usr/bin/env bash
                set -euo pipefail
                IFS=$'\n\t'

                # Where to save files
                mkdir -p "download"

                # axel options (tweak if you like)
                AXEL_OPTS=(-n 8 -a -c -v)   # 8 connections, alternate display, continue, verbose

                # One command per file (name first, then URL)
            """),
            )
            for i, (url, name) in enumerate(zip(self.chapter_downloadlinks, self.chapter_titles), 1):
                if i in self.exclude_list:
                    continue
                f.write('axel "{}" -o "download/{}.mp4" "{}"\n'.format("${AXEL_OPTS[@]}", name, url))

    def _saveChapterVideos(self):
        for href in self.chapters_url:
            cmd = ["axel", "-Ncvn4", href]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            o, e = proc.communicate()
            print("    Output:" + o.decode("ascii").split("\n")[-2])
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
