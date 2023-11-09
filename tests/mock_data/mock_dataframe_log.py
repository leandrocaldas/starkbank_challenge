import pandas as pd


def get_df_logs():
    df_success = {'success': [7],
            'Success %': [70.0],
            'created_to_sending_average(s)': [1.26443],
            'sending_to_success_average(s)': [17.927948],
            'total_success_average(s)': [19.192378]}
    df_failed = {'failed': [3],
            'failed %': [30.0],
            'created_to_sending_average(s)': [1.26443],
            'failed_to_refunded_average(s)': [1.227948],
            'sending_to_failed_average(s)': [17.927948],
            'total_failed_average(s)': [19.192378]}
    df_log_failed = {'id': [
        4710795078270976, 5766326240935936, 6399644938534912],
                     'errors': [['Specified amount is zero'],
                                ['Target account is closed'],
                                ['The specified amount is greater than the maximo']]}

    return pd.DataFrame(df_success), pd.DataFrame(df_failed), pd.DataFrame(df_log_failed)

