import csv
import os
import glob

path = "./*.csv" # All CSV files that need to be combined
output = "./NonSorted/Train_All.csv"

csv_files = glob.glob(path) # get all files that end in .csv in dir

combined_data = []

# Open each file and append it to new list
for file in csv_files:
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            combined_row = row
            combined_data.append(combined_row)


# write the non sorted data to file
with open(output, 'w', newline='') as f_output:
    writer = csv.writer(f_output)
    writer.writerows(combined_data)


# Print some data 
print(f"success {output}")
print(f"total: {len(combined_data)}")


# delete files that just got combined
for f in csv_files:
    os.remove(f)