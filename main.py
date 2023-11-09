import argparse
import os
from app.pix_generate import create_pix
from app.report.get_log import get_pix_data_log, get_pix_data_log_all_day
from app.report.generate_report import generate_reports
from app.report.report_dataframe import generate_pix_report_data
from datetime import datetime

def generate_pix(pix_qtd, pix_amount):
    # Create PIX transfers
    created_transfers = create_pix(pix_qtd, pix_amount)

    # Get PIX data logs
    data_log = get_pix_data_log(created_transfers)

    # Generate a PIX report
    df_success, df_failed, df_log_failed = generate_pix_report_data(data_log)
    generate_reports(df_success, df_failed, df_log_failed)

def generate_all_day_report(after, before):
    # Get PIX data logs during all day
    data_log = get_pix_data_log_all_day(after, before)
    
    # Generate a PIX report
    df_success, df_failed, df_log_failed = generate_pix_report_data(data_log)
    generate_reports(df_success, df_failed, df_log_failed)

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
        after_before = datetime.now().strftime('%Y-%m-%d')
        generate_all_day_report(after_before, after_before)

if __name__ == "__main__":
    main()
