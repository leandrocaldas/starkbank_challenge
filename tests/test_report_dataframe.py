import os
from unittest.mock import patch, call
from app.report.generate_report import generate_reports
from tests.mock_data.mock_dataframe_log import get_df_logs


def test_generate_reports():
    # Mock the dataframes
    mock_df_success, mock_df_failed, mock_df_log_failed = get_df_logs()

    # Mock the external functions that interact with the file system
    with patch(
        'app.report.generate_report._create_directory'
        ) as mock_create_directory:
        
        with patch(
            'app.report.generate_report._get_folder_name'
            ) as mock_get_folder_name:
            with patch(
                'app.report.generate_report._dataframe_to_json_and_print'
                ) as mock_dataframe_to_json_and_print:
                # Mock the return values of the mocked functions
                mock_get_folder_name.return_value = 'test_folder'
                mock_create_directory.return_value = None

                # Call the function to be tested
                generate_reports(
                    mock_df_success, mock_df_failed, mock_df_log_failed)

                assert mock_create_directory.call_count == 2
                mock_create_directory.assert_any_call(
                    os.path.join('report_file','2023-11-09'))
                
                mock_create_directory.assert_any_call(
                    os.path.join('report_file', '2023-11-09', 'test_folder'))
                assert  mock_dataframe_to_json_and_print.call_count == 3
                expected_json_calls = [
                    call(mock_df_success, os.path.normpath(
                        'report_file/2023-11-09/test_folder/success.json')),
                    call(mock_df_failed, os.path.normpath(
                        'report_file/2023-11-09/test_folder/failed.json')),
                    call(mock_df_log_failed, os.path.normpath(
                        'report_file/2023-11-09/test_folder/errors.json'))
                ]
                mock_dataframe_to_json_and_print.assert_has_calls(
                    expected_json_calls, any_order=True)
                