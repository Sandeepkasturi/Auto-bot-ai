import streamlit as st
import requests
import webbrowser
import os
import time
import base64
from google.generativeai import configure, GenerativeModel
from IPython.display import Markdown
import textwrap
from urllib.parse import quote, urlparse
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# Set up the Generative AI configuration with a placeholder API key
configure(api_key=st.secrets["api_key"])

# Create a Generative Model instance (assuming 'gemini-pro' is a valid model)
model = GenerativeModel('gemini-pro')

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Function to download HTML code
def download_html_code(html_content, url, filename='extracted_html_code.html'):
    try:
        # Extract domain name from the URL
        domain = urlparse(url).netloc
        # Remove any leading 'www.' from the domain name
        domain = domain.replace('www.', '')
        # Construct the filename using the domain name
        filename = f"{domain}_code.html"

        with open(filename, 'w') as file:
            file.write(html_content)
        st.markdown(get_binary_file_downloader_html(filename), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to download HTML code: {e}")


# Function to redirect to VS Code after 5 seconds
# Function to redirect to Colab Code editor after 3 seconds countdown
def colab_code():
    countdown_value = int(10)
    while countdown_value > 0:
        st.write(f" {countdown_value} seconds")
        time.sleep(1)
        countdown_value -= 1

    st.markdown("Redirecting to Codespaces...")
    st.write(webbrowser.open_new_tab("https://github.com/codespaces"))
    st.markdown('---')
    st.info("If application Can't Redirect to the Page use the link below")
    st.markdown("Follow the Link: https://github.com/codespaces")


# Function to extract intent from the user's question
def get_intent(question):
    intents = {
        "tic tac toe": "tic-tac-toe",
        "python ": "Python_code",
        "html ": "html-code",
        # Add more intents and corresponding filenames as needed
    }

    # Find the matching intent in the user's question
    for intent, filename in intents.items():
        if intent in question.lower():
            return filename

    # Default filename if no matching intent is found
    return "generated_code"


# Function to download generated code
def download_generated_code(content, question, format='txt'):
    # Get the intent from the question
    filename = get_intent(question)

    # Determine the file extension based on the format
    if format == 'txt':
        extension = 'txt'
    elif format == 'pdf':
        extension = 'pdf'
    else:
        raise ValueError("Unsupported format. Please choose from 'txt', 'html', or 'pdf'.")

    # Save the content to a temporary file
    temp_filename = f"{filename}.{extension}"
    with open(temp_filename, 'w') as file:
        file.write(content)

    # Create a download link for the temporary file
    with open(temp_filename, 'rb') as file:
        data = file.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/{format};base64,{b64}" download="{filename}.{format}">Download Code ({format.upper()})</a>'
    st.markdown(href, unsafe_allow_html=True)

    # Delete the temporary file after downloading
    os.remove(temp_filename)


# Function to display HTML content
def display_html(html_content):
    # Create a base64 encoded version of the HTML content
    encoded_html = base64.b64encode(html_content.encode()).decode()
    # Create a URL that points to the base64 encoded HTML content
    html_url = f'data:text/html;base64,{quote(encoded_html)}'
    # Create a link that opens the URL in a new tab
    st.markdown(f'<a href="{html_url}" target="_blank">Run on Browser</a>', unsafe_allow_html=True)


# Function to display file download link
def get_binary_file_downloader_html(bin_file, file_label='Download Code'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/html;base64,{b64}" download="{bin_file}" target="_blank">{file_label}</a>'
    return href

# Function to display footer
def display_footer():
    # Additional buttons
    st.markdown('---')
    st.markdown("&copy; 2024 SKAV TECH . All rights reserved.")
    st.subheader('@ Follow on')
    st.markdown("https://bit.ly/socialinstag")

# Main Streamlit application
def main():
    st.sidebar.image("auto_bot_2.png")

    page = st.sidebar.selectbox("Navigate",
                                ["🏠 Home", "AutoBot 🤖", "CODEX ⚡", "Web Scrapper 🌐", "Github CodeSpaces 🖥️"])

    # Donation section
    st.sidebar.title("Donate")
    st.sidebar.info(
        "Support the Project.")
    st.sidebar.info("""
        Payment Details:
         1. **UPI NUMBER: 9919932723**
         2. **Name: Kasturi Sandeep**
         """)

    st.sidebar.markdown("Click here to UPI QR CODE: "
                        f'<a href="https://ibb.co/nBtGVnk" download="downloaded_image.png" alt = "UPI"><img src="https://i.ibb.co/0Kv7WFJ/Google-Pay-QR.png" width="50"></a>',
                        unsafe_allow_html=True
                        )

    # Display image with a link for download
    st.sidebar.write("Thank you for your support ❤️")

    if page == "🏠 Home":
        st.title("Welcome to AutoBot 🤖")
        st.markdown(""" 
        **AutoBot AI**:
         **Functionalities:**
         1. AI Chatbot
         2. CODEX
         3. Web Scrapper
         4. Github Codespaces

        AutoBot, powered by the Gemini API, is a basic chatbot designed for automation. It excels in writing code and generating downloadable files with a .txt extension, offering the ability to handle up to 60 queries per minute.

        Named for its automation capabilities, AutoBot combines "Auto" for continuous work and "Bot" for an intelligent machine that works for you.

        Why choose AutoBot? Unlike other chatbots, AutoBot offers unlimited prompts and responses to the Google AI model, leveraging Gemini-pro. It's particularly effective for basic web development tasks.

        Developed by SKAV TECH, a company focused on creating practical AI projects, AutoBot is intended for educational purposes only. We do not endorse any illegal or unethical activities.""")

        st.write("**Watch the Quick tutorial on how to use the application**:")
        # Replace 'video_url' with the URL of your tutorial video

        if st.button("Tutorial"):
            video_url = "https://youtu.be/i0Q-NBrYpPI"
            # Embed the video with autoplay
            st.video(video_url, start_time=0)

        # Display footer
        display_footer()

    elif page == "AutoBot 🤖":
        st.image("auto_bot_2.png")
        st.header("AutoBot 🤖")
        st.markdown(
            "AutoBot is effective for code generation, if your prompt contains code generation then you can get Downloadable files")
        question = st.text_input("Ask the model a question:")
        if st.button("Ask AI"):
            try:
                # Call your AI model and get the response
                response = model.generate_content(question)
                st.text("AutoBot  Response:")
                st.write(response.text)
                st.markdown('---')
                st.markdown("""Security Note:
                We used **.txt** file format for Code downloads which is not easily possible for virus and malware attacks""")

            except ValueError:
                st.write(
                    "**Sorry 😖, I can't assist you with that. I feel it's sensitive or Confidential or out of my Knowledge. Please ask something else.**")
            except IndexError:
                st.write("**😭 I can't assist you with that Ask something else.**")
            # Check if the response contains a URL
            # if "http" in response.text:
            #   st.write("The response contains a URL.")

            # Check if the question is related to generating code
            code_keywords = ["code", "write code", "develop code", "generate code", "generate", "Build"]
            if any(keyword in question.lower() for keyword in code_keywords):
                download_generated_code(question, response.text)

        # Display footer
        display_footer()

    elif page == "Github CodeSpaces 🖥️":
        st.header("Github CodeSpaces 🖥️")
        st.markdown("Application will start in 10 sec. 😀")
        colab_code()

    elif page == "Web Scrapper 🌐":
        st.header("Web Scrapper")
        st.markdown(
            "AutoBot powered **Web Scrapper**. This tool will get the code of any website. Simply enter the URL below. Download Extracted Code. Upload the Downloaded HTML code in the HTML editor section, then run the application")
        url = st.text_input("Enter URL:")
        if st.button("Extract HTML Code"):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    extracted_html = response.text
                    # Pass the URL to the download_html_code function
                    download_html_code(extracted_html, url)
                else:
                    st.error(f"Failed to retrieve HTML content 😕. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred check the URL 🌐. Or May be system cannot retrieve content 😕 : {str(e)}")
        # Display footer
        display_footer()

    elif page == "CODEX ⚡":
        st.header("CODEX ⚡️")
        uploaded_files = st.file_uploader("Upload code files:", accept_multiple_files=True)
        st.markdown("""
                Welcome to **CODEX** 
                Interactive CODING GUIDE, No one can explain Code like me trust me,
                Trust is the Most expensive thing Cheap people can't afford it. 
                1. You can ask specific code or content using the phase @codex "prompt"
                2. You can upload your code here to ask the CODEX to generate Explanation (for eg. @codex Can you explain me this code in the file "filename"
                3. I can Generate 60 queries per minute Pretty wild right, Haha more to see and Explore.
                """)
        st.info("""Example prompt: @codex explain me the code in the file "your_file_name"

        Some popular Prompts:. 
                1. @codex explain me the code in the file app.py
                2. @codex how does this code works in the file app.py
                3. @codex can you explain me this code how does it works: "paste your code"
        """)
        st.warning("use @codex phase to start the prompt")
        prompt = st.text_area('Type your query here:', height=300)
        st.markdown('---')
        if st.button('Submit'):
            if prompt or uploaded_files:
                if prompt:
                    response = model.generate_content(prompt)
                    st.write("CODEX Response:")
                    st.write(response.text)
                if uploaded_files:
                    for file in uploaded_files:
                        st.write(f"Code for {file.name}:")
                        st.code(file.getvalue())  # Display file content as code
                        # Call the generative model with the file contents as input
                        response = model.generate_content(file.getvalue())
                        st.write("CODEX Response:")
                        st.write(response.text)  # Display model response
            else:
                st.error("Please provide a query or upload a file.")

        # Display footer
        display_footer()

if __name__ == "__main__":
    main()
