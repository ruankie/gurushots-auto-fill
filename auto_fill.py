##############################################################################################
## Author:           Ruan Pretorius                                                         ##
## GitHub:           https://github.com/ruankie                                             ##
## Last Updated:     13 June 2021                                                            ##
## Disclaimer:       This is for website testing and educational purposes only.             ##
##                   This programme was intended for users to learn how the Selenium        ##
##                   library works in the Python environment while exposing users to        ##
##                   online photography competitions. The author will not be held           ##
##                   responsible for any misuse of tihs code.                               ##
##############################################################################################


######################
## import libraries ##
######################
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from credentials import my_email_address, my_password
import numpy as np


#########################
## consants and config ##
#########################
CHROMEDRIVER_PATH = 'C:/Program Files (x86)/chromedriver.exe' # location of driver
LOGIN_WAIT = 15 # max time to wait for login elements to load
IMPLICIT_WAIT = 5 # implicit wait time
LOW_WAIT_TIME_BETWEEN_CHALLENGES = 4.0 # lower limit of wait time between filling chllenges
HIGH_WAIT_TIME_BETWEEN_CHALLENGES = 10.0 # upper limit of wait time between filling chllenges
LOW_WAIT_TIME_BETWEEN_VOTES = 0.05 # lower limit of wait time between voting for photos
HIGH_WAIT_TIME_BETWEEN_VOTES = 0.5 # upper limit of wait time between voting for photos
FILL_THRESHOLD = 85.0 # only vote if exposure less than this
BOOST = True # whether ot not to boost where free boosts are available
HEADLESS = False # whether or not to run Chrome headless
if HEADLESS:
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options) # load driver
else:
    driver = webdriver.Chrome(CHROMEDRIVER_PATH) # load driver



######################
## helper functions ##
######################
def go_to_home_page():
    '''
    go to page GuruShots home page
    '''
    driver.get('https://gurushots.com/')
    driver.fullscreen_window()


def go_to_challenges_page():
    '''
    go to page that contains currently enrolled challenges
    '''
    driver.get('https://gurushots.com/challenges/my-challenges/current')
    driver.fullscreen_window()   


def log_in(email, password):
    '''
    log into GuruShots account with specified email address and password
    store your credentials inside the credentials.py file
    '''
    try:
        print('logging in...')

        # click login button
        log_in_button = WebDriverWait(driver, LOGIN_WAIT).until(
            EC.presence_of_element_located((By.XPATH, "//*[@ng-click='$ctrl.signin()']"))
        )
        log_in_button.click()

        # send login credentials and hit enter to log in
        email_field = WebDriverWait(driver, LOGIN_WAIT).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_field.send_keys(email)
        password_field = WebDriverWait(driver, LOGIN_WAIT).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        print('logged in.')

    except Exception as e:
        print('*** ERROR: ',e)


def fill_exposure(challenge_nb=0):
    '''
    fill exposure of specific challenge
    '''    
    driver.implicitly_wait(IMPLICIT_WAIT)
    vote_buttons = driver.find_elements_by_xpath("//div[@ng-click='$ctrl.vote()']")

    try:
        # click on challenge vote button
        vote_button = vote_buttons[challenge_nb]
        driver.implicitly_wait(IMPLICIT_WAIT)
        vote_button.click()

        # click LET'S GO button
        driver.implicitly_wait(IMPLICIT_WAIT)
        lets_go_button = driver.find_element_by_xpath("//div[text()=" + "\"LET'S GO\"" + "]")
        lets_go_button.click()

        # click 3 photos until exposure meter is full
        last_photo_voted = 0        
        exposure_filled = False        
        while not exposure_filled:
            # check if exposure full
            driver.implicitly_wait(IMPLICIT_WAIT)
            exposure_meter = driver.find_element_by_xpath("//div[@class='modal-vote__exposure-meter__arrow']")
            rotation = float(exposure_meter.get_attribute('style').split('rotate(')[1].split('deg)')[0])
            if rotation < 90.0:
                for i in range(last_photo_voted, last_photo_voted+3):
                    driver.implicitly_wait(IMPLICIT_WAIT)
                    photo = driver.find_element_by_xpath(f"//div[@id='vote-photo-{i}']")
                    time.sleep(np.round(np.random.uniform(low=0.05, high=0.5),2)) # wait between photo clicks for realism
                    photo.click()
                    last_photo_voted += 1
            else:
                print('\texposure full.')
                exposure_filled = True

        # click submit vote
        driver.implicitly_wait(IMPLICIT_WAIT)
        submit_vote_button = driver.find_element_by_xpath("//span[text()='SUBMIT VOTE']")
        submit_vote_button.click()

        # close vote window
        driver.implicitly_wait(IMPLICIT_WAIT)
        close_button = driver.find_element_by_xpath("//*[@id='gs-app-main']/gs-modals/div/modal-vote/div[4]/div/div[2]/div[2]")
        close_button.click()

    except Exception as e:
        print('\t*** ERROR: ',e)
        go_to_challenges_page()


def boost_available():
    '''
    find all available boosts and boost most pupular image for given challenge
    '''
    try:
        # find available boosts
        driver.implicitly_wait(IMPLICIT_WAIT)
        boosts_abailable = driver.find_elements_by_class_name("challenge-action-button__content__boost-state__available")
        nb_boosts_abailable = len(boosts_abailable)
        print(f'{nb_boosts_abailable} available boosts found.')

        # loop through available boosts and boost most pupular image
        for i, boost_button in enumerate(boosts_abailable):
            print(f'\tboosting {i+1}/{nb_boosts_abailable}...')
            # click boost
            boost_button.click()
            driver.implicitly_wait(IMPLICIT_WAIT)

            # click on left-most picture
            left_image = driver.find_element_by_xpath("//md-dialog-content/div[2]/div[3]/div[1]")
            left_image.click()
            driver.implicitly_wait(IMPLICIT_WAIT)

    except Exception as e:
        print('\t*** ERROR: ',e)
        go_to_challenges_page()



####################
## main execution ##
####################
if __name__ == '__main__':

    # open home page
    go_to_home_page()

    # log in
    log_in(my_email_address, my_password)

    # check exposure meters of active challenges
    driver.implicitly_wait(IMPLICIT_WAIT)
    exposure_meters = driver.find_elements_by_xpath("//div[@class='c-challenges-item__exposure__meter__arrow']")
    print(f'{len(exposure_meters)} active challenges found.')

    # add challenge id to list if exposure meter below threshold
    unfilled_meters_idxs = []
    for e, exp_meter in enumerate(exposure_meters):
        rotation = float(exp_meter.get_attribute('style').split('rotate(')[1].split('deg)')[0])
        if rotation < FILL_THRESHOLD:
            unfilled_meters_idxs.append(e)

    # fill exposure meters
    nb_vote_buttons = len(unfilled_meters_idxs)
    for i, idx in enumerate(unfilled_meters_idxs):
        time.sleep(np.random.randint(low=LOW_WAIT_TIME_BETWEEN_CHALLENGES, high=HIGH_WAIT_TIME_BETWEEN_CHALLENGES)) # to keep request frequency low and realism high
        print(f'filling challenge {i+1}/{nb_vote_buttons}...')
        fill_exposure(challenge_nb=idx)

    # boost all available
    if BOOST:
        boost_available()

    # wait for a second
    time.sleep(1)

    # close window
    driver.quit()
    print('done.')