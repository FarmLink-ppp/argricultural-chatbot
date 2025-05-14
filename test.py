def extract_text_file(txt_file):
    try:
        with open(txt_file, "r", encoding="utf-8") as file:
            text = file.read()
            return text
    except Exception as e:
        print(f"Error reading {txt_file}: {e}")
        return None

# Example usage
txt_file = r"C:\Users\bejao\AgriGenius\Data\farmerbook.txt"  # <-- use the new TXT path
text_content = extract_text_file(txt_file)

if text_content:
    print(text_content)
