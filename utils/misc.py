import datetime
import uuid

# Function to generate a unique cardId
def generate_unique_card_id():
    return f"image_card_{int(datetime.datetime.now().timestamp())}_{uuid.uuid4().hex[:6]}"

def get_docs(doc_name: str) -> str:
    try:
        # Construct the file path based on the doc_name
        file_path = f'docs/{doc_name}.md'
        
        # Read the specified markdown file
        with open(file_path, 'r') as file:
            content = file.read()

        # Split the content at the "---" header line and get the second part
        doc_content = content.split("---", 2)[-1].strip()

        return doc_content

    except Exception as e:
        print(f"Error reading {doc_name} content: {str(e)}")
        return f'Sorry, I encountered an error retrieving the {doc_name} content.'
