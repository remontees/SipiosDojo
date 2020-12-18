#!/usr/bin/env python3.8

test = {'id': 42578, 'firstName': 'anais', 'lastName': 'Ly', 'iban': 'FR7630001005746963581943647', 'amount': 86.11, 'idCard': '100000', 'latitude': 51.3, 'longitude': -0.7, 'createDate': 1608301933009,
        'idServerTransactionProcessing': 'FR-SIPIOS1002941234567890595', 'merchantCodeCategory': '2', 'merchantId': '4', 'cardType': 'silver', 'transactionProcessingDuration': 122, 'bitcoinPriceAtTransactionTime': 10305, 'ethPriceAtTransactionTime': 290}


def outer():
    id_last_card = None
    last_amount = 0
    increment = None
    counter = None

    def is_transaction_fraudulent(transaction, transactions_set):
        nonlocal id_last_card
        nonlocal last_amount
        nonlocal increment
        nonlocal counter

        if id_last_card == transaction["idCard"] and (transaction["amount"] - last_amount) == increment and transaction["id"]-counter >= 3:
            id_last_card = transaction["idCard"]
            increment = transaction["amount"] - last_amount
            last_amount = transaction["amount"]
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

    return is_transaction_fraudulent(test, set())


if __name__ == "__main__":
    print(outer())
