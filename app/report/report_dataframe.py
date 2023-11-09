import pandas as pd

def _filter_event_data(data_log, event_type):
    """
    Filter event data by event type.

    Parameters:
        data_log (DataFrame): The input data log.
        event_type (str): The event type to filter.

    Returns:
        DataFrame: Filtered data containing 'id', 'created', and 'errors' 
        (if event_type is 'failed').
    """
    df = pd.DataFrame(data_log)
    columns = ['id', 'created']
    if event_type == 'failed':
        columns.append('errors')
    return df[df['type'] == event_type][columns]

def _merge_event_data(event1_df, event2_df, event1_suffix, event2_suffix):
    """
    Merge two event data DataFrames.

    Parameters:
        event1_df (DataFrame): The first event DataFrame.
        event2_df (DataFrame): The second event DataFrame.
        event1_suffix (str): Suffix for the first event's columns.
        event2_suffix (str): Suffix for the second event's columns.

    Returns:
        DataFrame: Merged data with specified suffixes.
    """
    merged_df = event1_df.merge(
        event2_df, on='id', suffixes=(event1_suffix, event2_suffix),
        how='outer')
    return merged_df

def _calculate_time_in_seconds(end_time_series, start_time_series):
    """
    Calculate time difference in seconds between two time series.

    Parameters:
        end_time_series (Series): Series containing end timestamps.
        start_time_series (Series): Series containing start timestamps.

    Returns:
        Series: Time differences in seconds.
    """
    start_time_series = pd.to_datetime(start_time_series)
    end_time_series = pd.to_datetime(end_time_series)
    time_difference = end_time_series - start_time_series
    return time_difference.dt.total_seconds()

def _calculate_average_times(complete_report, event_type):
    """
    Calculate average times for successful and failed events.

    Parameters:
        complete_report (DataFrame): Complete report containing event times.
        event_type (str): The event type for which to calculate average times 
        ('success' or 'failed').

    Returns:
        DataFrame: DataFrames for average times of success or failed events.
    """
    valid_events = complete_report[
        complete_report[f'sending_to_{event_type}(s)'] != 0]
    
    average_times = pd.DataFrame({
        event_type: valid_events[
            f'created_to_sending(s)'].count(),
        
        'created_to_sending_average(s)':valid_events[
            f'created_to_sending(s)'].mean(),
        
        f'sending_to_{event_type}_average(s)': valid_events[
            f'sending_to_{event_type}(s)'].mean(),
        
        f'total_{event_type}_average(s)': valid_events['total_time(s)'].mean(),
    }, index=[0])
    
    if event_type == 'failed':
        new_column_name = f'{event_type}_to_refunded_average(s)'
        new_column_data = valid_events[f'{event_type}_to_refunded(s)'].mean()
        average_times.insert(
            len(average_times.columns) - 1, new_column_name, new_column_data)

    return average_times

def _calculate_percentage(success_df, failed_df):
    total_success = success_df['success']
    total_failed = failed_df['failed']
    success_percentage = (
        success_df['success'] / (total_success + total_failed)) * 100
    
    failed_percentage = (
        failed_df['failed'] / (total_success + total_failed)) * 100
    
    success_df.insert(1, 'Success %', success_percentage)
    failed_df.insert(1, 'Failed %', failed_percentage)
    return success_df, failed_df

def _calculate_and_fill_time_differences(merged_df):
    """
    Calculate and fill time differences between different events.

    Parameters:
        merged_df (DataFrame): Merged data containing event times.
    """
    time_columns = [
        ('created_sending', 'created', 'created_to_sending(s)'),
        ('created_success', 'created_sending', 'sending_to_success(s)'),
        ('created_failed', 'created_sending', 'sending_to_failed(s)'),
        ('created_refunded', 'created_failed', 'failed_to_refunded(s)')
    ]
    for end_column, start_column, result_column in time_columns:
        merged_df[result_column] = _calculate_time_in_seconds(
            merged_df[end_column], merged_df[start_column]).fillna(0)
    merged_df['total_time(s)'] = (
        merged_df['created_to_sending(s)']
        + merged_df['sending_to_success(s)']
        + merged_df['sending_to_failed(s)']
        + merged_df['failed_to_refunded(s)']
    )

def _merge_data_frames(data_log):
    """
    Merge different event dataframes based on event type.

    Parameters:
        data_log (DataFrame): Data log containing different event types.

    Returns:
        DataFrame: Merged data for further analysis.
    """
    event_types = ['created', 'sending', 'success', 'failed', 'refunded']
    data_frames = {
        event_type: _filter_event_data(data_log, event_type) 
        for event_type in event_types}

    # Merge data frames
    merged_df = data_frames['created']
    for event_type in event_types[1:]:
        if event_type == 'failed':
            df_log_failed = data_frames[event_type][['id', 'errors']]
        suffix = f'_{event_type}' if event_type != 'created' else ''
        merged_df = _merge_event_data(
            merged_df, data_frames[event_type], '', suffix)
    return df_log_failed, merged_df

def generate_pix_report_data(data_log):
    """
    Generate a PIX report and calculate average times and % for success and 
    failed events.

    Parameters:
        data_log (DataFrame): Input data log.

    Returns:
        dict: A dictionary containing average times for success and failed 
        events, and an error report.
    """
    # Extract data frames for different event types
    df_log_failed, merged_df = _merge_data_frames(data_log)

    # Calculate and fill time differences
    _calculate_and_fill_time_differences(merged_df)
    
    # Extract required columns
    new_df = merged_df[['id', 'created_to_sending(s)', 'sending_to_success(s)',
                        'sending_to_failed(s)', 'failed_to_refunded(s)',
                        'total_time(s)']]

    # Calculate average times for success and failed
    average_times_success = _calculate_average_times(new_df, 'success')
    average_times_failed = _calculate_average_times(new_df, 'failed')
    
    # Calculate and return the percentage data
    df_success, df_failed = _calculate_percentage(
        average_times_success, average_times_failed)
    
    return df_success, df_failed, df_log_failed