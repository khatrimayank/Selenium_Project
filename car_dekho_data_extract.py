from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd

# chrome_options = Options()

# chrome_options.add_argument("--headless")

url = "https://www.cardekho.com/newcars"

# driver=webdriver.Chrome(options=chrome_options)

driver = webdriver.Chrome()

driver.get(url)

driver.maximize_window()

time.sleep(1)

all_brand_links = []

all_model_links = []

MAKE_MODEL = []
Engine_Type = []
Engine_Displacement = []
Transmission_Type = []
Fuel_Type = []
Mileage = []
Tank_Capacity = []
Front_Suspension = []
Rear_Suspension = []
Entertainment_Details = []


def row_data_to_dict(rows_data):
    row_dict = {}
    for i in range(0, len(rows_data), 2):
        key = rows_data[i]
        value = rows_data[i + 1] if i + 1 < len(rows_data) else "N/A"
        row_dict[key] = value
    return row_dict


# extract links of all brands
all_brands = driver.find_elements(By.XPATH, '//div[@data-track-section="Current"]//a')

for brand in all_brands:

    # link for current brand
    brand_link = brand.get_attribute("href")

    all_brand_links.append(brand_link)

    # Open the link in a new tab
    driver.execute_script("window.open('{}', '_blank');".format(brand_link))

    time.sleep(1)  # Wait for the new tab to open

    # Switch to the newly opened tab
    driver.switch_to.window(driver.window_handles[-1])

    time.sleep(1)

    # extract links of all models
    all_models = driver.find_elements(By.XPATH, '//ul[@class="modelList"]//a')

    count = 0

    for model in all_models:

        if count % 2 == 0:

            try:
                make_model = model.text
                # print("make model : ", make_model)
                MAKE_MODEL.append(model.text)

            except Exception as e:
                MAKE_MODEL.append("N/A")
                make_model = "n/a"

            # link of current model

            model_link = model.get_attribute("href")

            # print("model link ", model_link)

            all_model_links.append(model_link)

            # store the handle of current tab
            current_tab = driver.current_window_handle

            # open cuurent model link in new tab
            driver.execute_script("window.open('{}', '_blank');".format(model_link))

            time.sleep(1)  # Wait for the new tab to open

            # handle of newly openend tab
            new_tab_handle = driver.window_handles[-1]

            # switch to new tab
            driver.switch_to.window(new_tab_handle)

            time.sleep(1)

            retries = 3

            count = 0
            for _ in range(retries):
                try:
                    element = WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "div.BottomLinkViewAll > a")
                        )
                    )

                    element.click()
                    break
                except Exception as e:
                    time.sleep(1)
                    count += 1

            if count == 3:
                Engine_Type.append("N/A")
                Engine_Displacement.append("N/A")
                Transmission_Type.append("N/A")
                Fuel_Type.append("N/A")
                Mileage.append("N/A")
                Tank_Capacity.append("N/A")
                Front_Suspension.append("N/A")
                Rear_Suspension.append("N/A")
                Entertainment_Details.append("N/A")
                continue

            engine_table = []
            fuel_table = []
            suspension_table = []
            enterntainment_table = []

            for _ in range(
                3
            ):  # (By.XPATH,"//*[@id='scrollDiv']//h3[contains(@id, 'Engine')]/following-sibling::table")

                try:
                    engine_table = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "#scrollDiv > h3[id*='Engine'] + table")
                        )
                    )
                    break
                except Exception as e:
                    print("for model {} engine table cant extracted".format(make_model))
                    time.sleep(1)

            for _ in range(3):
                try:
                    fuel_table = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "#scrollDiv > h3[id*='Fuel'] + table")
                        )
                    )
                    break
                except Exception as e:
                    print("for model {} fuel table cant extracted".format(make_model))
                    time.sleep(1)

            for _ in range(3):
                try:
                    suspension_table = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "#scrollDiv > h3[id*='Suspension'] + table",
                            )
                        )
                    )
                    break
                except Exception as e:
                    print(
                        "for model {} Suspension table cant extracted".format(
                            make_model
                        )
                    )
                    time.sleep(1)

            for _ in range(3):
                try:
                    enterntainment_table = WebDriverWait(driver, 1).until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                "#scrollDiv > h3[id*='Entertainment'] + table",
                            )
                        )
                    )
                    break
                except Exception as e:
                    print(
                        "for model {} enterntainment table cant extracted".format(
                            make_model
                        )
                    )
                    time.sleep(1)

            data_list = []

            for table in [
                engine_table,
                fuel_table,
                suspension_table,
                enterntainment_table,
            ]:

                if not table:
                    print("No data in table")
                    continue
                try:
                    table_row_data = table.find_elements(By.XPATH, ".//tr//td")

                    for row_data in table_row_data:

                        if row_data.text == "Report Incorrect Specs":

                            continue

                        data_list.append(row_data.text)
                except Exception as e:
                    pass

            data_dict = row_data_to_dict(data_list)

            try:
                Engine_Type.append(
                    data_dict.get("Engine Type", data_dict.get("Battery Type", "N/A"))
                )

            except Exception as e:
                Engine_Type.append("N/A")

            try:
                Engine_Displacement.append(
                    data_dict.get("Displacement", data_dict.get("Motor Power", "N/A"))
                )

            except Exception as e:
                Engine_Displacement.appen("N/A")

            try:
                Transmission_Type.append(data_dict.get("Transmission Type", "N/A"))

            except Exception as e:
                Transmission_Type.append("N/A")

            try:
                Fuel_Type.append(data_dict.get("Fuel Type", "N/A"))
                fuel_type = Fuel_Type[-1]

            except Exception as e:
                Fuel_Type.append("N/A")

            try:
                Mileage.append(
                    data_dict.get(
                        str(fuel_type) + " Mileage ARAI",
                        data_dict.get(
                            str(fuel_type) + " Mileage WLTP",
                            data_dict.get("Range", "N/A"),
                        ),
                    )
                )
            except Exception as e:
                Mileage.append("N/A")

            try:
                Tank_Capacity.append(
                    data_dict.get(
                        str(fuel_type) + " Fuel Tank Capacity",
                        data_dict.get("Battery Capacity", "N/A"),
                    )
                )

            except Exception as e:
                Tank_Capacity.append("N/A")

            try:
                Front_Suspension.append(data_dict.get("Front Suspension", "N/A"))

            except Exception as e:
                Front_Suspension.append("N/A")

            try:
                Rear_Suspension.append(data_dict.get("Rear Suspension", "N/A"))

            except Exception as e:
                Rear_Suspension.append("N/A")

            try:
                keys_to_get = [
                    "Touch Screen size",
                    "Connectivity",
                    "Tweeters",
                    "Additional Features",
                ]

                temp = {}

                for key in keys_to_get:

                    temp[key] = data_dict.get(key, "N/A")

                Entertainment_Details.append(temp)

            except Exception as e:
                Entertainment_Details.append("N/A")

            # close the current model tab
            driver.close()

            # switch window handle to curent tab
            driver.switch_to.window(current_tab)

        count += 1

    driver.close()

    driver.switch_to.window(driver.window_handles[0])

# print(all_model_links)
df = pd.DataFrame(
    {
        "MAKE_MODEL": MAKE_MODEL,
        "ENGINE_TYPE/BATTERY_TYPE": Engine_Type,
        "ENGINE_DISPLACEMENT(CC)/MOTOR_POWER(KW)": Engine_Displacement,
        "TRANSMISSION_TYPE": Transmission_Type,
        "FUEL_TYPE": Fuel_Type,
        "MILEAGE/Range": Mileage,
        "TANK_CAPACITY/BATTERY_CAPACITY": Tank_Capacity,
        "FRONT_SUSPENSION": Front_Suspension,
        "REAR_SUSPENSION": Rear_Suspension,
        "Entertainment_Details": Entertainment_Details,
    }
)

df.to_csv("CAR_DETAILS_FROM_CAR_DEKHO.csv")
