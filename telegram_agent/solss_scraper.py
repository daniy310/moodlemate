import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
# options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

def get_mobile_timetable(driver):
    timetable = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "courses_list": []
    }

    # Resize the window to simulate a mobile screen (e.g., 375px width)
    driver.set_window_size(375, 800)  # Simulate mobile view

    # Give the page some time to adjust to the mobile layout
    driver.implicitly_wait(3)

    # Find the timetable in mobile view (which is now a list of items)
    try:
        # Find all the <ul> elements (timetable days)
        ul_elements = driver.find_elements(By.XPATH, "//ul[@class='list-group']")
        print(f"✅ Found {len(ul_elements)} timetable sections in mobile view.")
    except Exception as e:
        print(f"❌ Error: Could not find mobile timetable - {e}")
        return timetable

    current_day = None
    for ul in ul_elements:
        li_elements = ul.find_elements(By.TAG_NAME, "li")

        for li in li_elements:
            # Check for day headers safely
            day_headers = li.find_elements(By.XPATH, ".//h4[@class='list-group-item-heading']")
            if day_headers:
                possible_day = day_headers[0].text.strip()
                if possible_day in timetable:  # Only update if it's a valid weekday
                    current_day = possible_day
                    print(f"📅 Found day: {current_day}")

            # Ensure `current_day` is set before processing courses
            if current_day is None:
                continue  # Skip processing if no valid day is found yet

            # Find enrolled courses safely
            course_headers = li.find_elements(By.XPATH, ".//h4[contains(text(), 'Enrolled')]")
            if course_headers:
                course_id = course_headers[0].text.strip().split('-')[-1].strip()

                # Extract course details safely
                course_details_elements = li.find_elements(By.XPATH, ".//p[@class='list-group-item-text']")
                course_details = course_details_elements[0].text.strip() if course_details_elements else "No details available"

                # Split course details into structured information
                course_details_lines = course_details.split("\n")
                if len(course_details_lines) >= 3:
                    course_type = course_details_lines[0].split(':')[0].strip()
                    course_timing = course_details_lines[1].split(',')[-1].strip()
                    course_start_time, course_end_time = course_timing.split('-')
                    course_location = course_details_lines[2].split(':')[-1].strip()

                    print(f"📌 Found course: {course_id} - {course_type} \n Starting at : {course_start_time} - {course_end_time} \n Location: {course_location}")

                    # Add course to timetable
                    timetable[current_day].append({
                        "course_id": course_id,
                        "course_type": course_type,
                        "course_start_time": course_start_time.strip(),
                        "course_end_time": course_end_time.strip(),
                        "course_location": course_location
                    })

                    if course_id not in timetable["courses_list"]:
                        timetable["courses_list"].append(course_id)

    # Print the final timetable for debugging
    print("✅ Final mobile timetable:")
    print(json.dumps(timetable, indent=4))

    return timetable



async def scrape_timetable(user_email: str, user_password: str, update, context):
    try:
        driver.get("https://solss.uow.edu.au/sid/sols_login_ctl.login_app")
        time.sleep(7)

        # Enter email & continue
        driver.find_element(By.NAME, "loginfmt").send_keys("ds374@uowmail.edu.au")
        driver.find_element(By.ID, "idSIButton9").click()
        time.sleep(5)

        # Enter password & continue
        driver.find_element(By.NAME, "passwd").send_keys("fyrT7wvY")
        driver.find_element(By.ID, "idSIButton9").click()
        time.sleep(5)

        # Find OTP code and send to user (Replace with Telegram message logic)
        otp_code = driver.find_element(By.ID, "idRichContext_DisplaySign").text.strip()
        await update.message.reply_text(f"Your OTP number is {otp_code}. Please enter it on your phone.")
        time.sleep(10)

        # Click 'Yes' to stay signed in
        driver.find_element(By.ID, "idSIButton9").click()
        time.sleep(5)

        driver.find_element(By.XPATH, "//a[h2[text()='My Timetable']]").click()
        time.sleep(5)

        timetable = get_mobile_timetable(driver)

        driver.quit()  # Keep browser open
        return timetable

    except Exception as e:
        print(f"❌ Error: {e}")
        return None