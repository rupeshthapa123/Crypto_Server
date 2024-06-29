# import requests

# def get_top_tokens(api_url, tags, top_n=10):
#     try:
#         # Fetch the data from the API
#         response = requests.get(api_url)
#         response.raise_for_status()
#         tokens = response.json()

#         # Print the number of tokens fetched
#         print(f"Fetched {len(tokens)} tokens from the API.")

#         # Filter tokens based on the specified tags (any of the tags)
#         filtered_tokens = [token for token in tokens if any(tag in token['tags'] for tag in tags)]

#         # Print the number of tokens after filtering
#         print(f"Filtered down to {len(filtered_tokens)} tokens with tags {tags}.")

#         # Sort the tokens based on their name or symbol
#         sorted_tokens = sorted(filtered_tokens, key=lambda x: x.get('name', ''))

#         # Get the top N tokens
#         top_tokens = sorted_tokens[:top_n]

#         return top_tokens
    
#     except requests.RequestException as e:
#         print(f"An error occurred while fetching data: {e}")
#         return []

# # Example usage
# api_url = "https://token.jup.ag/strict"
# tags = ['old-registry', 'community']
# top_tokens = get_top_tokens(api_url, tags)

# #  Print the top tokens
# print("Top tokens:")
# for token in top_tokens:
#     print(token)



# https://api.coingecko.com/api/v3/


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

# Example usage
api_url = "https://stats.jup.ag/coingecko/tickers"
data = fetch_data(api_url)

# Print the top 10 fetched data
if data:
    print("Top 10 items from the fetched data:")
    for index, item in enumerate(data[:10], start=1):
        print(f"\nItem {index}:")
        for key, value in item.items():
            print(f"{key}: {value}")
