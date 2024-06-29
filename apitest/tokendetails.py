import requests

def fetch_data(api_url):
    try:
        # Fetch the data from the API
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()  # Parse JSON response
        return data
    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return None

def get_token_details(query):
    api_url = f"https://api.dexscreener.com/latest/dex/search/?q={query}"
    data = fetch_data(api_url)
    
    if data and 'pairs' in data:
        top_token = data['pairs'][0]  # Get the top token pair
        return top_token
    else:
        print("No data found for the given query.")
        return None

# Example usage
query = "USDC/SOL"
token_details = get_token_details(query)

# Print the token details
if token_details:
    print("Top token details:")
    for key, value in token_details.items():
        print(f"{key}: {value}")