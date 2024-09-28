import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the HTML content from a webpage
def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

# Step 2: Parse the HTML content using BeautifulSoup
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

# Step 3: Extract data from the parsed HTML (customize based on your needs)
def extract_data(tag, soup):
    data = []
    # Example: Extracting all paragraphs
    paragraphs = soup.find_all(tag)
    for para in paragraphs:
        data.append(para.get_text())
    
    return data

# Step 3: Extract data after finding a condition
def extract_data_after_tag(soup, tag_name):
    data_question = []
    # Find the specific tag based on condition (e.g., find the first h2)
    target_tag = soup.find(tag_name)
    paragraphs = soup.find_all(tag_name)
    for para in paragraphs:
        data_question.append(para.get_text())
    
    if target_tag:
        print(f"Found target tag: {target_tag.get_text()}")
        
        # Get the next tags after the target tag
        next_sibling = target_tag.find_next_sibling()  # Find the first next sibling tag
        
        data = []
        while next_sibling:
            if next_sibling.name == 'p':  # Check if the sibling is a paragraph
                data.append(next_sibling.get_text())
            # Move to the next sibling
            next_sibling = next_sibling.find_next_sibling()
        
        return data_question, data
    else:
        print(f"Tag with condition '{tag_name}' not found")
        return []

# Step 4: Write the scraped data into a text file
def write_to_file(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for line in data:
                file.write(line + "\n")
        print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Step 5: Main function to bring it all together
def scrape_page_answer(url, output_file_1, output_file_2, tag_name):
    html_content = get_html(url)
    if html_content:
        soup = parse_html(html_content)
        data_question, data= extract_data_after_tag(soup, tag_name)
        write_to_file(data, output_file_1)
        write_to_file(data_question, output_file_2)
    else:
        print("No HTML content to parse.")

# Step 5: Main function to bring it all together
def scrape_page_question(url, output_file, tag_name):
    html_content = get_html(url)
    if html_content:
        soup = parse_html(html_content)
        data = extract_data(soup, tag_name)
        write_to_file(data, output_file)
    else:
        print("No HTML content to parse.")

if __name__ == "__main__":
    # Example URL (you can change this to any URL)
    url = "https://consensys.io/knowledge-base/blockchain-super-faq"
    output_file_1 = "answer.txt"  # Specify your output file name
    output_file_2 = "question.txt"  # Specify your output file name
    tag_name = "h4"  # Specify the tag to find

    # Run the scraper and save the output
    scrape_page_answer(url, output_file_1, output_file_2, tag_name)
    # scrape_page_question(url, output_file_2, tag_name)
