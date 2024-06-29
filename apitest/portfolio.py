import requests

API_KEY = "YE7o5Z5gC7ucUbZQ"

def fetch_data(api_url):
    try:
        headers = {
            "x-api-key": API_KEY
        }
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()  # Parse JSON response
        return data
    except requests.RequestException as e:
        print(f"Error fetching data from {api_url}: {str(e)}")
        return None

def get_wallet_information(holder_address):
    api_url = f"https://api.shyft.to/sol/v1/wallet/get_portfolio?network=mainnet-beta&wallet={holder_address}"
    print(f"Fetching data from: {api_url}")
    data = fetch_data(api_url)
    
    if data and data.get('success', False) and 'result' in data:
        return data['result']
    else:
        print(f"Failed to fetch wallet information. API response: {data}")
        return None

# Example usage
holder_address = "9DrvZvyWh1HuAoZxvYWMvkf2XCzryCpGgHqrMjyDWpmo"  # Replace with actual holder address
wallet_info = get_wallet_information(holder_address)

if wallet_info:
    print(f"SOL Balance: {wallet_info['sol_balance']}")
    print("Top 10 Tokens:")
    tokens_to_display = min(10, len(wallet_info['tokens']))
    for i in range(tokens_to_display):
        token = wallet_info['tokens'][i]
        print(f"Token Address: {token['address']}, Balance: {token['balance']}, Associated Account: {token['associated_account']}, Decimals: {token['info']['decimals']}")
else:
    print("Failed to fetch wallet information.")
