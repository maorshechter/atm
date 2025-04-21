from atm_cli import ATMCLI
from atm_handler.atm_file_handler import AtmFileHandler
import argparse
from atm_handler.atm_ephemeral_handler import AtmEphemeralHandler

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ATM CLI Application")
    parser.add_argument('--mode', choices=['ephemeral', 'file'], required=True, help="Mode of operation: 'ephemeral' or 'file'")
    args = parser.parse_args()

    if args.mode == 'ephemeral':
        atm_handler = AtmEphemeralHandler()

    elif args.mode == 'file':
        atm_handler = AtmFileHandler(data_file='./data/data.json')

    cli = ATMCLI(atm_handler=atm_handler)
    cli.run()
