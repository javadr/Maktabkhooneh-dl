#!/usr/bin/env python3

# Standard library imports
import re
from pathlib import Path

# Third-party imports
from playwright.sync_api import sync_playwright

# ----------------- settings -----------------
# COURSE_URL = "https://maktabkhooneh.org/course/آموزش-هک-قانونمند-ceh-mk641/"
COURSE_URL = input("please give me URL: ")
OUTPUT_DIR = Path("MK_Downloads")
USER_DATA_DIR = Path("./mk_profile")
SKIP_IF_EXISTS = True


# -------------------- سلکتور ها --------------------
# سلکتورها در صفحه دوره 
CHAPTER_SELECTOR = "div[id^='course-chapter-']" 
CHAPTER_TITLE_SELECTOR = "div[title^='فصل'] span.text-xl" 
LESSON_SELECTOR = "a.group[href*='/ویدیو-']"
LESSON_TITLE_SELECTOR = "div.BaseChapterContentUnitTitle > span[title]"
# سلکتور دکمه دانلود در صفحه جلسه 
DOWNLOAD_SELECTOR = ".unit-content--download a[download]"
# سلکتور دکمه ورود
LOGIN_BUTTON_SELECTOR = "button#login.button[type='button']"

# -------------------- پایان سلکتور --------------------

# ----------------- توابع کمکی -----------------
def slugify(txt: str) -> str:
    txt = re.sub(r"[^\w\s\-\.]", "", txt, flags=re.UNICODE)
    txt = re.sub(r"\s+", " ", txt, flags=re.UNICODE).strip()
    txt = txt.replace("/", "-")
    return txt

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

# ----------------- اسکریپت اصلی -----------------
def main():
    ensure_dir(OUTPUT_DIR)
    ensure_dir(USER_DATA_DIR)

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(USER_DATA_DIR),
            headless=False,
            viewport={"width": 1920, "height": 1080} 
        )
        page = browser.new_page()

        
        page.goto(COURSE_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        # ----------------- بررسی لاگین -----------------
        if page.query_selector(LOGIN_BUTTON_SELECTOR):
            print("[INFO] هنوز لاگین نشده، لطفاً وارد شوید...")
            page.click(LOGIN_BUTTON_SELECTOR)
            
            page.wait_for_timeout(15000) 
            input("✅ بعد از لاگین شدن، Enter بزنید...")

        page.wait_for_selector(CHAPTER_SELECTOR)

        chapters = page.query_selector_all(CHAPTER_SELECTOR)
        print(f"[INFO] تعداد {len(chapters)} فصل پیدا شد.")

        chapters_data = []
        for ch_idx, ch in enumerate(chapters, start=1):
            ch_title_el = ch.query_selector(CHAPTER_TITLE_SELECTOR)
            ch_title = slugify(ch_title_el.inner_text()) if ch_title_el else f"Chapter_{ch_idx}"
            
            lessons = ch.query_selector_all(LESSON_SELECTOR)
            lesson_infos = []
            for l_idx, lesson in enumerate(lessons, start=1):
                l_title_el = lesson.query_selector(LESSON_TITLE_SELECTOR)
                l_title = slugify(l_title_el.get_attribute("title") or l_title_el.inner_text()) if l_title_el else f"Lesson_{l_idx}"
                lesson_href = lesson.get_attribute("href")
                if not lesson_href.startswith("http"):
                    lesson_href = "https://maktabkhooneh.org" + lesson_href
                lesson_infos.append((l_idx, l_title, lesson_href))
            
            chapters_data.append((ch_idx, ch_title, lesson_infos))

        
        for ch_idx, ch_title, lesson_infos in chapters_data:
            chapter_dir = OUTPUT_DIR / f"{ch_idx:02d} - {ch_title}"
            ensure_dir(chapter_dir)
            for l_idx, l_title, lesson_href in lesson_infos:
                out_path = chapter_dir / f"{l_idx:02d}-{l_title}.mp4"
                if SKIP_IF_EXISTS and out_path.exists():
                    continue
                page.goto(lesson_href, wait_until="domcontentloaded")
                page.wait_for_selector(DOWNLOAD_SELECTOR)
                with page.expect_download(timeout=600000) as dl_info:
                    page.click(DOWNLOAD_SELECTOR)
                dl_info.value.save_as(str(out_path))


        browser.close()

if __name__ == "__main__":
    main()
