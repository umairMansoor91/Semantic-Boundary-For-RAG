import re
from bs4 import BeautifulSoup
import json

# Load HTML file
file_path = "015.htm"
output_file = "015.json"
with open(file_path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Initialize structure
chapters = []
all_contents = []  

# Function to find all hadith numbers in a text block
def extract_hadith_numbers(text):
    # Pattern to match numbers like "575 -" 
    pattern = r'(\d+)\s*-'
    return re.findall(pattern, text)

# First pass: extract all content in order
for block in soup.find_all("div", class_="PageText"):
    # Check for chapter title
    title_tag = block.find("span", class_="title")
    if title_tag:
        all_contents.append({
            "type": "chapter",
            "title": title_tag.text.strip()
        })
        continue
    
    # Convert block to text for easier processing
    block_text = str(block)
    
    # Remove PageHead divs as they're not part of the hadith text
    block_soup = BeautifulSoup(block_text, "html.parser")
    for page_head in block_soup.find_all("div", class_="PageHead"):
        page_head.decompose()
    
    block_text = block_soup.get_text()
    
    # Find all hadith numbers in the block
    hadith_numbers = extract_hadith_numbers(block_text)
    
    if hadith_numbers:
        # Split text by hadith numbers
        parts = re.split(r'(\d+)\s*-', block_text)
        
        # First part is empty or header text, skip it
        parts = parts[1:] 
        
        # Process parts in pairs (number, text)
        for i in range(0, len(parts), 2):
            if i+1 < len(parts):
                hadith_number = parts[i]
                hadith_text = parts[i+1].strip()
                
                
                hadith_text = f"{hadith_number} -{hadith_text}"
                
                all_contents.append({
                    "type": "hadith",
                    "number": hadith_number,
                    "text": hadith_text
                })

# Second pass: organize content into chapters
current_chapter = None

for item in all_contents:
    if item["type"] == "chapter":
        
        if current_chapter:
            
            if current_chapter["hadiths"]:
                current_chapter["verdict"] = current_chapter["hadiths"][-1].copy()
            chapters.append(current_chapter)
        
        current_chapter = {
            "chapter_title": item["title"],
            "hadiths": []
        }
    elif item["type"] == "hadith" and current_chapter is not None:
        
        current_chapter["hadiths"].append({
            "hadith_number": item["number"],
            "text": item["text"]
        })
    elif item["type"] == "hadith" and current_chapter is None:
        # Handle hadiths that appear before any chapter
        # Create a default first chapter if needed
        current_chapter = {
            "chapter_title": "مقدمة الكتاب", 
            "hadiths": [{
                "hadith_number": item["number"],
                "text": item["text"]
            }]
        }

if current_chapter:
    if current_chapter["hadiths"]:
        current_chapter["verdict"] = current_chapter["hadiths"][-1].copy()
    chapters.append(current_chapter)

# Save to JSON

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(chapters, f, ensure_ascii=False, indent=2)

total_hadiths = sum(len(ch["hadiths"]) for ch in chapters)
print(f"Successfully extracted {total_hadiths} hadiths across {len(chapters)} chapters")
print(f"Output saved to {output_file}")