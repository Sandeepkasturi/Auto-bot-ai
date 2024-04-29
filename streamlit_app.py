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

# Set up the Generative AI configuration with a placeholder API key
headers = {
    "authorization": st.secrets["api_key"],
    "content-type": "application/json"
}
configure(api_key='')

# Create a Generative Model instance (assuming 'gemini-pro' is a valid model)
model = GenerativeModel('gemini-pro')


# Function to convert plain text to Markdown format
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
    st.markdown("<html>google-site-verification: google543c77f631827437.html</html>", unsafe_allow_html=True)
    st.markdown(
        """<meta name="google-site-verification" content="P_V7QpJhhNnZfjp1lndSh-zM1mwA3nM4o_VnKBmiv_Y"/></meta>""",
        unsafe_allow_html=True)


# Global variable to track whether the VS Code page is Active
colab_code_active = False


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
         **UPI ID's**

         1. Phonepe: 9919932723@ybl
         2. Gpay: sandeepkasturi67@oksbi
         3. Paytm: 9919932723@paytm
         """)

    st.sidebar.markdown("Click here to UPI QR CODE: "
                        f'<a href="https://ibb.co/nBtGVnk" download="downloaded_image.png" alt = "UPI QR"><img src="https://ibb.co/nBtGVnk" width="400"></a>',
                        unsafe_allow_html=True
                        )

    # Display image with a link for download
    st.sidebar.write("Thank you for your support!")

    if page == "🏠 Home":

        st.write("**Below is a quick tutorial video on how to use the application**:")
        # Replace 'video_url' with the URL of your tutorial video
        video_url = "https://youtu.be/i0Q-NBrYpPI"
        # Embed the video with autoplay
        st.video(video_url, start_time=0)
        st.title("Welcome to AutoBot AI")
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

        # Display footer
        display_footer()


    elif page == "AutoBot 🤖":
        st.image("auto_bot_2.png")
        st.header("AutoBot 🤖")
        st.markdown(
            "Ask the AI to generate codes for your use-case. You can now get downloadable files whenever the keyword *CODE* is in your prompt.")
        question = st.text_input("Ask the model a question:")
        if st.button("Ask AI"):
            try:
                # Call your AI model and get the response
                response = model.generate_content(question)
                st.text("AutoBot  Response:")
                st.write(response.text)
                st.markdown('---')
                st.markdown("""Security Note:
    We used .TXT file format for Code downloads which is not easily possible for virus and malware attacks""")
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
    # Add the implementation of the VS Code page to your main Streamlit application
    elif page == "Github CodeSpaces 🖥️":
        global colab_code_active
        colab_code_active = True
        st.header("Github CodeSpaces 🖥️")
        if colab_code_active:
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
        # Update the HTML Editor section

    elif page == "CODEX ⚡":
        st.header("CODEX ⚡️")
        st.info("""
                Welcome to **CODEX** 
                Hi I'm CODEX your interactive CODING GUIDE, No one can explain Code like me Trust me.
                Trust is the Most expensive thing Cheap people can't afford it. 
                1. You can ask specific code or content using the phase @codex "prompt"
                2. You can upload your code here to ask the CODEX to generate Explanation (for eg. @codex Can you explain me this code in the file "filename"
                3. I can Generate 60 queries per minute Pretty wild right, Haha more to see and Explore.
                """)

        st.info("use @codex phase to start the prompt")
        st.info("""Example prompt: @codex explain me the code in the file "your_file_name

        Some popular Prompts:. 
                1. @codex explain me the code in the file app.py
                2. @codex how does this code works in the file app.py


        """)
        prompt = st.text_area('Type your query here:', height=100)
        st.markdown('---')
        uploaded_files = st.file_uploader("Upload code files:", accept_multiple_files=True)
        if st.button('Submit Query'):
            if uploaded_files:
                # Check for the presence of the uploaded file and the query
                if prompt:
                    query_keywords = ["file", "code file", "application"]

                    # Convert prompt to lowercase for case-insensitive comparison
                    prompt_lower = prompt.lower()

                    # Check if any query keyword is present in the prompt
                    if any(keyword in prompt_lower for keyword in query_keywords):
                        # Identify the filename mentioned in the query
                        file_name = None
                        for keyword in query_keywords:
                            if keyword in prompt_lower:
                                # Find the keyword's position in the prompt
                                keyword_idx = prompt_lower.index(keyword)
                                # Extract the filename mentioned after the keyword
                                file_name = prompt[keyword_idx + len(keyword):].strip()
                                break

                        if file_name:
                            # Look for the specified file in the uploaded files
                            requested_file = None
                            for file in uploaded_files:
                                if file_name.lower() in file.name.lower():
                                    requested_file = file
                                    break

                            if requested_file:
                                # Get the contents of the requested file
                                file_contents = requested_file.read().decode("utf-8")

                                # Call the generative model with the file contents as input
                                response = model.generate_content(file_contents)

                                # Display file content and CODEX response
                                st.write(f"Code for {requested_file.name}:")
                                st.code(file_contents)  # Display file content as code

                                st.write("CODEX Response:")
                                st.write(response.text)  # Display model response
                            else:
                                st.error(f"File named '{file_name}' not found among the uploaded files.")
                        else:
                            st.error("Please provide a valid query mentioning the uploaded file.")
                    else:
                        st.error("Please include a keyword ('file', 'code file', 'application') in your query.")
            else:
                st.error("Please upload a file.")
            # Display the compiled HTML
            # display_html(html_code)
        # Display footer
        display_footer()


if __name__ == "__main__":
    main()
