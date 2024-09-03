# CarDekho Data Extraction Script

## Introduction

The CarDekho Data Extraction Script is a Python-based tool designed to extract detailed car specifications from the CarDekho website. The script automates the process of gathering information about various car models, including engine type, fuel type, transmission type, mileage, suspension details, and entertainment features, and stores the data in a CSV file.

## Script Functionality

### Data Extraction
- The script extracts car specifications for different models available on the CarDekho website. Each car is defined by attributes such as "make", "model", "engine type", "fuel type", "transmission type", "mileage", "tank capacity", "suspension details", and "entertainment features".

### Automated Web Scraping
- Using Selenium, the script automates the browsing process, opening brand and model pages, extracting relevant data, and saving the information into a CSV file.

## Requirements
- Python 3.x
- Selenium
- ChromeDriver
- pandas

## How to Run

1. **Install Dependencies:**
   - Make sure you have Python installed along with the required packages:
     ```bash
     pip install selenium pandas
     ```
   - Also, ensure that the ChromeDriver is installed and is compatible with your version of Chrome.

2. **Run the Script:**
   - Navigate to the directory containing the script and execute it:
     ```bash
     python car_dekho_data_extract.py
     ```

3. **Output:**
   - The extracted data will be saved into a CSV file named `CAR_DETAILS_FROM_CAR_DEKHO.csv`.

## Edge Cases Handled

- The script handles cases where car models might not have all the specified attributes available.
- If a webpage fails to load or an attribute is missing, the script assigns a default value of "N/A".

## Testing

- The script is designed to handle different scenarios, such as pages not loading correctly or certain data not being available.
- Test the script by running it for different car brands and models to ensure it captures data accurately.

## Author

[Mayank Khatri]
