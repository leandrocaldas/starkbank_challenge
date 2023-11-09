import os
import starkbank
from app.auth import get_authentication
import random
import string

bank_code = os.getenv("bank_code", "90400888")
tax_id = os.getenv("tax_id", "630.388.220-00")
branch_code = os.getenv("branch_code", "8977")
account_number = os.getenv("account_number", "07218468-4")
starkbank.user = get_authentication()

def create_pix(pix_quantity, pix_amount):
    """
    Create multiple PIX transfers at specified intervals.

    Args:
        pix_quantity (int): Number of PIX transfers to create.
        pix_amount (int): Amount for each PIX transfer.
        
    Returns:
        List of created PIX transfers.
    """
    transfers = []
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
