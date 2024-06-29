import requests

def fetch_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()  # Parse JSON response
        return data
    except requests.RequestException as e:
        return None

def get_token_details(query):
    api_url = f"https://api.dexscreener.com/latest/dex/search/?q={query}"
    data = fetch_data(api_url)
    
    if data and 'pairs' in data:
        top_token = data['pairs'][0]  # Get the top token pair
        return top_token
    else:
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
        
        return holders_sorted  # Return the sorted holders list
    else:
        return None

def get_holder_transactions(holder_address):
    api_url = f"https://api.solana.fm/v0/accounts/{holder_address}/transactions"
    data = fetch_data(api_url)
    
    if data and data['status'] == 'success' and 'result' in data and 'data' in data['result']:
        return data['result']['data']
    else:
        return None

# Example usage
query = "USDC/SOL"
token_details = get_token_details(query)

if token_details:
    mint_address = token_details['baseToken']['address']
    token_holders = get_token_holders(mint_address)

    if token_holders:
        # Simulate a user clicking on the first holder's address
        example_holder_address = token_holders[0]['address']
        
        transactions = get_holder_transactions(example_holder_address)
        if transactions:
            for transaction in transactions:
                print(f"Signature: {transaction['signature']}, Slot: {transaction['slot']}, Block Time: {transaction['blockTime']}, Status: {transaction['confirmationStatus']}, Error: {transaction['err']}")
        else:
            print("No transactions found for the selected holder.")
    else:
        print("No holders data found or failed to fetch token holders.")
else:
    print("No token details found for the given query.")
