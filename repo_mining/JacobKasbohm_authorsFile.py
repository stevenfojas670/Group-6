import subprocess
import csv
import os

# Function to read source files from a CSV file
def get_source_files_from_csv(csv_filename):
    source_files = []
    
    with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row

        # Iterate over the rows in the CSV file
        for row in reader:
            if row:  # Skip empty rows
                source_files.append(row[0])  # Assuming filenames are in the first column
    
    return source_files

# Function to collect the authors and dates when they touched each file
def collect_authors_and_dates(source_files, repo_dir):
    authors_and_dates = {}
    
    # Ensure we are in the correct directory (the local repo directory)
    os.chdir(repo_dir)

    for file in source_files:
        # Git log command to get all authors and commit dates for each file
        try:
            # The git command to get all authors and commit dates for the file
            command = [
                'git', 'log', '--format=%an %ad', '--date=short', '--', file
            ]
            result = subprocess.check_output(command, stderr=subprocess.PIPE).decode('utf-8')

            # Split the result into lines and collect the author/date
            lines = result.strip().split('\n')
            authors_and_dates[file] = []

            if lines:
                for line in lines:
                    # Split the line into author and date
                    # Assuming the first space separates the author from the date
                    parts = line.split(' ', 2)  # Split into at most 3 parts: First name, Last name, Date
                    if len(parts) == 3:
                        authorFirst, authorLast, date = parts
                        # Append the author and date tuple
                        authors_and_dates[file].append((authorFirst, authorLast, date))

        except subprocess.CalledProcessError as e:
            print(f"Error while processing file {file}: {e}")
        except FileNotFoundError:
            print(f"Error: Git repository not found in {repo_dir}")

    return authors_and_dates

# Main function to collect and display the data
def main():
    # Specify the CSV file containing the list of source files
    csv_filename = r'data\file_rootbeer.csv'  # Use a raw string literal for Windows path
    repo_dir = r'rootbeer'  # Your local Git repository path

    # Get the source files from the CSV
    source_files = get_source_files_from_csv(csv_filename)
    
    # Collect authors and commit dates for the source files
    authors_and_dates = collect_authors_and_dates(source_files, repo_dir)
    
    # Ensure the 'data' directory exists
    if not os.path.exists('data'):
        os.makedirs('data')  # Create the 'data' directory if it doesn't exist

    # Output to CSV
    output_file = r'data\file_authors_and_dates.csv'
    rows = ['FileName', 'Author First Name', 'Author Last Name', 'Date']
    with open(output_file, 'w') as fileCSV:
        writer = csv.writer(fileCSV)
        writer.writerow(rows)

        # Output the results
        i=0
        for file in source_files:
            if file in authors_and_dates:
                # Iterate through the author/date information for each file
                print(file)
                for authorFirst, authorLast, date in authors_and_dates[file]:
                    writer.writerow([file, authorFirst, authorLast, date])
                    print(  authorFirst, authorLast, date)
                i += 1
    print("Files found = ", i)
if __name__ == "__main__":
    main()
