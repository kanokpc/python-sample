import requests

def read_google_docs(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.content
        else:
            data = f"Failed to retrieve document. Status code: {response.status_code}"
    except Exception as e:
        data = f"An error occurred: {e}"
    
    return data

def extract_table_data(doc):
    from bs4 import BeautifulSoup
    import pandas as pd

    # Sample HTML content
    html_content = doc

    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')

    # Find the table
    table = soup.find('table')

    # Extract table rows
    rows = []
    for row in table.find_all('tr')[1:]:  # Skip header row
        cells = [cell.text for cell in row.find_all('td')]
        rows.append(cells)

    # Create a DataFrame
    df = pd.DataFrame(rows)

    return df

def create_grid(width, height):
    return [[' ' for _ in range(width)] for _ in range(height)]

def print_grid(grid):
    for row in grid:
        print(''.join(row))

def place_character(grid, x, y, char):
    if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
        grid[y][x] = char
        
# read google docs
docs = read_google_docs('https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub')

# extract html table
docstable = extract_table_data(docs)

# find columns and rows count
width = len(docstable.columns)
height = len(docstable.index)

grid = create_grid(width, height)

# Place characters at specific coordinates
for index, row in docstable.iterrows():
    #print(row['c1'], row['c2'])
    place_character(grid, int(row[0]), int(row[2]), row[1])

# Print the grid
print_grid(grid)