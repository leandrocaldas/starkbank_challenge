import argparse
import os
from pix import create_pix
from log import get_pix_data_log, get_pix_data_log_all_day
from report import generate_pix_report

def generate_pix(pix_qtd, pix_amount):
    # Create PIX transfers
    created_transfers = create_pix(pix_qtd, pix_amount)

    # Get PIX data logs
    data_log = get_pix_data_log(created_transfers, pix_qtd)

    # Generate a PIX report
    report = generate_pix_report(data_log)
    print(report)

def generate_all_day_report(after, before):
    # Get PIX data logs during all day
    data_log = get_pix_data_log_all_day(after, before)
    
    # Generate a PIX report
    report = generate_pix_report(data_log)
    print(report)

def main():
    parser = argparse.ArgumentParser(description='Run a specific function')
    parser.add_argument(
        '--function', type=str, 
        choices=['generate_pix', 'generate_all_day_report'],
        default='generate_pix',
        help='Select the function to run (default: generate_pix)')

    args = parser.parse_args()

    if args.function == 'generate_pix':
        pix_qtd = int(os.getenv("PIX_QTD", 10))
        pix_amount = int(os.getenv("PIX_AMOUNT", 10000))
        generate_pix(pix_qtd, pix_amount)
    elif args.function == 'generate_all_day_report':
        generate_all_day_report()

if __name__ == "__main__":
    main()
