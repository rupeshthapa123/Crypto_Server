from flask import jsonify
import requests
import time

def fetch_data_from_api(api_url, max_retries=3, timeout=5):
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(api_url, timeout=timeout)
            data = response.json()
            return jsonify({"payload":data})
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries >= max_retries:
                return jsonify({'error': f"Max retries exceeded: {str(e)}"})
            print(f"Request failed. Retrying... (Attempt {retries}/{max_retries})")
            time.sleep(1)

    return jsonify({'error': 'Unexpected error occurred.'})


