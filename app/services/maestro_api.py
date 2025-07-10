import os
import requests

class MaestroAPIError(Exception):
    """Custom exception for Maestro API errors."""
    pass

def get_maestro_data():
    """
    Fetches data from the Maestro API.

    Reads the API endpoint and key from environment variables MAESTRO_ENDPOINT
    and MAESTRO_API_KEY.

    Returns:
        dict: The JSON response from the API.

    Raises:
        MaestroAPIError: If environment variables are not set or if the API request fails.
    """
    endpoint = os.getenv("MAESTRO_ENDPOINT")
    api_key = os.getenv("MAESTRO_API_KEY")

    if not endpoint:
        raise MaestroAPIError("MAESTRO_ENDPOINT environment variable not set.")
    if not api_key:
        raise MaestroAPIError("MAESTRO_API_KEY environment variable not set.")

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "SOME_KEY": "SOME_VALUE"
    }

    try:
        response = requests.post(endpoint, headers=headers, timeout=60) # 10 second timeout
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        return response.json()
    except requests.exceptions.MissingSchema:
        raise MaestroAPIError(f"Invalid URL: '{endpoint}'. Make sure it includes the schema (e.g., http:// or https://).")
    except requests.exceptions.ConnectionError as e:
        raise MaestroAPIError(f"Connection error to Maestro API at {endpoint}: {e}")
    except requests.exceptions.Timeout as e:
        raise MaestroAPIError(f"Request to Maestro API timed out: {e}")
    except requests.exceptions.HTTPError as e:
        raise MaestroAPIError(f"Maestro API request failed with status {e.response.status_code}: {e.response.text}")
    except requests.exceptions.RequestException as e:
        raise MaestroAPIError(f"An unexpected error occurred while calling Maestro API: {e}")
    except ValueError as e: # Handle cases where response.json() fails
        raise MaestroAPIError(f"Failed to decode JSON response from Maestro API: {e}")
