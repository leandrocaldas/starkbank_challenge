import os
from tabulate import tabulate
from datetime import datetime

def _create_directory(path):
    """
    Cria um diretório se ele não existir.

    Args:
        path (str): O caminho do diretório a ser criado.

    Returns:
        None
    """
    base_path = os.path.basename(os.path.dirname(path))
    if not os.path.exists(path):
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        os.mkdir(path)

def _dataframe_to_json_and_print(df, file_path):
    """
    Salva um DataFrame em um arquivo JSON com formatação.

    Args:
        df (pandas.DataFrame): O DataFrame a ser salvo.
        file_path (str): O caminho do arquivo de destino.

    Returns:
        None
    """
    filename_with_extension = os.path.basename(file_path)
    filename, _ = os.path.splitext(filename_with_extension)
    if not df.dropna().empty:
        df.to_json(file_path, orient='records', indent=4)
        if not filename == 'errors':
            _print_report_on_console(f'Average times when {filename}', df)
        else:
            _print_report_on_console("Failed log", df)

def _get_folder_name(df_success, df_failed, pix_qtd):
    """
    Determina o nome da pasta com base nos DataFrames e no limite de PIX.

    Args:
        df_success (pandas.DataFrame): DataFrame de sucesso.
        df_failed (pandas.DataFrame): DataFrame de falha.
        pix_qtd (int): O limite de PIX.

    Returns:
        str: O nome da pasta.
    """
    if (df_success['success'].item() > pix_qtd 
        or df_failed['failed'].item() > pix_qtd):
        return 'completed_period'
    else:
        return datetime.now().strftime('%Y-%m-%d %H-%M-%S')

def _print_report_on_console(title, data_frame):
    """
    Print a DataFrame as a table with a title.

    Parameters:
        title (str): The title for the table.
        data_frame (pd.DataFrame): The DataFrame to be printed as a table.
    """
    print(title)
    print(tabulate(data_frame, headers='keys', tablefmt='pretty'))
    print("\n")

def generate_reports(df_success, df_failed, df_log_failed):
    """
    Gera arquivos de log com DataFrames em JSON com formatação e 
    organiza em diretórios.

    Args:
        df_success (pandas.DataFrame): DataFrame de sucesso.
        df_failed (pandas.DataFrame): DataFrame de falha.
        df_log_failed (pandas.DataFrame): DataFrame de log de falha.

    Returns:
        None
    """
    pix_qtd = int(os.getenv("PIX_QTD", 10))
    current_date = datetime.now().strftime('%Y-%m-%d')
    base_dir =  os.path.join('report_file',current_date)

    _create_directory(base_dir)
    
    folder_name = _get_folder_name(df_success, df_failed, pix_qtd)
    dir_path = os.path.join(base_dir, folder_name)

    _create_directory(dir_path)
    
    _dataframe_to_json_and_print(
        df_success, os.path.join(dir_path, "success.json"))
    _dataframe_to_json_and_print(
        df_failed, os.path.join(dir_path, "failed.json"))
    _dataframe_to_json_and_print(
        df_log_failed, os.path.join(dir_path, "errors.json"))
    
    