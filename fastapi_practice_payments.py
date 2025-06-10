from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

app = FastAPI()

class Payment(BaseModel):
    id: int
    from_account_id: int
    to_account_id: int
    amount_in_euros: int
    payment_date: date

# type hint for a list of payments
payments: list[Payment] = []

@app.post("/payments/")
def create_payment(payment: Payment):
    payments.append(payment)
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
    return {"message": "Payment deleted successfully"}

