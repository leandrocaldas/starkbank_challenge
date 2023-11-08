import pandas as pd

def generate_pix_report(data_log):
    """
    Generate a PIX report and calculate average times for success 
    and failed events.

    Parameters:
        data_log (DataFrame): Input data log.

    Returns:
        dict: A dictionary containing average times for success and failed 
        events, and an error report.
    """
    event_types = ['created', 'sending', 'success', 'failed', 'refunded']
    data_frames = {event_type: _filter_event_data(
        data_log, event_type) for event_type in event_types}

    # Initialize merged_df with the 'created' DataFrame
    merged_df = data_frames['created']

    # Loop through the other event types and merge their DataFrames
    for event_type in event_types[1:]:
        if event_type == 'failed':
            failed_df = data_frames[event_type][['id', 'errors']]
        suffix = f'_{event_type}' if event_type != 'created' else ''
        merged_df = merge_event_data(
            merged_df, data_frames[event_type], '', suffix)

    calculate_and_fill_time_differences(merged_df)
    
    new_df = merged_df[['id', 'created_to_sending(s)',
                    'sending_to_success(s)', 'sending_to_failed(s)',
                    'failed_to_refunded(s)', 'total_time(s)']]

    average_times_success = calculate_average_times(new_df, 'success')
    average_times_failed = calculate_average_times(new_df, 'failed')

    return {
        'average_times_success': average_times_success,
        'average_times_failed': average_times_failed,
        'error_report': failed_df
    }

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

def merge_event_data(event1_df, event2_df, event1_suffix, event2_suffix):
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

def calculate_time_in_seconds(end_time_series, start_time_series):
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

def calculate_average_times(complete_report, event_type):
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
        f'{event_type}_qtd': valid_events[
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

def calculate_and_fill_time_differences(merged_df):
    time_columns = [
        ('created_sending', 'created', 'created_to_sending(s)'),
        ('created_success', 'created_sending', 'sending_to_success(s)'),
        ('created_failed', 'created_sending', 'sending_to_failed(s)'),
        ('created_refunded', 'created_failed', 'failed_to_refunded(s)')
    ]
    for end_column, start_column, result_column in time_columns:
        merged_df[result_column] = calculate_time_in_seconds(
            merged_df[end_column], merged_df[start_column]).fillna(0)
    merged_df['total_time(s)'] = (
        merged_df['created_to_sending(s)']
        + merged_df['sending_to_success(s)']
        + merged_df['sending_to_failed(s)']
        + merged_df['failed_to_refunded(s)']
    )
