# Maktabkhooneh Downloader

## Introduction

[Maktabkhooneh](http://maktabkhooneh.org) provides *massive open online courses* (MOOCs) for Persian users, 
offering classes from top universities in Iran such as [Sharif University of Technology](http://sharif.edu). 
Maktabkhooneh has been active since 2011.

This script helps you batch download videos from Maktabkhooneh courses.  
To access the video links for any course, you must have a Maktabkhooneh account.

---

## Installing Dependencies

Use `pip` to install the required dependencies listed in `requirements.txt`:

```python
pip install -r requirements.txt
```

To enable Firefox with Selenium, you also need to install *geckodriver*.
Geckodriver launches the Firefox browser and supports JavaScript.

# Running the script

For a complete and up-to-date list of runtime options, refer to:
```bash
maktabkhooneh-dl --help
```

Run the script by providing your Maktabkhooneh account credentials (email and password), the course name, and any additional parameters:



```python
python maktabkhooneh-dl.py -u <user> -p <pass> آموزش-رایگان-تحلیل-هوشمند-تصاویر-زیست-پزشکی-mk1070
```

> **CAVEAT**: Due to a recent update, downloading course materials from Maktabkhooneh now requires prior registration for the course.

```

╔═══════════════════════════════════════════════════════════════════════════════════════════╦════════╗
║                                                                               Description ║ Lesson ║
╠═══════════════════════════════════════════════════════════════════════════════════════════╬════════╣
║                                         جلسه 1: مقدمات درس تحلیل هوشمند تصاویر زیست پزشکی ║   1    ║
║                                                              جلسه 2: پردازش تصویر مقدماتی ║   2    ║
║                                    جلسه 3: مباحث نظری سیستمهای خطی، فیلترها و تبدیل فوریه ║   3    ║
║                                               جلسه 4: ادامه تبدیل فوریه - استاندارد DICOM ║   4    ║
║                                              جلسه 5: آشنایی با تصویربرداری مبتنی بر X-Ray ║   5    ║
║                                                          جلسه 6: آشنایی با تصویربرداری CT ║   6    ║
║                                                         جلسه 7: آشنایی با تصویربرداری MRI ║   7    ║
║                                                         جلسه 8: آشنایی با تصویربرداری PET ║   8    ║
║                         جلسه 9: دو کاربرد از تصاویر MRI، آشنایی با تصویربرداری Ultrasound ║   9    ║
║                  جلسه 10: آشنایی با میکروسکوپهای Phase-Contrast، Dark Field، Bright Field ║   10   ║
║                                   جلسه 11: آشنایی با میکروسکوپهای Fluorescence و Confocal ║   11   ║
║                               جلسه 12: آشنایی با میکروسکوپهای Super-Resolution و الکترونی ║   12   ║
║                                                           جلسه 13: آشنایی با CellProfiler ║   13   ║
║                                                    جلسه 14: Image Registration (قسمت اول) ║   14   ║
║                                                    جلسه 15: Image Registration (قسمت دوم) ║   15   ║
║                                                    جلسه 16: Image Registration (قسمت سوم) ║   16   ║
║                                                  جلسه 17: Image Registration (قسمت چهارم) ║   17   ║
║                                                   جلسه 18: Image Registration (قسمت پنجم) ║   18   ║
║                                                                   جلسه 19: قطعهبندی تصویر ║   19   ║
║                                جلسه 20: قطعهبندی تصاویر با شبکههای U-Net (ارائه دانشجویی) ║   20   ║
║                           جلسه 21: ادامه قطعهبندی و تشخیص در تصاویر RCNN (ارائه دانشجویی) ║   21   ║
║                                  جلسه 22: ادامه قطعهبندی و روش Deep k-NN (ارائه دانشجویی) ║   22   ║
║                           جلسه 23: تشخیص بیماری COVID-19 در تصاویر X-Ray (ارائه دانشجویی) ║   23   ║
║     جلسه 24: مباحث Bone Age Estimation و Knee Magnetic Resonance Imaging (ارائه دانشجویی) ║   24   ║
║               جلسه 25: مباحث Pneumonia Detection و Skin Cancer Detection (ارائه دانشجویی) ║   25   ║
║                                             جلسه 26: دستهبندی تصاویر MRI (ارائه دانشجویی) ║   26   ║
║ جلسه 27: روش CE-Net برای قطعهبندی و همینطور قطعهبندی تومور در تصاویر MRI (ارائه دانشجویی) ║   27   ║
║                                          جلسه 28: سنجههای توانبالای میکروسکوپی (قسمت اول) ║   28   ║
║                                          جلسه 29: سنجههای توانبالای میکروسکوپی (قسمت دوم) ║   29   ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╩════════╝
Be Patient ...
```

## Options 
|short from |long form | description|
|---|---|---|
|`-u USERNAME`| `--username USERNAME` | username (email/tel) that you use to login to Maktabkhooneh|
|`-p PASSWORD` | `--password PASSWORD` |maktabkhooneh password |
| `-i` |`--interactive` | Interactively asks the user which lesson(s) to download|
| `-q QUALITY` |`--quality QUALITY`| Downloading quality of the lesson(s); H for high quality and L for low quality video (Default: H)|
|| `--path PATH` | Path to where to save the file. (Default: current directory)|
