import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from win10toast import ToastNotifier

def fetch_weather_data(url):
    session = requests.Session()
    retry = Retry(
        total=5,  # Total number of retries
        backoff_factor=1,  
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these HTTP status codes
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        # Send GET request with a 60-second timeout
        response = session.get(url, headers=headers, timeout=60)
        response.raise_for_status() 

        # Print the raw HTML
        print(response.text)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the temperature and chances of rain
        current_temp = soup.find("span", class_="CurrentConditions--tempValue--MHmYY")
        chances_rain = soup.find("div", class_="CurrentConditions--precipValue--2aJSf")

        # Extract the text from the parsed elements
        temp_text = current_temp.text if current_temp else "N/A"
        rain_text = chances_rain.text if chances_rain else "N/A"

        result = f"Current temperature: {temp_text} in Kathmandu\nChance of rain: {rain_text}"

        # Display a toast notification with the result
        n = ToastNotifier()
        n.show_toast("Weather Update", result, duration=10)

        print(result)  # Also print the result to the console

    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error occurred: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")

# URL for the weather data
weather_url = 'https://www.accuweather.com/en/np/national/satellite'

# Fetch the weather data
fetch_weather_data(weather_url)
