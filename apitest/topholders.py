# import requests

# def get_top_holders(api_url, top_n=10):
#     try:
#         # Fetch the data from the API
#         response = requests.get(api_url)
#         response.raise_for_status()
#         holders_data = response.json()

#         # Ensure we have the expected structure
#         if isinstance(holders_data, list):
#             token_accounts = holders_data
#         elif isinstance(holders_data, dict) and 'tokenAccounts' in holders_data:
#             token_accounts = holders_data['tokenAccounts']
#         else:
#             raise ValueError("Unexpected API response format")

#         # Extract holders and details
#         holders = []
#         for account in token_accounts:
#             if 'info' in account and 'tokenAmount' in account['info'] and 'uiAmountString' in account['info']['tokenAmount']:
#                 holder = {
#                     'owner': account['info']['owner'],
#                     'uiAmountString': account['info']['tokenAmount']['uiAmountString'],
#                     'mint': account['info']['mint'],
#                     'state': account['info']['state'],
#                     '_id': account['_id'],
#                     'slot': account['slot']
#                 }
#                 holders.append(holder)

#         # Sort holders based on uiAmountString (convert to float for proper sorting)
#         sorted_holders = sorted(holders, key=lambda x: float(x['uiAmountString'].replace(',', '')), reverse=True)

#         # Get the top N holders
#         top_holders = sorted_holders[:top_n]

#         return top_holders
    
#     except requests.RequestException as e:
#         print(f"An error occurred while fetching data: {e}")
#         return []
#     except (ValueError, KeyError) as e:
#         print(f"Error: {e}")
#         return []

# # Example usage
# api_url = "https://api.solana.fm/v1/tokens/CoRkC3r6MqYuTeMRc7D8JJF7UiUyFWurXGpYy1xQATNq/holders"
# top_holders = get_top_holders(api_url)

# # Print the top holders with additional details
# print("Top token holders:")

# for holder in top_holders:
#     print(holder)




# import requests

# url = "https://api.dune.com/api/v1/farcaster/trends/users"

# headers = {"X-DUNE-API-KEY": "seq3K84oFzSbJ7cjBjooYFQI7rse5cfi"}

# response = requests.request("GET", url, headers=headers)

# print(response.text)
import requests

def fetch_data(api_url):
    try:
        # Fetch the data from the API
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()  # Parse JSON response
        return data
    except requests.RequestException as e:
        print(f"An error occurred while fetching data from {api_url}: {e}")
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

def get_token_holders(mint_address):
    api_url = f"https://api.solana.fm/v1/tokens/{mint_address}/holders"
    data = fetch_data(api_url)
    
    if data and 'tokenAccounts' in data:
        holders = []
        for account in data['tokenAccounts']:
            holder_info = {
                "address": account['info']['owner'],
                "balance": float(account['info']['tokenAmount']['uiAmount'])  # Convert balance to float for sorting
            }
            holders.append(holder_info)
        
        # Sort holders based on balance (highest to lowest)
        holders_sorted = sorted(holders, key=lambda x: x['balance'], reverse=True)
        
        return holders_sorted[:10]  # Return only the top 10 holders
    else:
        print(f"No holders data found for mint address '{mint_address}' or failed to fetch token holders.")
        return None

# Example usage
query = "USDC/SOL"
token_details = get_token_details(query)

# Print the token details
if token_details:
    print("Top token details:")
    for key, value in token_details.items():
        print(f"{key}: {value}")

    # Fetch and print the top 10 holders if available
    mint_address = token_details['baseToken']['address']
    token_holders = get_token_holders(mint_address)

    if token_holders:
        print("\nTop 10 Token holders (sorted by balance):")
        for index, holder in enumerate(token_holders, start=1):
            print(f"Rank {index}:")
            print(f"Address: {holder['address']}, Balance: {holder['balance']}")
    else:
        # If token_holders is None, it means no holders data was found
        print("No holders data found or failed to fetch token holders.")
