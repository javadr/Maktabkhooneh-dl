#!/usr/bin/env python3


# Standard library imports
import requests
import subprocess
import stat
from pathlib import Path

# Third-party imports
from bs4 import BeautifulSoup
from rich import print
from rich.console import Console
from rich.progress import Progress
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Local application imports
from maktabkhooneh import TableStreamer, shell_script, clear_screen
from maktabkhooneh.parser import CourseConfig, DownloaderConfig


class Course:
    def __init__(self, course_cfg: CourseConfig, downloader_cfg: DownloaderConfig):
        self.course_cfg = course_cfg
        self.downloader_cfg = downloader_cfg

        self.console = Console(log_path=False)
        self.streamer = TableStreamer()
        self._showChapters()

        self.driver = Firefox()
        self.driver.get(self.course_cfg.course_url)
        self.wait = WebDriverWait(self.driver, 15)

    @property
    def chapter_urls(self):
        """List of URLs for each chapter."""
        return self.course_cfg.chapter_urls

    @property
    def chapter_titles(self):
        """List of titles for each chapter."""
        return self.course_cfg.chapter_titles

    @property
    def chapter_downloadlinks(self):
        """List of download links for each chapter's video."""
        return self.course_cfg.chapter_downloadlinks

    @property
    def exclude_list(self):
        """Set of lessons to be excluded from download."""
        return self.course_cfg.exclude_list

    @exclude_list.setter
    def exclude_list(self, item):
        """Update the set of lessons to be excluded from download."""
        self.course_cfg.exclude_list = item

    def _showChapters(self):
        page = requests.get(self.course_cfg.course_url)
        if page.status_code != 200:
            print(f"[red] Course {self.course_cfg.course_url} was not found.[/red]")
            exit()
        soup = BeautifulSoup(page.text, "html.parser")
        chapters = [
            item.get_text().replace("\n", "").split('"')[0].strip()
            for item in soup.find_all("span", class_="font-medium ellipsis text-dark flex-1")
        ]
        self.streamer.create_table(chapters[: len(chapters)])
        self.streamer.stop()
        self.streamer.console.print("Be Patient ...", end="")

    def extract(self):
        self._login()
        self._get_chapters()  # gets chapters of the course
        self._get_exclusion()  # sets the exclude list
        self._get_chapter_links()  # makes the download urls of the inlcluded lesson(s)
        if not self.downloader_cfg.axel:
            self._save_chapter_links()
        else:
            self._save_chapter_videos()

    def _login(self):
        # Click the login button (top-left)
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'ورود')]")))
        login_button.click()

        # Wait for user form to appear and then Fill in credentials
        email_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="tessera"]')))
        email_input.send_keys(self.course_cfg.username)

        ok_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'تایید')]")))
        ok_button.click()

        # Wait for password form to appear and then Fill in credentials
        password_input = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        password_input.send_keys(self.course_cfg.password)

        login_submit = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-tag='ga-password-submit']"))
        )
        login_submit.click()

    def _get_exclusion(self):
        getRange = lambda x: set(
            range(int(x), int(x) + 1)
            if len(x.split("-")) == 1
            else range(int(x.split("-")[0]), int(x.split("-")[1]) + 1)
        )
        if not self.downloader_cfg.interactive:
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
                self.exclude_list.difference_update(getRange(item))

    def _get_chapters(self):
        chapter_units = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/ویدیو-']")))
        clear_screen()

        if len(chapter_units) == 0:
            print("[red] You should [bold]register[/bold] at first in the course in order to have acces to it.[/red]")
            exit()
        for i, chapter in enumerate(chapter_units):
            self.chapter_urls.append(chapter.get_attribute("href"))
            self.chapter_titles.append(chapter.get_attribute("text").split('"')[0].strip())

        self.streamer.create_table(self.chapter_titles)
        self.streamer.stop()

    def _get_chapter_links(self):
        with Progress(console=self.console) as progress:
            task = progress.add_task(
                "Downloading the Lesson(s) ...",
                total=len(self.chapter_urls) - len(self.exclude_list),
            )
            self.streamer.create_table(data=[])
            for i in range(1, len(self.chapter_urls) + 1):
                if i in self.exclude_list:
                    continue
                self.driver.get(self.chapter_urls[i - 1])
                chapter = self.driver.find_elements(By.LINK_TEXT, "دانلود")[
                    0 if self.downloader_cfg.quality.upper() == "H" else 1
                ]
                self.chapter_downloadlinks.append(chapter.get_attribute("href"))
                self.streamer.add_row(self.chapter_titles[i-1], i)
                self.streamer.console.log(f"Lesson {i}: {self.chapter_downloadlinks[-1]}")
                             
                progress.update(task, advance=1)
            self.streamer.stop()

    def _save_chapter_links(self):
        # Save all chapter download URLs to a file named 'urls' in the target path,
        # excluding any chapters listed in self.exclude_list
        with open(f"{self.downloader_cfg.path}/urls", "w") as f:
            f.write(
                "\n".join([url for i, url in enumerate(self.chapter_downloadlinks, 1) if i not in self.exclude_list]),
            )

        # Prepare a string of "name|url" pairs for each chapter, skipping excluded chapters
        # This string will be injected into the shell script template
        names_urls = ""
        for i, (url, name) in enumerate(zip(self.chapter_downloadlinks, self.chapter_titles), 1):
            if i in self.exclude_list:
                continue
            names_urls += f'"{name}|{url}"\n    '

        # Write the downloader shell script ('download.sh') in the target path
        # Inject the prepared "name|url" entries into the shell script template
        file_path = Path(f"{self.downloader_cfg.path}/download.sh")
        with open(file_path, "w") as f:
            f.write(shell_script.format(names_urls.rstrip()))

        # Make the shell script executable for all users (owner, group, others)
        mode = file_path.stat().st_mode
        file_path.chmod(mode | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def _save_chapter_videos(self):
        for href in self.chapter_downloadlinks:
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
