import streamlit as st
import requests
import webbrowser
import os
import time
import base64
from google.generativeai import configure, GenerativeModel
from urllib.parse import urlparse
import json
from streamlit_lottie import st_lottie


# Set up the Generative AI configuration with a placeholder API key
configure(api_key=st.secrets["api_key"])

# Create a Generative Model instance (assuming 'gemini-pro' is a valid model)
model = GenerativeModel('gemini-pro')

# Lottie animation
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

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
        background-color: #f8f9fa;
        text-align: center;
        border-top: 1px solid #e1e1e1;
        font-family: 'Arial', sans-serif;
        color: #6c757d;
    }
    </style>
    <div class="footer">
        <p><b>&copy; 2024 SKAV TECH. All rights reserved. | Follow us on <a href="https://bit.ly/socialinstag">Instagram</a></b></p>
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
        st.error(f"Failed to fetch YouTube videos. Status code: {response.status_code}")
    return video_details

# Function to extract the main topic from the prompt
def extract_topic(prompt):
    start_phrases = ["@codex", "codex", "@autobot"]
    for phrase in start_phrases:
        if prompt.lower().startswith(phrase):
            return prompt[len(phrase):].strip()
    return prompt.strip()

# Main Streamlit application
def main():
    st.set_page_config(page_title="AutoBot AI", page_icon="💀", layout="wide", initial_sidebar_state="expanded")

    st.sidebar.image("auto_bot_2.png", use_column_width=True)
    page = st.sidebar.selectbox("**MENU**", ["🏠 Home", "AutoBot 💀", "CODEX ⚡", "Web Scrapper 🌐", "GitHub Codespaces 🖥️", "Refund & Privacy Policy 💸"])

    st.sidebar.title("Support Us")
    st.sidebar.info("Your support helps us improve AutoBot AI.")
    st.sidebar.markdown("""
        <p>Donate for Knowledge, We will be doing this again ❤️</p>
        <a href="https://ibb.co/nBtGVnk"><img src="https://i.ibb.co/0Kv7WFJ/Google-Pay-QR.png" width="50"></a>
    """, unsafe_allow_html=True)

    if page == "🏠 Home":
        st.title("Welcome to AutoBot AI 💀")
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

        # Embedding Lottie animation
        st.markdown("""
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://lottie.host/ee1e5978-9014-47cb-8031-45874d2dc909/tXASIvRMrN.json" background="#FFFFFF" speed="1" style="width: 300px; height: 300px" loop controls autoplay direction="1" mode="normal"></lottie-player>
        """, unsafe_allow_html=True)

        st.video("https://youtu.be/i0Q-NBrYpPI", start_time=0)
        display_footer()

    elif page == "AutoBot 💀":
        st.image("auto_bot_2.png")
        st.header("AutoBot 💀")
        st.markdown("AutoBot is effective for code generation. If your prompt contains code generation **-prompt-**, you can get downloadable files.")

        question = st.text_input("Ask the model a question:")

        if st.button("Ask AI"):

            lottie_url = "https://lottie.host/fb24aa71-e6dd-497e-8a6c-3098cb64b1ed/V9N1Sd3klS.json"

            # Load and display Lottie animation
            lottie_animation = load_lottie_url(lottie_url)
            if lottie_animation:
                st_lottie(lottie_animation, speed=27, width=150, height=100, key="lottie_animation")
            else:
                st.error("Failed to load Lottie animation.")
            with st.spinner("Generating response 💀..."):
                try:
                    response = model.generate_content(question)
                    if response.text:
                        st.text("AutoBot Response:")
                        st.write(response.text)
                        st.markdown('---')
                        st.markdown("Security Note: We use **.txt** file format for code downloads, which is not easily susceptible to virus and malware attacks.")
                    else:
                        st.error("No valid response received from the AI model.")
                        st.write(f"Safety ratings: {response.safety_ratings}")
                except ValueError as e:
                    st.info(f"Unable to assist with that prompt due to: {e}")
                except IndexError as e:
                    st.info(f"Unable to assist with that prompt due to: {e}")
                except Exception as e:
                    st.info(f"An unexpected error occurred: {e}")

                code_keywords = ["code", "write code", "develop code", "generate code", "generate", "build"]
                if any(keyword in question.lower() for keyword in code_keywords):
                    if response.text:
                        download_generated_code(response.text, "generated_code")
        st.markdown('---')
        display_footer()

    elif page == "GitHub Codespaces 🖥️":
        st.header("GitHub Codespaces 🖥️")
        st.markdown("Application will start in 10 seconds...")
        lottie_url = "https://lottie.host/1b47b231-3f17-4e3c-920f-25d73c2570d5/YFkJCSv0nf.json"

        # Load and display Lottie animation
        lottie_animation = load_lottie_url(lottie_url)
        if lottie_animation:
            st_lottie(lottie_animation, speed=1, width=300, height=300, key="lottie_animation")
        else:
            st.error("Failed to load Lottie animation.")

        redirect_to_codespaces()
        display_footer()

    elif  page == "Web Scrapper 🌐":
        st.header("Web Scrapper 🌐")
        st.markdown("AutoBot powered **Web Scrapper**. This tool will get the code of any website. Simply enter the URL below. Download Extracted Code.")
        url = st.text_input("Enter URL:")
        if st.button("Extract HTML Code"):

            with st.spinner("Extracting HTML code 🫨..."):

                lottie_url = "https://lottie.host/ee1e5978-9014-47cb-8031-45874d2dc909/tXASIvRMrN.json"

                # Load and display Lottie animation
                lottie_animation = load_lottie_url(lottie_url)
                if lottie_animation:
                    st_lottie(lottie_animation, speed=1, width=300, height=300, key="lottie_animation")
                else:
                    st.error("Failed to load Lottie animation.")

                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        extracted_html = response.text
                        download_html_code(extracted_html, url)
                        st.balloons()
                    else:
                        st.info(f"Failed to retrieve HTML content. Status code: {response.status_code}")
                except Exception as e:
                    st.info(f"An error occurred: {e}")
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

        st.info("""
            Example prompt: @codex explain me the code in the file "your_file_name"

            Some popular prompts:
            1. @codex explain me the code in the file app.py
            2. @codex how does this code work in the file app.py
            3. @codex can you explain me this code: "paste your code"
        """)

        st.warning("Use @codex phrase to start the prompt")

        prompt = st.text_area('Type your query here:', height=100)
        st.markdown('If you face Problem in Generating your Query, Try changing the Prompt, This is may be because of Gemini API restrictions')
        if st.button('Submit'):
            st.markdown('---')

            if prompt or uploaded_files:
                with st.spinner("Processing..."):

                    if prompt:
                        try:
                            response = model.generate_content(prompt)
                            if response.text:
                                st.write("CODEX Response:")
                                st.write(response.text)

                                topic = extract_topic(prompt)
                                video_suggestions = fetch_youtube_videos(topic)

                                if video_suggestions:
                                    st.markdown("### YouTube Video Suggestions:")
                                    for video in video_suggestions:
                                        st.write(f"[{video['title']}]({video['url']})")
                                        st.video(video["url"])
                            else:
                                st.error("No valid response received from the AI model.")
                                st.write(f"Safety ratings: {response.safety_ratings}")
                        except ValueError as e:
                            st.info(f"Unable to assist with that prompt due to: {e}")
                        except IndexError as e:
                            st.info(f"Unable to assist with that prompt due to: {e}")
                        except Exception as e:
                            st.info(f"An unexpected error occurred: {e}")

                    if uploaded_files:
                        for file in uploaded_files:
                            st.write(f"Code for {file.name}:")
                            file_content = file.getvalue().decode("utf-8")
                            st.code(file_content)

                            try:
                                response = model.generate_content(file_content)
                                if response.text:
                                    st.write("CODEX Response:")
                                    st.write(response.text)

                                    video_suggestions = fetch_youtube_videos(file_content)
                                    if video_suggestions:
                                        st.markdown("### YouTube Video Suggestions:")
                                        for video in video_suggestions:
                                            st.write(f"[{video['title']}]({video['url']})")
                                            st.video(video["url"])
                                else:
                                    st.error("No valid response received from the AI model.")
                                    st.write(f"Safety ratings: {response.safety_ratings}")
                            except ValueError as e:
                                st.info(f"Unable to assist with that prompt due to: {e}")
                            except IndexError as e:
                                st.info(f"Unable to assist with that prompt due to: {e}")
                            except Exception as e:
                                st.info(f"An unexpected error occurred: {e}")

            else:
                st.error("Please provide a query or upload a file.")
                st.markdown('---')

        display_footer()
    
    elif page == "Refund & Privacy Policy 💸":
        st.markdown("""

### Privacy Policy:

**1. Collection of Information:**
We may collect personal information such as name, email address, and other contact details when you interact with our services. We may also collect non-personal information such as device information, browser type, and IP address for analytics purposes.

**2. Use of Information:**
We use the information collected to provide and improve our services, communicate with you, and personalize your experience. We do not sell or share your personal information with third parties without your consent, except as required by law.

**3. Security:**
We take reasonable measures to protect your personal information from unauthorized access, use, or disclosure. However, no method of transmission over the internet or electronic storage is 100% secure, and we cannot guarantee absolute security.

**4. Cookies:**
We may use cookies and similar technologies to collect information and improve our services. You can choose to disable cookies in your browser settings, but this may affect the functionality of our services.

**5. Third-Party Links:**
Our services may contain links to third-party websites or services. We are not responsible for the privacy practices or content of these third parties. We encourage you to review the privacy policies of these third parties.

**6. Changes to Privacy Policy:**
We reserve the right to update or change our privacy policy at any time. Any changes will be effective immediately upon posting on this page.

**Refund Policy:**

**1. Refund Eligibility:**
Refunds may be requested within [X days/weeks/months] of purchase for any reason. To be eligible for a refund, you must provide proof of purchase and meet any additional requirements specified in our refund policy.

**2. Refund Process:**
To request a refund, please contact us at [contact email/phone number]. We will review your request and respond as soon as possible. If your refund is approved, it will be processed using the original payment method.

**3. Non-Refundable Items:**
Certain items may not be eligible for a refund, such as digital products that have been downloaded or used, or services that have been completed.

**4. Refund Exceptions:**
We reserve the right to refuse refunds in cases of suspected abuse or fraud, or if the refund request does not meet our refund policy criteria.

**5. Contact Us:**
If you have any questions or concerns about our privacy policy or refund policy, please contact us at [contact skavtech.in@gmail.com].

This is a basic template and should be customized to fit the specific details and requirements of your project. It's also important to consult with legal professionals to ensure compliance with relevant laws and regulations.""")
        display_footer()

if __name__ == "__main__":
    main()
