import base64
import requests
import os
from dotenv import load_dotenv


# Load the environment variables from the .env file
load_dotenv()

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

# Ensure API key is available
if not api_key:
    raise ValueError("No API key found. Please set your OPENAI_API_KEY in the .env file.")


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "images/img_3.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


# Text content sections

test_prompts = {
    "1": "I'm sending you an image of a document. Please extract the text and categorize it into three parts: the Title, the Body, and the Footer. The Title is often times at the top but not always, bold font, or all caps. Be carful not to extract the wrong text for the title, use context clues to determine the title, the title will always be centered wherever it is on the page. The Body is the main content that follows the title and contains the core message, keep in mind that the body will be inbetween the title and footer which will be both be centered in the middle of the page so use that as refernce. The Footer directly follows the body and includes names of organizations or societies. The footer is similar to the title in that its centered wherver it is on the page.",
    "2": "I'm sending you an image of a document used to make historical signs. Please extract the text that would pertain to a historical sign and categorize it into three parts: the Title, the Body, and the Footer. The Title is often times at the top but not always, bold font, or all caps. Be carful not to extract the wrong text for the title, use context clues to determine the title remeber that the text we need will be on a historical sign so remember that for context, the title will always be centered wherever it is on the page. The Body is the main content that follows the title and contains the core message, remember that is historical information that will be on a sign so use that for context when finding the text, keep in mind that the body will be inbetween the title and footer which will be both be centered in the middle of the page so use that as refernce. The Footer directly follows the body and includes names of organizations or societies, the footer is similar to the title in that its centered wherver it is on the page, remeber that the text will be on a historical sign so keep that in mind when finding the footer.",
    "3": "I'm sending you an image of a document used to make historical signs. Please extract the text that would pertain to a historical sign and categorize it into three parts: the Title, the Body, and the Footer. Format your response as follows:\n\nTitle: [Extracted Title]\nBody: [Extracted Body]\nFooter: [Extracted Footer]\n\nNote: The Title is often at the top but not always, and it may be in bold font or all caps. Be careful not to extract the wrong text for the title, use context clues to determine the title, remember that the text we need will be on a historical sign so remember that for context, the title will always be centered wherever it is on the page. The Body is the main content that follows the title and contains the core message, remember that it is historical information that will be on a sign so use that for context when finding the text, keep in mind that the body will be between the title and footer which will both be centered in the middle of the page so use that as reference. The Footer directly follows the body and includes names of organizations or societies, the footer is similar to the title in that it's centered wherever it is on the page, remember that the text will be on a historical sign so keep that in mind when finding the footer.",
    "4": "I'm sending you an image of a document used to make historical signs. Please extract and categorize the text (that would pertain to a historical sign) from the image strictly into three parts: Title, Body, and Footer. Format your response as follows:\n\nTitle: [Extracted Title]\nBody: [Extracted Body]\nFooter: [Extracted Footer]\n\nDo not add any interpretations, explanations, or commentary beyond the direct extraction. Note: The Title is often at the top but not always, and it may be in bold font or all caps. Be careful not to extract the wrong text for the title, use context clues to determine the title, remember that the text we need will be on a historical sign so remember that for context, the title will always be centered wherever it is on the page. The Body is the main content that follows the title and contains the core message, remember that it is historical information that will be on a sign so use that for context when finding the text, keep in mind that the body will be between the title and footer which will both be centered in the middle of the page so use that as reference. The Footer directly follows the body and includes names of organizations or societies, the footer is similar to the title in that it's centered wherever it is on the page, remember that the text will be on a historical sign so keep that in mind when finding the footer.",
}




payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": test_prompts["3"]
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    response_json = response.json()

    print(response_json)

    # Extract the 'content' section of the message
    content = response_json['choices'][0]['message']['content']

    # Assuming the content is a string, split the content by its sections
    sections = content.split('\n\n')

    # Extracting each section
    title = sections[0].replace('Title:', '').strip()
    body = sections[1].replace('Body:', '').strip()
    footer = sections[2].replace('Footer:', '').strip()

    # Print the extracted parts in a nice format
    print(f"Title:\n{title}\n")
    print(f"Body:\n{body}\n")
    print(f"Footer:\n{footer}\n")
else:
    print("Failed to get a successful response from the API")