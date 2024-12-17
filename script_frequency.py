import pandas as pd
import matplotlib.pyplot as plt
import glob

# Define file pattern for the CSV files
file_pattern = "rq2.*.csv"  # Adjust this pattern if the files are stored in a specific folder

# Initialize an empty DataFrame to store results
all_results = pd.DataFrame()

# Process each CSV file
for file in glob.glob(file_pattern):
    # Load the CSV into a DataFrame
    data = pd.read_csv(file)
    
    # Ensure proper column names
    data.columns = ['Project', 'Dependency', 'Version', 'ReleaseTimestamp']
    
    # Filter rows with invalid versions (non-numeric major versions)
    valid_versions = data['Version'].str.match(r'^\d+\.\d+.*$')
    data = data[valid_versions]
    
    # Extract the major version from the Version column
    data['MajorVersion'] = data['Version'].str.split('.').str[0].astype(int)
    
    # Sort data by Project and MajorVersion
    data = data.sort_values(by=['Project', 'MajorVersion'])
    
    # Identify new major releases
    data['IsNewMajorRelease'] = data.groupby('Project')['MajorVersion'].diff().fillna(0) != 0
    
    # Count the total number of releases and new major releases for each project
    result = (
        data.groupby('Project')
        .agg(
            TotalReleases=('Version', 'size'),
            NewMajorReleases=('IsNewMajorRelease', 'sum')
        )
        .reset_index()
    )
    
    # Calculate the percentage of major releases
    result['PercentMajorReleases'] = (result['NewMajorReleases'] / result['TotalReleases']) * 100
    
    # Append the result to the combined DataFrame
    all_results = pd.concat([all_results, result], ignore_index=True)

# Plot the percentage of major releases for all projects
plt.figure(figsize=(12, 8))
plt.bar(all_results['Project'], all_results['PercentMajorReleases'], color='skyblue')
plt.title('Percentage of Major Releases per Project (Combined)', fontsize=14)
plt.xlabel('Project', fontsize=12)
plt.ylabel('Percentage of Major Releases (%)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Save the plot
plt.savefig('combined_percent_major_releases.png')
plt.show()
