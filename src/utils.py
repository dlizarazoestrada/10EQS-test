import csv
import requests
import os

def read_csv(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

def fetch_external_data(api_url):
    api_key = os.getenv("API_KEY", "DPSKDRJGLXGSFOMBLKFMOFXWAODQLAFSISJJTQLSTNJXLJEGRZXKQRMIAEXRVEJD")
    if not api_key:
        print("Error: API_KEY is not set in the environment variables.")
        return []
    else:
        print(f"API_KEY loaded successfully")
    
    try:
        response = requests.get(f"{api_url}?token={api_key}&page=1&per_page=10")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            return data['results']
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return []
