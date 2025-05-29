from scripts.clean_main_file import CleanMainFile
from scripts.calculate_productivity import CalculateProductivity
import json
import os


print("Starting the script")

# read the json file relative to this script's location
parameters_path = os.path.join(os.path.dirname(__file__), "initial_parameters.json")
with open(parameters_path, "r") as infile:
    data = json.load(infile)

# extract the required data
emails_to_delete = data["EMAILS_TO_DELETE"]
year = data["YEAR"]
month = data["MONTH"]
coefficients = data["COEFFICIENTS"]

year_month = f"{year}-{str(month).zfill(2)}"
path = f"C:\\Productividad\\{year_month}\\"

my_cleaner = CleanMainFile(path, year, month, emails_to_delete)
cleaned_main_excel_file = my_cleaner.clear_data()

my_productivity = CalculateProductivity(path, year, month, coefficients)
df_productivity = my_productivity.calculate_productivity()
my_productivity.final_table()

