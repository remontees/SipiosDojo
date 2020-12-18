#!/usr/bin/env python

import asyncio
import websockets
import requests
import json
import urllib.parse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

API_HOST = "aml.sipios.com"
API_PORT = "8080"
API_ENDPOINT_SCORE = "/transaction-validation"
API_WEBSOCKET_TRANSACTION = "ws://" + API_HOST + \
    ":" + API_PORT + "/transaction-stream/username/"

TEAM_NAME = "Les-deter-gens"
TEAM_PASSWORD = "your_password"

DATA = pd.read_csv("transactions_samples.csv")
X = DATA[['idServerTransactionProcessing', 'merchantId', 'merchantCodeCategory', 'cardType',
          'transactionProcessingDuration', 'bitcoinPriceAtTransactionTime', 'ethPriceAtTransactionTime']]  # Features
Y = DATA['isFraud']  # Labels
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.3)  # 70% training and 30% test
clf = RandomForestClassifier(n_estimators=100)
# clf.fit(X_train, Y_train)
# y_pred = clf.predict(X_test)
# print("Accuracy:", metrics.accuracy_score(Y_test, y_pred))


def send_value(transaction_id, is_fraudulent):
    url = "http://" + API_HOST + ":" + API_PORT + API_ENDPOINT_SCORE
    params = {
        'username': TEAM_NAME,
        'password': TEAM_PASSWORD
    }
    queryParams = urllib.parse.urlencode(params)
    url += "?" + queryParams

    # data to be sent to api
    data = {
        'fraudulent': is_fraudulent,
        'transaction': {
            'id': transaction_id
        }
    }

    # sending post request and saving response as response object
    requests.post(url=url, json=data, )


async def receive_transaction():
    uri = API_WEBSOCKET_TRANSACTION + TEAM_NAME
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                received = json.loads(await websocket.recv())
                # print(received)
                process_transactions(received)

            except:
                print('Reconnecting')
                websocket = await websockets.connect(uri)


def process_transactions(transactions):
    transactions_set = set()

    id_last_card = None
    last_amount = 0
    increment = None
    counter = None
    amount_fraud = False

    def is_transaction_fraudulent(transaction, transactions_set):
        nonlocal id_last_card
        nonlocal last_amount
        nonlocal increment
        nonlocal counter
        nonlocal amount_fraud

        if id_last_card == transaction["idCard"] and (transaction["amount"] - last_amount) == increment and transaction["id"]-counter >= 3:
            id_last_card = transaction["idCard"]
            increment = transaction["amount"] - last_amount
            last_amount = transaction["amount"]
            amount_fraud = True
            return True
        else:
            counter = transaction["id"]
            id_last_card = transaction["idCard"]
            increment = transaction["amount"] - last_amount
            last_amount = transaction["amount"]

        fraudulent_names = ["fraud", "frauder",
                            "superman", "robinwood", "picsou"]
        if transaction['firstName'] in fraudulent_names:
            return True

        fraudulent_coords = [(39.01, 125.73), (6.46, 3.24), (12.97, 77.58)]
        if (transaction['latitude'], transaction['longitude']) in fraudulent_coords:
            return True

        common_transaction = (
            transaction["firstName"],
            transaction["lastName"],
            transaction["iban"],
            transaction["amount"],
            transaction["idCard"]
        )

        if common_transaction in transactions_set:
            return True
        else:
            transactions_set.add(common_transaction)

        return False

    for transaction in transactions:
        is_fraud = is_transaction_fraudulent(transaction, transactions_set)
        print(transaction)
        print(is_fraud)
        # Sending data back to the API to compute score
        if is_fraud:
            send_value(transaction['id'], is_fraud)
            if amount_fraud == True:
                amount_fraud = False
                send_value(transaction['id']-1, is_fraud)
                send_value(transaction['id']-2, is_fraud)


    return True


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(receive_transaction())
