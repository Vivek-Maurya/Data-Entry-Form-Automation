import pandas as pd
from playwright.sync_api import sync_playwright

# --- CONFIGURATION ---
EXCEL_FILE = "C:/Users/Vivek Maurya/Desktop/HCAH No Kit Enrolled.xlsx"  # Make sure this file is in the same directory
URL = 'https://hridayampsp.com/login' # **CHANGE THIS to your target website URL**

# --- LOCATORS (The 'map' to your website's form fields) ---
# You will need to inspect your website's form fields (using Developer Tools)
# and replace the example locators (e.g., '#name-field') with the correct ones.
LOCATORS = {
    'UID':           '//*[@id="email"]',
    'Pass':          '//*[@id="password"]',
    'Go':            '//*[@id="loginButton"]',
    'Pinfo':         '//html/body/div[2]/div[1]/div/div/div/ul/li[4]/a',

    'Dr Name':       '//*[@id="hcp_name"]',       # Use 'select' for dropdowns or radio button group
    'Patient Name':  '//*[@id="patient_name"]',   
    'Age':           '//*[@id="age"]',           # Use 'select' for dropdowns or radio button group
    'Mobile Number': '//*[@id="mobile_number"]',
    'Gender':        '//*[@id="gender"]',        # Use 'select' for dropdowns or radio button group
    'Comp':          '//html/body/div[1]/div[3]/div/form/div/div[3]/div[2]/div[5]/div[4]/div[2]/div/div/span/span[1]/span/span/textarea',
    'Heart Rate':    '//*[@id="heart_rate"]',
    'Weight':        '//*[@id="weight"]',
    'Height':        '//*[@id="height"]',
    
    'CBP':           '//html/body/div[1]/div[3]/div/form/div/div[3]/div[2]/div[3]/div[1]/div/div/span[2]/label',
    'PA':            '//html/body/div[1]/div[3]/div/form/div/div[3]/div[2]/div[4]/div[1]/div/div/span[2]/label',
    'PE':            '//html/body/div[1]/div[3]/div/form/div/div[3]/div[2]/div[5]/div[1]/div/div/span[2]/label/input',
    
    'T2DM':          '//html/body/div[1]/div[3]/div/form/div/div[6]/div/div/div[4]/div[1]/div[4]/div[1]/div/div/span[1]/label/input',
    
    'HPT':           '//html/body/div[1]/div[3]/div/form/div/div[6]/div/div/div[4]/div[1]/div[4]/div[2]/div/div/span[1]/label/input',
    
    'DYS':           '//html/body/div[1]/div[3]/div/form/div/div[6]/div/div/div[4]/div[1]/div[4]/div[3]/div/div/span[2]/label/input',
    
    'PCO':           '//html/body/div[1]/div[3]/div/form/div/div[6]/div/div/div[4]/div[1]/div[4]/div[4]/div/div/span[2]/label/input',
    
    'KPN':           '//html/body/div[1]/div[3]/div/form/div/div[6]/div/div/div[4]/div[1]/div[4]/div[5]/div/div/span[2]/label/input',
    
    'AST':           '//html/body/div[1]/div[3]/div/form/div/div[6]/div/div/div[4]/div[1]/div[4]/div[6]/div/div/span[2]/label/input',
    
    'BTH':           '//html/body/div[1]/div[3]/div/form/div/div[6]/div/div/div[4]/div[3]/div[4]/div[1]/div/div/span[1]/label/input',
    
    'DRS':           '//html/body/div[1]/div[3]/div/form/div/div[6]/div/div/div[4]/div[3]/div[4]/div[2]/div/div/span[2]/label/input',
    
    'WLK':           '//html/body/div[1]/div[3]/div/form/div/div[6]/div/div/div[4]/div[3]/div[4]/div[3]/div/div/span[1]/label/input',
    
    'TLT':           '//html/body/div[1]/div[3]/div/form/div/div[6]/div/div/div[4]/div[3]/div[4]/div[4]/div/div/span[1]/label/input',
    
    'Submit':        '//*[@id="submit"]'         # Selector for the final submission button
}
# ---------------------

def automate_data_entry():
    # 1. READ DATA FROM EXCEL
    try:
        # Assuming your Excel file has a sheet named 'Sheet1' and columns like 'Name', 'Email', 'Value'
        df = pd.read_excel(EXCEL_FILE, sheet_name='Sheet1')
        print(f"Successfully loaded {len(df)} rows from '{EXCEL_FILE}'.")
    except FileNotFoundError:
        print(f"ERROR: Excel file '{EXCEL_FILE}' not found. Please create it.")
        return
    except KeyError as e:
        print(f"ERROR: Column {e} missing in the Excel file. Check your column names.")
        return

    # 2. START WEB AUTOMATION WITH PLAYWRIGHT
    # 'headless=False' makes the browser visible so you can watch the process
    USER_DATA_DIR = "C:/Users/Vivek Maurya/Desktop/playwright_user_data"
    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=False)
        # page = browser.new_page()
        
        browser = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False
        )
        # When using persistent context, the context *is* the browser, 
        # and you get a page from it.
        page = browser.pages[0] if browser.pages else browser.new_page() 


        row_count = 0
        success_count = 0

        # Login
        page.goto(URL, wait_until='networkidle')

        uid = input('Enter the EMP ID: ')
        password = input('Enter the Password: ')
        page.fill(LOCATORS['UID'], uid)
        page.fill(LOCATORS['Pass'], password)
        page.click(LOCATORS['Go'])
        page.click(LOCATORS['Pinfo'])

        for index, row in df.iterrows():
            row_count += 1
            print(f"\n--- Processing Row {row_count} (Index {index}) ---")

            try:
                
                # Extract data for the current row

                dname = str(row['Dr Name'])
                pname = str(row['Patient Name'])
                age = str(row['Age'])
                mnumber = str(row['Mobile Number'])
                gender = str(row['Gender'])
                comp = 'N/A'
                hrate = str(row['Heart Rate'])
                weight = str(row['Weight'])
                height = str(row['Height'])



                print(f"   -> EMP ID      : '{uid}'")
                print(f"   -> Password    : '{password}'")
                print(f"   -> Dr Name     : '{dname}'")
                print(f"   -> Patient Name: '{pname}'")
                print(f"   -> Age         : '{age}'")
                print(f"   -> Number      : '{mnumber}'")
                print(f"   -> Gender      : '{gender}'")
                print(f"   -> Competitor  : '{comp}'")
                print(f"   -> Heart Rate  : '{hrate}'")
                print(f"   -> Weight      : '{weight}'")
                print(f"   -> Height      : '{height}'")

                # Fill the form fields using the data and the locators

                page.select_option(LOCATORS['Dr Name'], dname)
                page.fill(LOCATORS['Patient Name'], pname)
                page.select_option(LOCATORS['Age'], age)
                page.fill(LOCATORS['Mobile Number'], mnumber)
                page.select_option(LOCATORS['Gender'], gender)
                
                
                page.click(LOCATORS['CBP'])
                page.click(LOCATORS['PA'])
                page.click(LOCATORS['PE'])
                
                page.fill(LOCATORS['Comp'], comp)
                page.keyboard.press('Enter')
                page.mouse.click(1000,50)
                
                
                
                # page.fill(LOCATORS['Heart Rate'], hrate)
                page.fill(LOCATORS['Weight'], weight)
                page.fill(LOCATORS['Height'], height)
                
                page.click(LOCATORS['T2DM'])
                page.click(LOCATORS['HPT'])
                page.click(LOCATORS['DYS'])
                page.click(LOCATORS['PCO'])
                page.click(LOCATORS['KPN'])
                page.click(LOCATORS['AST'])
                page.click(LOCATORS['BTH'])
                page.click(LOCATORS['DRS'])
                page.click(LOCATORS['WLK'])
                page.click(LOCATORS['TLT'])
                #page.click(LOCATORS['Submit'])
                

                # Click the submit button
                # page.click(LOCATORS['Submit'])

                # Optional: Add a check to confirm submission success
                # This check will be highly specific to your website (e.g., checking for a success message)
                # For this example, we'll just wait a moment.
                page.wait_for_timeout(4000) # Wait 1 second (adjust as needed)
                page.reload()
                print("   -> Data successfully submitted.")
                success_count += 1

            except Exception as e:
                print(f"ERROR processing row {row_count}: {e}")
                # You might want to log the failed row for later manual review

        # 3. CLEANUP
        # browser.close()

        print("\n==============================================")
        print(f"Automation Complete: {success_count} of {row_count} rows submitted successfully.")
        print("==============================================")


if __name__ == "__main__":
    automate_data_entry()