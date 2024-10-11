import gzip
import requests
import base64
import os
import uuid
import bcrypt
from pathlib import Path
from datetime import datetime


def Aropha(email, password, engine = None, address_to_spreadsheet = None, timeout = 3600):
    """
    A function that processes a spreadsheet, compresses it, sends it to Aropha's processing server and returns the response.

    Parameters:
    - email (str): The email for the Aropha account.
    - password (str): The password for the Aropha account.
    - engine (str): The engine or model to use for processing.
    - address_to_spreadsheet (str): The path to the spreadsheet file.
    - timeout (int): The time in seconds after which the request will time out.

    Returns:
    None
    """

    if (address_to_spreadsheet is not None) & (isinstance(address_to_spreadsheet, str)):
        address_to_spreadsheet = Path(address_to_spreadsheet).resolve(strict = True)

        if not address_to_spreadsheet.exists():
            raise FileNotFoundError(f"File not found at {address_to_spreadsheet}. Please check the file path and try again.")

        if not (address_to_spreadsheet.suffix.lower().__eq__('.xlsm') or address_to_spreadsheet.suffix.lower().__eq__('.xlsx')):
            print(f"Invalid file format.\n")
            return None
        
        try:
            with open(address_to_spreadsheet, 'rb') as f:
                raw_data = base64.b64encode(gzip.compress(f.read(), compresslevel = 9)).decode('utf-8')
                f.close()

            try:
                random_file = f"{uuid.uuid4()}.txt"
                with open(f"{address_to_spreadsheet.parent}/{random_file}", "w") as f:
                    f.write('Test file by Aropha to check if the file can be created in this folder.')
                    f.close()
                
                os.remove(f"{address_to_spreadsheet.parent}/{random_file}")

            except Exception as e:
                print(f"Can not create files at `{address_to_spreadsheet.parent}`. Please try again later.\n")
                return None
        
        except Exception as e:
            print(f"An error occurred while reading the file: {str(e)}. Please try again later.\n")
            return None
        
        if raw_data.__sizeof__() > 10*1024*1024:
            print(f"Even after zip compression, your file size exceeds the 10MB limit. Please upload a smaller file./nn")
            return None
    else:
        print(f"Spreadsheet file not provided.\n")
        raw_data = 'blank'

    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        json_data = {'email': email, 'hashed_password': hashed_password, 'engine': engine, 'raw_data': raw_data}

        response_content = requests.post(
            url = 'https://test.aropha.com',
            headers = {'Content-Type': 'application/json'},
            json = json_data,
            timeout = timeout,
            verify = True,
            allow_redirects = False
        )

        status_code = response_content.status_code
        print(status_code)

    except Exception as e:
        print(f"An error occurred during data processing: {str(e)}. Please try again later.\n")
        return None

    if status_code == 200:

        biodeg_data = f"{address_to_spreadsheet.parent}/{address_to_spreadsheet.stem}_biodeg_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.gz"
        with open(biodeg_data, 'wb') as f:
            f.write(base64.b64decode(response_content.json()['data']))
            f.close()

        print(f"Data processing completed successfully. You can access the processed data at: `{biodeg_data}`\n")
        print(f"Number of remaining polymer experiment credits: {response_content.json()['polymer_credits']}\n")
        print(f"Number of remaining SMILES string experiment credits: {response_content.json()['smiles_string_credits']}\n")

    elif status_code == 422:

        flag_address = f"{address_to_spreadsheet.parent}/{address_to_spreadsheet.stem}_flag_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.gz"
        with open(flag_address, 'wb') as f:
            f.write(base64.b64decode(response_content.json()['data']))
            f.close()

        print(f"Data processing flagged for inconsistencies in row entries. Please review the flagged rows and correct them. The flagged notes can be found at: `{flag_address}`\n")
        print(f"Number of remaining polymer experiment credits: {response_content.json()['polymer_credits']}\n")
        print(f"Number of remaining SMILES string experiment credits: {response_content.json()['smiles_string_credits']}\n")

    elif status_code == 403:
        print(f"{response_content.json()['detail']}\n")

    else:
        try:
            print(f"An error occurred during data processing: {response_content.json()['detail']}. Please try again later.\n")
        except:
            print(f"Internal error problem.\n")

    return None