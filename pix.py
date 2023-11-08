import os
import starkbank
from auth import get_authentication
import random
import string

bank_code = os.getenv("bank_code")
tax_id = os.getenv("tax_id")
branch_code = os.getenv("branch_code")
account_number = os.getenv("account_number")
tax_id = os.getenv("tax_id")

starkbank.user = get_authentication()

def create_pix(pix_quantity, pix_amount):
    """
    Create multiple PIX transfers at specified intervals.

    Args:
        pix_quantity (int): Number of PIX transfers to create.
        pix_amount (int): Amount for each PIX transfer.
        pix_interval (int): Time interval in hours between PIX transfers.

    Returns:
        List of created PIX transfers.
    """
    transfers = []
    # pix_interval_minutes = pix_interval * 60
    # total_transfers = (24 / pix_interval) * pix_quantity

    for pix_id in range(pix_quantity):
        transfer = _create_pix_list(pix_amount, pix_id)
        transfers.append(transfer)
    return starkbank.transfer.create(transfers)

def _create_pix_list(amount, pix_id):
    """
    Create a single PIX transfer.

    Args:
        amount (int): Amount for the PIX transfer.

    Returns:
        Created PIX transfer object.
    """
    characters = string.ascii_letters + string.digits
    try:
        transfer = starkbank.Transfer(
            amount=amount,
            tax_id=tax_id,
            name=f"Automation test PIX id {pix_id}",
            bank_code=bank_code,
            branch_code=branch_code,
            account_number=account_number,
            account_type="checking",
            external_id=''.join(random.choice(characters) for _ in range(18))
        )
        return transfer
    except starkbank.error.InputErrors as exception:
        for error in exception.errors:
            print(error.code)
            print(error.message)
