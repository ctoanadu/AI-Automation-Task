import streamlit as st
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


import chromedriver_autoinstaller
from openai import OpenAI

# Scraper class to get HTML content
class Scraper:
    def __init__(self, url):
        self.url = url

    def get_html_content(self):
        #chromedriver_autoinstaller.install()
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-data-dir=/tmp/chrome-profile")

        # Configure and pass both service and options
        #driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        # Set path to ChromeDriver executable (replace 'path/to/chromedriver' with the actual path)
        #driver_path = "/path/to/chromedriver"  # Replace with your ChromeDriver path
        #driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

        driver = webdriver.Chrome(options=chrome_options)




        # Navigate to the URL and scrape HTML content
        driver.get(self.url)
        time.sleep(6)  # Allow the page to load completely
        html_content = driver.page_source
        driver.quit()  # Always close the driver after use
        return html_content

# LLM class to interact with OpenAI API
class LLM:
    def __init__(self, api_key, model="gpt-4o-mini"):
        self.model = model
        self.api_key = api_key  # Store the API key

    def make_api(self, user_inst, system_inst):
        client = OpenAI(api_key=self.api_key)  # Use the provided API key

        # Request to OpenAI's API
        completion = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_inst},
                {"role": "user", "content": user_inst}
            ]
        )

        response = completion.choices[0].message.content
        return response

# Streamlit app setup
st.title('Company Insights from URL: Growth X')

# Input field for OpenAI API key (manual input)
api_key_input = st.text_input('Enter your OpenAI API Key:', '')

# Check if API key is provided
if api_key_input:
    # Input field to take URL from the user
    url_input = st.text_input('Enter the URL of the company website:', '')

    # Show a loading spinner while processing
    if url_input:
        st.write("Processing the website... Please wait.")
        scraper = Scraper(url_input)
        html_content = scraper.get_html_content()

        # Define the system instruction
        system_inst = """You are an AI designed to produce research reports for sales teams. Given the HTML content obtained from the website, your task is to extract key information from the site to create a concise, informative article. Focus on providing insights that will help the sales team engage effectively with the prospect. For each summary:

                Identify the company's industry and core mission or goals.
                Summarize the main products or services offered.
                Describe the primary target audience or customer segment.
                Provide details on the company’s size, locations, or key executives, if available.
                Note any recent news, achievements, or partnerships to help the sales team understand potential discussion points.
                Present the information in a clear and structured format, similar to a brief research article, making it easy for the sales team to access insights at a glance."""

        # User instruction with HTML content
        user_inst = f"Given the HTML content of {url_input}, provide a concise brief research summary about the company, including its industry, main products or services, target customers, company size, and any recent news or achievements that would be valuable for the sales team."

        # Initialize LLM with the API key and get response
        llm = LLM(api_key_input)
        result = llm.make_api(user_inst, system_inst)

        # Display the result in the app
        st.write("### Company Summary:")
        st.write(result)
else:
    st.warning("Please enter your OpenAI API key.")
