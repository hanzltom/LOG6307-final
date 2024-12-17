import pandas as pd

# Load the CSV into a DataFrame
csv_file = "popularity.csv"  # Replace with your CSV file path
data = pd.read_csv(csv_file)

# Ensure proper column names
data.columns = ['Artifact', 'UpdateCount', 'Popularity']

# Convert Popularity to numeric (in case it's not already)
data['Popularity'] = pd.to_numeric(data['Popularity'], errors='coerce')

# Drop rows with invalid or missing Popularity values
data = data.dropna(subset=['Popularity'])

# Sort data by Popularity in descending order and get the top 10
top_10_popular = data.sort_values(by='Popularity', ascending=False).head(10)

# Save the result to a new CSV
top_10_popular.to_csv("top_10_popular_artifacts.csv", index=False)

# Print the result
print(top_10_popular)
