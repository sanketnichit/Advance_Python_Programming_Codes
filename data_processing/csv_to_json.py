import csv
import json

# Input and output file names
input_file = "students.csv"
output_file = "students.json"

try:
    # Open the CSV file
    with open(input_file, "r", newline="") as csv_file:

        # Read CSV data using the first row as keys
        csv_data = csv.DictReader(csv_file)

        # Convert all rows into a list
        records = list(csv_data)

    # Open JSON file for writing
    with open(output_file, "w") as json_file:

        # Write CSV data into JSON format
        json.dump(records, json_file, indent=4)

    print("CSV file successfully converted to JSON.")
    print("Number of records:", len(records))
    print("Output file:", output_file)

except FileNotFoundError:
    print("Error: The CSV file was not found.")

except Exception as e:
    print("Error:", e)