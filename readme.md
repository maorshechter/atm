# ATM Project

This project simulates an ATM system where users can perform various banking operations such as checking balances, withdrawing money, and depositing funds.

# how to start
src/main.py

file mode - load and persist from file
ephemeral mode - load and dummy persist static data (for dev purposes)

# tests
python -m pytest

## `data.json` Structure

The `data.json` file stores user account information in the following format:

```json
{
  "users": {
    "1": {
      "name": "John Doe",
      "email": ""
    },
    "2": {
      "name": "Jane Smith",
      "email": ""
    }
  },
  "passwords": {
    "1": {
      "password": "111"
    },
    "2": {
      "password": "qwerty"
    }
  },
  "accounts": {
    "1": {
      "owner_id": "1",
      "balance": 901.5,
      "account_id": "1"
    },
    "2": {
      "owner_id": "1",
      "balance": 2100.0,
      "account_id": "2"
    },
    "3": {
      "owner_id": "2",
      "balance": 1500,
      "account_id": "3"
    },
    "4": {
      "owner_id": "2",
      "balance": 2500,
      "account_id": "4"
    }
  }
}

considerations:
i didnt want to make one big flat table because it is kind of unefficient and when a change happens it requires
too much updates, so i normalized the data:
**users dataset
**passwords dataset
**accounts datasets
to support multiple data types i chose json as file format, i didnt want to use csv and build costum reader
and didnt want to create multiple files (file per table)

load and save:
when i started building my code i thought i can read only the logged in user data but because i want to support money transfer
to all account, all data (accounts) is neeeded, current solution will not scale for tons of users (OOM).
about the save - i could do it more efficient, right now i overwrite the file, i could save the delta and make a partial update - because it is file based and not a real data bases i dont think there is a benfit to do it.

when i read the data in atm class i build (preprocess) user to accounts dictionary (index) - this way i can answer the get balance in O(1), the dict point on the accoutnt obj so when i deposit/withdraw money the data is updationg in index as well.


