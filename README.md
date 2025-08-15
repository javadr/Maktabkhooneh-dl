# 📥 Maktabkhooneh Downloader

## مقدمه

[Maktabkhooneh](https://maktabkhooneh.org) یکی از بزرگ‌ترین پلتفرم‌های MOOC فارسی است که دوره‌های خود را از بهترین دانشگاه‌های ایران، مانند [دانشگاه صنعتی شریف](http://sharif.edu) گردآوری می‌کند.

این پروژه به شما کمک می‌کند تا ویدیوهای دوره‌ها را به صورت **Batch** دانلود کنید.
برای دسترسی به لینک‌های ویدیو، نیاز به حساب کاربری مکتب‌خونه دارید.

---

## ✨ ویژگی‌ها

* **ورژن ۱** – نسخه اصلی بر پایه **Selenium + geckodriver** (پشتیبانی از نسخه‌های قدیمی‌تر سایت)
* **ورژن ۲** – نسخه بازنویسی شده با **Playwright** (سریع‌تر، پایدارتر، بدون نیاز به geckodriver)

---

## 📦 نصب وابستگی‌ها

### نسخه ۱ (قدیمی - Selenium)

```bash
pip install -r requirements.txt
```

همچنین نیاز دارید **geckodriver** نصب کنید تا Selenium بتواند مرورگر Firefox را کنترل کند.

---

### نسخه ۲ (جدید - Playwright)

```bash
pip install -r v2/requirements-v2.txt
playwright install
```

---

## ▶️ نحوه اجرا

### نسخه ۱ – Selenium

```bash
python maktabkhooneh-dl.py -u <USERNAME> -p <PASSWORD> <COURSE_SLUG>
```

مثال:

```bash
python maktabkhooneh-dl.py -u test@example.com -p 123456 آموزش-رایگان-تحلیل-هوشمند-تصاویر-زیست-پزشکی-mk1070
```

---

### نسخه ۲ – Playwright

```bash
python v2/maktabkhone-dl-v2.py -u <USERNAME> -p <PASSWORD> <COURSE_URL>
```

مثال:

```bash
python v2/maktabkhone-dl-v2.py -u test@example.com -p 123456 https://maktabkhooneh.org/course/آموزش-کالی-Linux-mk4021
```

---

## 🛠 گزینه‌ها

| گزینه کوتاه   | گزینه کامل            | توضیح                                                          |
| ------------- | --------------------- | -------------------------------------------------------------- |
| `-u USERNAME` | `--username USERNAME` | ایمیل یا شماره موبایلی که با آن وارد مکتب‌خونه می‌شوید         |
| `-p PASSWORD` | `--password PASSWORD` | رمز عبور                                                       |
| `-i`          | `--interactive`       | انتخاب تعاملی جلسات برای دانلود                                |
| `-q QUALITY`  | `--quality QUALITY`   | کیفیت ویدیو (`H` برای کیفیت بالا، `L` برای پایین – پیش‌فرض: H) |
| -             | `--path PATH`         | مسیر ذخیره‌سازی فایل‌ها (پیش‌فرض: پوشه جاری)                   |

---

## 📂 ساختار پروژه

```
.
├── maktabkhooneh           # نسخه ۱ (Selenium)
│   ├── course.py
│   ├── __init__.py
│   ├── maktabkhooneh_dl.py
│   └── parser.py
├── maktabkhooneh-dl.py     # اسکریپت اصلی نسخه ۱
├── README.md
├── requirements.txt
└── v2                      # نسخه ۲ (Playwright)
    ├── maktabkhone-dl-v2.py
    └── requirements-v2.txt
```

---

## 💡 نکات

* پیشنهاد می‌شود از **نسخه ۲** استفاده کنید مگر این که نیاز به پشتیبانی از ساختار قدیمی مکتب‌خونه داشته باشید.
* نسخه ۲ سرعت بالاتر، مدیریت خطای بهتر، و عدم نیاز به نصب geckodriver دارد.
* قبل از اجرای نسخه ۲ حتماً دستور `playwright install` را اجرا کنید.
* در صورتی که قالب مکتب خونه اپدیت شده باشد شما در نسخه ۲ کافیست  قسمت سلکتور‌ها و اپدیت کنید یعنی قسمت زیر(لطفا از اپدیت ها ما را نیز مطلع کنید):
```python
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

```


# 📥 Maktabkhooneh Downloader

## Introduction

[Maktabkhooneh](https://maktabkhooneh.org) is one of the largest Persian MOOC platforms, providing courses from top universities in Iran, such as [Sharif University of Technology](http://sharif.edu).

This project helps you **batch download** course videos.
To access video links, you need a Maktabkhooneh account.

---

## ✨ Features

* **Version 1** – Original version based on **Selenium + geckodriver** (supports the old site structure)
* **Version 2** – Rewritten version using **Playwright** (faster, more stable, no geckodriver required)

---

## 📦 Installing Dependencies

### Version 1 (Old – Selenium)

```bash
pip install -r requirements.txt
```

You also need **geckodriver** installed so that Selenium can control the Firefox browser.

---

### Version 2 (New – Playwright)

```bash
pip install -r v2/requirements-v2.txt
playwright install
```

---

## ▶️ How to Run

### Version 1 – Selenium

```bash
python maktabkhooneh-dl.py -u <USERNAME> -p <PASSWORD> <COURSE_SLUG>
```

Example:

```bash
python maktabkhooneh-dl.py -u test@example.com -p 123456 آموزش-رایگان-تحلیل-هوشمند-تصاویر-زیست-پزشکی-mk1070
```

---

### Version 2 – Playwright

```bash
python v2/maktabkhone-dl-v2.py -u <USERNAME> -p <PASSWORD> <COURSE_URL>
```

Example:

```bash
python v2/maktabkhone-dl-v2.py -u test@example.com -p 123456 https://maktabkhooneh.org/course/آموزش-کالی-Linux-mk4021
```

---

## 🛠 Options

| Short form    | Long form             | Description                                            |
| ------------- | --------------------- | ------------------------------------------------------ |
| `-u USERNAME` | `--username USERNAME` | Email or phone number used to log in to Maktabkhooneh  |
| `-p PASSWORD` | `--password PASSWORD` | Password                                               |
| `-i`          | `--interactive`       | Interactively choose which lessons to download         |
| `-q QUALITY`  | `--quality QUALITY`   | Video quality (`H` for high, `L` for low – default: H) |
| -             | `--path PATH`         | Path to save the files (default: current directory)    |

---

## 📂 Project Structure

```
.
├── maktabkhooneh           # Version 1 (Selenium)
│   ├── course.py
│   ├── __init__.py
│   ├── maktabkhooneh_dl.py
│   └── parser.py
├── maktabkhooneh-dl.py     # Main script for version 1
├── README.md
├── requirements.txt
└── v2                      # Version 2 (Playwright)
    ├── maktabkhone-dl-v2.py
    └── requirements-v2.txt
```

---

## 💡 Notes

* It’s recommended to use **Version 2**, unless you specifically need to support the old Maktabkhooneh structure.
* Version 2 offers higher speed, better error handling, and no need to install geckodriver.
* Before running Version 2, make sure you have executed `playwright install`.
* If Maktabkhooneh updates its UI, you may need to update the selectors in Version 2. Example:

```python
# -------------------- Selectors --------------------
# Course page selectors
CHAPTER_SELECTOR = "div[id^='course-chapter-']" 
CHAPTER_TITLE_SELECTOR = "div[title^='فصل'] span.text-xl" 
LESSON_SELECTOR = "a.group[href*='/ویدیو-']"
LESSON_TITLE_SELECTOR = "div.BaseChapterContentUnitTitle > span[title]"
# Download button on lesson page
DOWNLOAD_SELECTOR = ".unit-content--download a[download]"
# Login button
LOGIN_BUTTON_SELECTOR = "button#login.button[type='button']"

# -------------------- End of selectors --------------------
```

