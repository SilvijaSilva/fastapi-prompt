from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date
import os

app = FastAPI()

class BankAccount(BaseModel):
    id: int
    type: str
    person_name: str
    address: str


def write_bankaccount_to_file(bankaccount: BankAccount):
    with open("bank_accounts.txt", "a") as file:
        file.write(f"{bankaccount.id}, {bankaccount.type}, {bankaccount.person_name}, {bankaccount.address}\n")

def read_bankaccounts_from_file():
    bank_accounts = []
    with open("bank_accounts.txt", "r") as file:
        for line in file:
            id, type, person_name, address = line.strip().split(", ")
            bank_accounts.append(BankAccount(id=int(id), type=type, person_name=person_name, address=address))
    
    return bank_accounts

def delete_bankaccount_from_file(bankaccount_id_to_delete: int):
    bank_accounts = read_bankaccounts_from_file()
    bank_accounts = [account for account in bank_accounts if account.id != bankaccount_id_to_delete]

    with open("bank_accounts.txt", "w") as file:
        for account in bank_accounts:
            file.write(f"{account.id}, {account.type}, {account.person_name}, {account.address}\n")

if not os.path.exists("bank_accounts.txt"):
        open("bank_accounts.txt", "w").close()

# type hint for a list of bank accounts
bank_accounts: list[BankAccount] = read_bankaccounts_from_file()

@app.post("/bank_accounts/")
def create_bank_account(account: BankAccount):
    bank_accounts.append(account)
    write_bankaccount_to_file(account)
    return {"message": "Bank account created successfully"}

@app.get("/bank_accounts/")
def get_bank_accounts():
    return bank_accounts

@app.get("/bank_accounts/{account_id}")
def get_bank_account(account_id: int):
    for account in bank_accounts:
        if account.id == account_id:
            return account
    return {"message": "Bank account not found"}

@app.delete("/bank_accounts/{account_id}")
def delete_bank_account(account_id: int):
    global bank_accounts
    bank_accounts = [account for account in bank_accounts if account.id != account_id]
    return {"message": "Bank account deleted successfully"}


class Payment(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    amount_in_euros: int
    payment_date: date

def write_payment_to_file(payment: Payment):
    with open("payments.txt", "a") as file:
        file.write(f"{payment.id}, {payment.from_account_id}, {payment.to_account_id}, {payment.amount_in_euros}, {payment.payment_date}\n")

def read_payments_from_file():
    payments = []
    with open("payments.txt", "r") as file:
        for line in file:
            id, from_account_id, to_account_id, amount_in_euros, payment_date = line.strip().split(", ")
            payments.append(Payment(id=int(id), from_account_id=int(from_account_id), to_account_id=int(to_account_id), amount_in_euros=int(amount_in_euros), payment_date=date.fromisoformat(payment_date)))

    return payments

def delete_payment_from_file(payment_id_to_delete: int):
    payments = read_payments_from_file()
    payments = [payment for payment in payments if payment.id != payment_id_to_delete]

    with open("payments.txt", "w") as file:
        for payment in payments:
            file.write(f"{payment.id}, {payment.from_account_id}, {payment.to_account_id}, {payment.amount_in_euros}, {payment.payment_date}\n")

if not os.path.exists("payments.txt"):
        open("payments.txt", "w").close()

# type hint for a list of payments
payments: list[Payment] = read_payments_from_file()

@app.post("/payments/")
def create_payment(payment: Payment):
    payments.append(payment)
    write_payment_to_file(payment)
    return {"message": "Payment created successfully"}

@app.get("/payments/")
def get_payments():
    return payments

@app.get("/payments/{payment_id}")
def get_payment(payment_id: int):
    for payment in payments:
        if payment.id == payment_id:
            return payment
    return {"message": "Payment not found"}

@app.delete("/payments/{payment_id}")
def delete_payment(payment_id: int):
    global payments
    payments = [payment for payment in payments if payment.id != payment_id]
    delete_payment_from_file(payment_id)
    return {"message": "Payment deleted successfully"}