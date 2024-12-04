import gzip
import requests
import base64
import os
import uuid
from pathlib import Path
from datetime import datetime


def Aropha(email, password, address_to_spreadsheet = None, timeout = 3600):
    """
    A function for Aropha's inference pipeline that forwards a data entry spreadsheet to Aropha's processing servers and returns the results in the `gzip` format.

    Parameters:
    - email (str): The email for the Aropha account.
    - password (str): The password for the Aropha account.
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
            raise TypeError(f"Invalid file format.\n")
        
        try:
            with open(address_to_spreadsheet, 'rb') as f:
                raw_data = base64.b64encode(gzip.compress(f.read(), compresslevel = 9)).decode('utf-8')
                f.close()

        except Exception as e:
            raise Exception(f"An error occurred while reading the file: {str(e)}. Please try again later.\n")
        
        if raw_data.__sizeof__() > 10*1024*1024:
            raise BufferError(f"Even after zip compression, your file size exceeds the 10MB limit. Please upload a smaller file.\n")      

        try:

            counter = 0
            random_file = Path(f"{address_to_spreadsheet.parent}/{uuid.uuid4()}.txt")
            while random_file.exists():
                random_file = Path(f"{address_to_spreadsheet.parent}/{uuid.uuid4()}.txt")
                counter += 1
                if counter > 5:
                    raise PermissionError(f"Can not create files at `{address_to_spreadsheet.parent}`. Please try again later.\n")
            
            with open(random_file, "w") as f:
                f.write('Test file by Aropha to check if the file can be created in this folder.')
                f.close()
        
        except Exception as e:
            raise PermissionError(f"Can not create files at `{address_to_spreadsheet.parent}`. Please try again later.\n")

        try:
            os.remove(random_file)
        except:
            Warning(f"Could not delete the test file `{random_file}` created by Aropha. Please delete the file manually.\n")

    else:
        print(f"Spreadsheet file not provided.\n")
        raw_data = 'blank'

    try:
        json_data = {'email': email, 'password': password, 'raw_data': raw_data}

        response_content = requests.post(
            url = 'https://modelserver.aropha.com',
            headers = {'Content-Type': 'application/json'},
            json = json_data,
            timeout = timeout,
            verify = True,
            allow_redirects = False
        )

        status_code = response_content.status_code
        print(status_code)

    except Exception as e:
        raise Exception(f"An error occurred during data processing: {str(e)}. Please try again later.\n")

    if status_code == 200:

        biodeg_data = f"{address_to_spreadsheet.parent}/{address_to_spreadsheet.stem}_biodeg_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.gz"
        with open(biodeg_data, 'wb') as f:
            f.write(base64.b64decode(response_content.json()['data']))
            f.close()

        print(f"Data processing completed successfully. You can access the processed data at: `{biodeg_data}`\n")
        print(f"Number of remaining ArophaFormer simulation credits: {response_content.json()['ArophaFormer_credits']}\n")
        print(f"Number of remaining ArophaGrapher simulation credits: {response_content.json()['ArophaGrapher_credits']}\n")
        print(f"Number of remaining ArophaPolyFormer simulation credits: {response_content.json()['ArophaPolyFormer_credits']}\n")

    elif status_code == 422:

        flag_address = f"{address_to_spreadsheet.parent}/{address_to_spreadsheet.stem}_flag_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.gz"
        with open(flag_address, 'wb') as f:
            f.write(base64.b64decode(response_content.json()['data']))
            f.close()

        print(f"{response_content.json()['detail']}. The flagged notes can be found at: `{flag_address}`\n")

    elif status_code == 403:
        print(f"{response_content.json()['detail']}\n")

    else:
        try:
            print(f"An error occurred during data processing: {response_content.json()['detail']} Please try again later.\n")
        except:
            print(f"Internal error problem.\n")

    return None