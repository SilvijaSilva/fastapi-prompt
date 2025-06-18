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

