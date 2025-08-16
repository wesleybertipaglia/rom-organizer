import re
from datetime import datetime

# 📥 Read and clean the file
with open("scraper_game_titles.txt", "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file if line.strip()]

# 🔄 Utilities
def is_date(line):
    date_pattern = re.compile(r'^\d{4}$|^[A-Za-z]{3,9} \d{1,2}, \d{4}$|^[A-Za-z]{3,9} \d{4}$')
    return bool(date_pattern.match(line.lower()))

def is_rarity_line(line):
    return line.startswith("×") or line.lower() == "none"

def is_new_title_line(line, next_line):
    return line == next_line

def parse_block(block):
    title_lines = []
    date_str = None

    for line in block:
        line_lower = line.lower()

        if line_lower in ("subset", "bonus", "multi", "none"):
            continue
        elif is_rarity_line(line):
            continue
        elif line_lower == "unknown":
            date_str = "unknown"
            continue
        elif is_date(line):
            date_str = line
        else:
            title_lines.append(line)

    if not title_lines:
        return None, None

    # Remove duplicates and join title lines
    title = " ".join(dict.fromkeys(title_lines)).strip()
    return title, date_str

def extract_year(date_str):
    if not date_str or date_str.lower() == "unknown":
        return 0000
    for fmt in ("%b %d, %Y", "%B %d, %Y", "%B %Y", "%b %Y"):
        try:
            return str(datetime.strptime(date_str, fmt).year)
        except ValueError:
            continue
    try:
        return str(int(date_str))
    except:
        return 0000

# 🔄 Process blocks
blocks = []
current_block = []

for i in range(len(lines)):
    line = lines[i]
    next_line = lines[i + 1] if i + 1 < len(lines) else ""

    if is_new_title_line(line, next_line):
        if current_block:
            blocks.append(current_block)
            current_block = []
        current_block.append(line)
    else:
        current_block.append(line)

# Ensure the last block is processed
if current_block:
    blocks.append(current_block)

# 📦 Extract data
formatted = []
for block in blocks:
    title, date_str = parse_block(block)
    if not title:
        continue
    year = extract_year(date_str)
    formatted.append(f"{year},en-us,{title}")

# 🔤 Order by title
formatted.sort(key=lambda x: x.split(",")[2].lower())

# 💾 Save csv
output = "year,language,title\n" + "\n".join(formatted)

with open("output.csv", "w", encoding="utf-8") as f:
    f.write(output)

print("✅ CSV exported successfully to output.csv")
