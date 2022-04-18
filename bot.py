import sys
import datetime
from turtle import pd

from colorama import Fore
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
import selenium.common as sc
from time import sleep, time
import math
import pandas as pd
import os
from Classes import *

STATUS_XPATH = "/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/header/div[2]/div[2]/span"
CHAT_CLASS = "_3m_Xw"

class Bot():
    def __init__(self, time_to_wait_if_error):

        self.driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe")
        self.driver.get("https://web.whatsapp.com/")
        self.driver.maximize_window()
        #press not to remember the user
        #remember = self.driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div[3]/label/input')
        #remember.click()
        print("please scan QR code and press Enter")
        #wait for user input for scanning the QR
        input()
        print("Logged in!")
        self.wait = WebDriverWait(self.driver, time_to_wait_if_error)

    def OnlineLogs(self, time_to_run: float, sleep_time: float, output_file_name: str):

        print(f"{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y')}:"
              f" {Fore.YELLOW}[!] Welcome, program is currently setting up some needed data.\n")

        try:
            # Write the headers to the data file before appending anything related to the statuses themselves.
            df = pd.DataFrame(columns=("Name", "Status", "Duration", "Time"))
            df.to_csv(output_file_name, index=False, encoding='utf-8-sig')

        except PermissionError:
            print(f"\n{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y')}:"
                  f" {Fore.RED} Error- the file {output_file_name} is opened in another program.")
            input("Please close the file and press a key on the keyboard >> ")
            print(f"{Fore.GREEN}[+] Success. Starting the program...\n")

        contacts: list[Contact] = []
        # Collect the chats' info while making sure the window still exist to not show error on the screen.
        try:
            sleep(2)
            chats = self.wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, CHAT_CLASS)))
        except sc.exceptions.NoSuchWindowException:
            print(f"\n{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y')}:"
                  f"{Fore.RED}[-] Error: browser window was closed. Exiting the program...")
            chats = None
            sleep(1)
            exit(1)

        except:
            chat = self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, CHAT_CLASS)))
            chat.click()

        print(datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y') + "Starting to collect the statuses")
        sleep(1)
        times_to_loop = math.ceil(time_to_run * 3600 / sleep_time)
        last_print_is_printr = False
        for i in range(1, times_to_loop + 1):
            start = time()
            for chat in chats:
                try:
                    chat.click()
                except:
                    chat = self.wait.until(ec.presence_of_element_located((By.CLASS_NAME, CHAT_CLASS)))
                    chat.click()
                try:
                    # Get the status of the current chat by its xpath
                    status = self.wait.until(ec.presence_of_element_located((By.XPATH, STATUS_XPATH)))

                    # Make sure that the current contact has his online and last seen status enabled in whatsapp settings
                    if self._validate_contact_status(status.text):
                        name = str(chat.text).splitlines()[0]
                        contact_exists = False

                        for j in range(len(contacts)):
                            if contacts[j].get_name() == name:
                                # Means we've found our contact in the list. Then we will start comparing his current
                                # status to his last saved status.
                                status = self._check_status(status.text)

                                if status != contacts[j].get_status():
                                    # Means that the status has changed
                                    if status == 1:
                                        if last_print_is_printr: print()  # Print a new line if the last one used printr()

                                        print(f"{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y')}:"
                                              f"{Fore.YELLOW}[!] {contacts[j].get_name()} has gone online.")
                                        last_print_is_printr = False

                                    else:
                                        if last_print_is_printr: print()  # Print a new line if the last one used printr()

                                        print(f"{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y')}:"
                                              f"{Fore.YELLOW}[!] {contacts[j].get_name()} has gone offline.")
                                        last_print_is_printr = False

                                    # Get the current time and calculate the time difference between the current time and
                                    # the time that the last status of the contact has been changed, which is essentially
                                    # the duration of the last status
                                    timestamp = datetime.datetime.now()
                                    time_delta = timestamp - contacts[j].get_timestamp()

                                    # Save the current status, so it will become the last status (while overriding the
                                    # last saved status)
                                    contacts[j].set_duration(math.ceil(time_delta.total_seconds()))
                                    contacts[j].set_timestamp(timestamp)
                                    contacts[j].set_status(status)

                                    self._write_data(contacts[j], output_file_name)

                                contact_exists = True
                                break
                        if not contact_exists:
                            # Means that a new contact has been checked, a one that is not in our list yet
                            if last_print_is_printr: print()  # Print a new line if the last one used printr()

                            print(f"{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y')}:"f" {Fore.YELLOW}[!] A new contact has been found- {name}.")
                            last_print_is_printr = False

                            contacts.append(Contact(name, self._check_status(status.text), datetime.datetime.now()))
                            self._write_data(Contact(name, self._check_status(status.text), datetime.datetime.now()), output_file_name)

                except sc.exceptions.NoSuchElementException:
                    continue

                except sc.exceptions.StaleElementReferenceException:
                    continue

                except KeyboardInterrupt:
                    if last_print_is_printr: print()  # Print a new line if the last one used printr()

                    print(f"\n{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M, %m/%d/%Y')}:"
                          f" {Fore.YELLOW}[!] Program has been stopped manually.")
                    self._sort_file(output_file_name)
                    last_print_is_printr = False

                except Exception as e:
                    if last_print_is_printr: print()  # Print a new line if the last one used printr()

                    print(f"\n{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y')}:"f" {Fore.RED}[-] Error- {e}")
                    last_print_is_printr = False

            try:
                if sleep_time - (time() - start) > 0:
                    sleep(sleep_time - (time() - start))
            except KeyboardInterrupt:
                if last_print_is_printr: print()  # Print a new line if the last one used printr()

                print(f"\n{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y')}:"
                      f" {Fore.YELLOW}[!] Program has been stopped manually.")
                self._sort_file(output_file_name)
                last_print_is_printr = False

            minutes_left = (times_to_loop - i) * 15 / 60  # Calculates the time left

            self.printr(f"{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y')}: "
                   f"{Fore.GREEN}[+] Iteration {i}/{times_to_loop} (about {minutes_left} minutes left)...")
            last_print_is_printr = True

        self._sort_file(output_file_name)

        print(f"\n\n{Fore.CYAN}{datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y')}:"f" {Fore.GREEN}[+] Finished collecting the data.")

    #Given Func
    def printr(self, s):
        print("\r" + s, end='')

    #Given Func
    def _validate_contact_status(self, status: str) -> bool:
        # Returns true if the given status of a contact is valid for a contact: either typing, online or the last hour he
        # was seen. A status is false if it contains any other text. Note that it gets a string of the status.

        if status == "online" or status == "typing...":
            return True
        elif status == "מחובר/ת" or status == "מקליד/ה...":
            return True
        elif "last seen" in status or "נראה/תה לאחרונה" in status:
            return True
        else:
            return False

    #Given Func
    def _check_status(self, status: str) -> int:
        # Simplifies the given status to 1 for online status or 0 for offline status.
        if status == "online" or status == "typing...":
            return 1
        elif status == "מחובר/ת" or status == "מקליד/ה...":
            return 1
        else:
            return 0

    #Given Func
    def _write_data(self, contact: Contact, out_file_name: str):
        # Appends the given contact to the given filename.
        data = contact().split("\t")  # The string representation that we gave to contact will return us his name,
        # status and duration with /t (tab) between each one. So we split it into a list, so we can write it to the given
        # csv file with pandas.

        df = pd.DataFrame([data])
        df.to_csv(out_file_name, index=False, encoding='utf-8-sig', mode='a', header=False)  # mode='a' means append,
        # without overwriting the current data. The encoding we gave the function allows us to insert hebrew values to
        # the file.


    #Given Func
    def _sort_file(self, out_file_name: str):
        # Sorts the given csv file by the Name column.

        df = pd.read_csv(out_file_name)
        df = df.sort_values(by=["Name"], ascending=True)
        df.to_csv("data.csv", index=False, encoding='utf-8-sig')

