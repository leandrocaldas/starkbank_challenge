import starkbank
import time

def get_pix_data_log(created_transfers, pix_quantity):
    transfer_ids = [transfer.id for transfer in created_transfers]
    success_failed = []
    iteration = 0
    while len(success_failed) < pix_quantity and iteration < 4:
        time.sleep(15)
        success_failed = [
            log for log in starkbank.transfer.log.query(
                transfer_ids=transfer_ids, types=['success', 'failed']
                )
            ]
        logs = [
            log for log in starkbank.transfer.log.query(
                transfer_ids=transfer_ids
                )
            ]
        
        iteration +=1
    return data_generate(logs)

def get_pix_data_log_all_day(after, before):
    logs = [
        log for log in starkbank.transfer.log.query(
            after=after, before=before
            )
        ]
    return data_generate(logs)

def data_generate(logs):
    data = {
        "id": [log.transfer.id for log in logs],
        "type": [log.type for log in logs],
        "created": [log.created for log in logs],
        "errors": [log.errors for log in logs],
    }
    return data