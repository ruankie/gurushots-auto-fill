# Description
This programme uses Python along with [Selenium](https://www.selenium.dev/documentation/en/) to automate the tedious *exposure filling* process on [GuruShots](https://gurushots.com/). 

GuruShots is a platform that enables users from around the globe to enter photography competitions. Each competition has a specific topic that users have to stick to. During the competition, users vote for the photos of other users and get increased exposure for their own photos in return. Each user achieves maximum exposure by filling thier exposure meter for a given challenge, increasing the chances of their photos being seen (and voted for) by other users.

# How to Use
## Prerequisites
Ensure that you have `Selenium`, `Google Chrome`, and `ChromeDriver` installed on your machine. If not, follow these steps:
1. Run `pip install selenium` from your terminal to install Selenium **OR** `pip install -r requirements.txt` to install correct versions of all depedencies.
2. Download and install Google Chrome web browser from [here](https://www.google.com/chrome/).
3. Download ChromeDriver driver for your version of Google Chrome [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).
4. Move the `chromedriver.exe` file that was downloaded in step *3* to `C:\Program Files (x86)\` **OR** change the path of `chromedriver.exe` inside the `python auto_fill.py` file to the relevant location on your machine.

## Exection
In order to use this exposure auto-filler, ensure all the steps in the Prerequisites section above have been completed. Then follow these steps:
1. Add your GuruShots login credentials in the `credentials.py` file.
2. Run `python auto_fill.py` from your terminal and watch as your GuruShots eposure is auto-filled.

Any active challenges on your GuruShots profile will have their eposures auto-filled.

# Disclaimer
This is for website testing and educational purposes only. This programme was intended for users to learn how the Selenium library works in the Python environment while exposing users to online photography competitions. The author will not be held responsible for any misuse of tihs code.