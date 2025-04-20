from atm import ATM
from atm_cli import ATMCLI
from atm_handler.atm_file_handler import AtmFileHandler
import argparse
from atm_handler.atm_ephemeral_handler import AtmEphemeralHandler
from config import DATA_FILE_PATH

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ATM CLI Application")
    parser.add_argument('--mode',
                         default='file',
                         choices=['ephemeral', 'file'],
                         required=False,
                         help="Mode of operation: 'ephemeral' or 'file'")
    
    args = parser.parse_args()

    if args.mode == 'ephemeral':
        atm_handler = AtmEphemeralHandler()
        
    elif args.mode == 'file':
        atm_handler = AtmFileHandler(data_file=DATA_FILE_PATH)

    cli = ATMCLI(atm_handler=atm_handler)
    cli.run()
