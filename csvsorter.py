import csv

file1 = "./NonSorted/Naval_Books4.csv"
file2 = "./Sorted/Sorted_Trains4.csv"
sort_by = "Used"
descending = True # True for descending; False for ascending

# Read non-sorted csv file
with open(file1, 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Sort the data based on the specified numeric column in specified order
sorted_data = sorted(data, key=lambda x: float(x[sort_by]), reverse=descending)

# Calculate the total float values for price related numbers
total_used = sum(float(row['Used']) for row in sorted_data)
total_new = sum(float(row['New']) for row in sorted_data)
total_zero = len([row['Used'] for row in sorted_data if float(row['Used']) == 0])


# Write the sorted data to a new CSV file
headers = ["ISBN", "Title", "Author", "Date Published", "MSRP", "New", "Used"]

with open(file2, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(sorted_data)

# Print the statistical data
print(f"Total Used: {total_used}")
print(f"Total New: {total_new}")
print(f"{total_zero}, total with no pricing info")
print(f"{len(sorted_data)}, total entrees")