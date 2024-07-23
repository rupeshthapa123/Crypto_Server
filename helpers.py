from flask import jsonify
import requests
import time

def fetch_data_from_api(api_url, max_retries=3, timeout=5):
    retries = 0

    try:
        while retries < max_retries:
            try:
                response = requests.get(api_url, timeout=timeout)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
                data = response.json()
                return jsonify({"payload": data})
            except requests.exceptions.RequestException as e:
                retries += 1
                if retries >= max_retries:
                    return jsonify({'error': f"Max retries exceeded: {str(e)}"})
                print(f"Request failed. Retrying... (Attempt {retries}/{max_retries})")
                time.sleep(1)
    except Exception as e:
        return jsonify({'error': f'Unknown error occurred. Error: {e}'})

# from flask import jsonify
# import requests
# import time

# def fetch_data_from_api(api_url, max_retries=3, timeout=5):
#     retries = 0

#     while retries < max_retries:
#         try:
#             response = requests.get(api_url, timeout=timeout)
#             data = response.json()
#             return jsonify({"payload":data})
#         except requests.exceptions.RequestException as e:
#             retries += 1
#             if retries >= max_retries:
#                 return jsonify({'error': f"Max retries exceeded: {str(e)}"})
#             print(f"Request failed. Retrying... (Attempt {retries}/{max_retries})")
#             time.sleep(1)

#     return jsonify({'error': 'Unexpected error occurred.'})
