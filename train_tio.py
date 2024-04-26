import os
import pandas as pd
import csv

# Define the directory where you want to save the CSV file
output_directory = "C:/Users/Nitesh Jaiswar/OneDrive/Desktop/example/"

# Create the full path to the CSV file
csv_file_path = os.path.join(output_directory, "examples.csv")

# Load the 'movie_data.csv' file
movie_data = pd.read_csv("movie_data.csv")

# Prepare the data for appending to the CSV file
data_to_append = []


for index, row in movie_data.iterrows(200):
    genre = row['Genre(s)']
    synopsis = row['Synopsis']
    if isinstance(genre, str) and isinstance(synopsis, str):
        data_to_append.append((synopsis, genre))

# Append the new data to the CSV file
with open(csv_file_path, mode="a", newline="") as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for data in data_to_append:
        writer.writerow(data)

print("Data has been appended to 'examples.csv' in the specified directory.")
