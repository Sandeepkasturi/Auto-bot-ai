import streamlit as st
import requests
import webbrowser
import os
import time
import base64
from google.generativeai import configure, GenerativeModel
from urllib.parse import urlparse

# Set up the Generative AI configuration with a placeholder API key
configure(api_key=st.secrets["api_key"])

# Create a Generative Model instance (assuming 'gemini-pro' is a valid model)
model = GenerativeModel('gemini-pro')

# Function to download HTML code
def download_html_code(html_content, url):
    try:
        domain = urlparse(url).netloc.replace('www.', '')
        filename = f"{domain}_code.html"
        with open(filename, 'w') as file:
            file.write(html_content)
        st.markdown(get_binary_file_downloader_html(filename), unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to download HTML code: {e}")

# Function to redirect to GitHub Codespaces
def redirect_to_codespaces():
    with st.spinner("Redirecting to GitHub Codespaces..."):
        time.sleep(2)
    webbrowser.open_new_tab("https://github.com/codespaces")
    st.info("If the application can't redirect, use the link below:")
    st.markdown("[GitHub Codespaces](https://github.com/codespaces)")

# Function to download generated code
def download_generated_code(content, filename, format='txt'):
    extension = format
    temp_filename = f"{filename}.{extension}"
    with open(temp_filename, 'w') as file:
        file.write(content)
    with open(temp_filename, 'rb') as file:
        data = file.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/{format};base64,{b64}" download="{filename}.{format}">Download Code ({format.upper()})</a>'
    st.markdown(href, unsafe_allow_html=True)
    os.remove(temp_filename)

# Function to display file download link
def get_binary_file_downloader_html(bin_file, file_label='Download Code'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/html;base64,{b64}" download="{bin_file}" target="_blank">{file_label}</a>'
    return href

# Function to display footer
def display_footer():
    footer_html = """
    <style>
    .footer {
        padding: 10px;
        background-color: pink;
        text-align: center;
        border-top: 1px solid #e1e1e1;
        font-family: 'Arial', sans-serif;
    }
    </style>
    <div class="footer">
        <p style="color: red;"><big>&copy; 2024 SKAV TECH. All rights reserved. | Follow us on <a href="https://bit.ly/socialinstag">Instagram</a></big></p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# Function to fetch YouTube video suggestions
def fetch_youtube_videos(query):
    api_key = st.secrets["youtube_api_key"]
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 4,
        "key": api_key
    }
    response = requests.get(search_url, params=params)
    video_details = []
    if response.status_code == 200:
        results = response.json()["items"]
        for item in results:
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            video_details.append({
                "title": video_title,
                "url": video_url,
                "video_id": video_id
            })
    else:
        st.error(f"Failed to fetch YouTube videos 😭. Status code: {response.status_code}")
    return video_details

# Function to extract the main topic from the prompt
def extract_topic(prompt):
    start_phrase = "@codex" or "codex" or "@autobot"
    if prompt.lower().startswith(start_phrase):
        topic = prompt[len(start_phrase):].strip()
    else:
        topic = prompt.strip()
    return topic

# Main Streamlit application
def main():
    st.set_page_config(page_title="AutoBot AI", page_icon="🤖", layout="wide")

    st.sidebar.image("auto_bot_2.png", use_column_width=True)
    page = st.sidebar.selectbox("Navigate",
                                ["🏠 Home", "AutoBot 🤖", "CODEX ⚡", "Web Scrapper 🌐", "GitHub Codespaces 🖥️"])

    st.sidebar.title("Donate")
    st.sidebar.info("Support the Project.")
    st.sidebar.markdown("""
        <p>Donate for Knowledge, We will be doing this again ❤️</p>
        <a href="https://ibb.co/nBtGVnk"><img src="https://i.ibb.co/0Kv7WFJ/Google-Pay-QR.png" width="50"></a>
        <p>Thank you for your support 😍️</p>
    """, unsafe_allow_html=True)

    if page == "🏠 Home":
        st.title("Welcome to AutoBot 🤖")
        st.markdown("""
        **AutoBot AI**:
        **Functionalities:**
        1. AI Chatbot
        2. CODEX
        3. Web Scrapper
        4. GitHub Codespaces

        AutoBot, powered by the Gemini API, is a basic chatbot designed for automation. It excels in writing code and generating downloadable files with a .txt extension, offering the ability to handle up to 60 queries per minute.

        Developed by SKAV TECH, a company focused on creating practical AI projects, AutoBot is intended for educational purposes only. We do not endorse any illegal or unethical activities.
        """)
        st.video("https://youtu.be/i0Q-NBrYpPI", start_time=0)
        display_footer()

    elif page == "AutoBot 🤖":
        st.image("auto_bot_2.png")
        st.header("AutoBot 🤖")
        st.markdown(
            "AutoBot is effective for code generation. If your prompt contains code generation **-prompt-**, you can get downloadable files.")

        question = st.text_input("Ask the model a question:")
        if st.button("Ask AI"):
            with st.spinner("Generating response..."):
                try:
                    response = model.generate_content(question)
                    st.text("AutoBot Response:")
                    st.write(response.text)
                    st.markdown('---')
                    st.markdown(
                        "Security Note: We use **.txt** file format for code downloads, which is not easily susceptible to virus and malware attacks.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

                code_keywords = ["code", "write code", "develop code", "generate code", "generate", "build"]
                if any(keyword in question.lower() for keyword in code_keywords):
                    download_generated_code(response.text, "generated_code")

        display_footer()

    elif page == "GitHub Codespaces 🖥️":
        st.header("GitHub Codespaces 🖥️")
        st.markdown("Application will start in 10 sec. 😀")
        redirect_to_codespaces()
        display_footer()

    elif page == "Web Scrapper 🌐":
        st.header("Web Scrapper 🌐")
        st.markdown(
            "AutoBot powered **Web Scrapper**. This tool will get the code of any website. Simply enter the URL below. Download Extracted Code.")
        url = st.text_input("Enter URL:")
        if st.button("Extract HTML Code"):
            st.ballons()
            with st.spinner("Extracting HTML code..."):
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        extracted_html = response.text
                        download_html_code(extracted_html, url)
                    else:
                        st.error(f"Failed to retrieve HTML content 😕. Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

        display_footer()



    elif page == "CODEX ⚡":

        st.header("CODEX ⚡️")

        uploaded_files = st.file_uploader("Upload code files:", accept_multiple_files=True)

        st.markdown("""

            Welcome to **CODEX**

            Interactive CODING GUIDE, No one can explain Code like me trust me.

            CODEX is one way fun Feature, You can get Youtube Suggestion based on your Queries.

            **If you face ValueError or Type Error, Try changing the Prompt, This is may be because of Gemini API restrictions**

            1. You can ask specific code or content using the phrase @codex "prompt".


            2. You can upload your code here to ask the CODEX to generate an explanation (for example: @codex Can you explain me this code in the file "filename").


            3. I can generate 60 queries per minute. Pretty wild right? Haha, more to see and explore.

        """)

        st.info("""Example prompt: @codex explain me the code in the file "your_file_name"


        Some popular prompts:

        1. @codex explain me the code in the file app.py

        2. @codex how does this code work in the file app.py

        3. @codex can you explain me this code: "paste your code"

        """)

        st.warning("Use @codex phrase to start the prompt")

        prompt = st.text_area('Type your query here:', height=100)


        if st.button('Submit'):
            
            st.markdown('---')

            if prompt or uploaded_files:

                with st.spinner("Processing..."):

                    if prompt:

                        response = model.generate_content(prompt)

                        st.write("CODEX Response:")

                        st.write(response.text)

                        topic = extract_topic(prompt)

                        video_suggestions = fetch_youtube_videos(topic)

                        if video_suggestions:

                            st.markdown("### YouTube Video Suggestions:")

                            for video in video_suggestions:
                                st.write(f"[{video['title']}]({video['url']})")

                                st.video(video["url"])

                    if uploaded_files:

                        for file in uploaded_files:

                            st.write(f"Code for {file.name}:")

                            st.code(file.getvalue().decode("utf-8"))  # Display file content as code

                            response = model.generate_content(file.getvalue().decode("utf-8"))

                            st.write("CODEX Response:")

                            st.write(response.text)

                            video_suggestions = fetch_youtube_videos(file.getvalue().decode("utf-8"))

                            if video_suggestions:

                                st.markdown("### YouTube Video Suggestions:")

                                for video in video_suggestions:
                                    st.write(f"[{video['title']}]({video['url']})")

                                    st.video(video["url"])

            else:

                st.error("Please provide a query or upload a file.")

        display_footer()


if __name__ == "__main__":
    main()
