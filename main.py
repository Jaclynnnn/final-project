from selenium.webdriver.support.wait import WebDriverWait

import bot

# Amount of time to collect the data for in hours
time_to_run = 2.5
# Time to wait between each time collecting the data (delay inside the loop)
sleep_time = 15
# The name for the file that the contacts' data will be written to
output_file_name = "data.csv"
# The time to wait until selenium finds the chat/s. After that time it will throw an error
time_to_wait_if_error = 25

my_bot = bot.Bot(time_to_wait_if_error)
my_bot.OnlineLogs(time_to_run, sleep_time, output_file_name)