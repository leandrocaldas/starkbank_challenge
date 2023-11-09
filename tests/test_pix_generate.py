import os
import starkbank
from app.auth import get_authentication

from app.pix_generate import create_pix, _create_pix_list

def test_create_pix():
    starkbank.user = get_authentication()

    pix_quantity = 3
    pix_amount = 100

    transfers = create_pix(pix_quantity, pix_amount)
    assert len(transfers) == pix_quantity

def test_create_pix_list():
    amount = 100
    pix_id = 1

    transfer = _create_pix_list(amount, pix_id)
    assert isinstance(transfer, starkbank.Transfer)
    assert transfer.amount == amount
    assert transfer.tax_id == os.getenv("tax_id", "630.388.220-00")
    assert transfer.bank_code == os.getenv("bank_code", "90400888")
    assert transfer.branch_code == os.getenv("branch_code", "8977")
    assert transfer.account_number == os.getenv("account_number", "07218468-4")
    assert transfer.account_type == "checking"

