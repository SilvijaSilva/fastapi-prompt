from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class BankAccount(BaseModel):
    id: int
    type: str
    person_name: str
    adress: str

# type hint for a list of bank accounts
bank_accounts: list[BankAccount] = []

@app.post("/bank_accounts/")
def create_bank_account(account: BankAccount):
    bank_accounts.append(account)
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

