#!/usr/bin/env python3.8

test = {'id': 42578, 'firstName': 'anais', 'lastName': 'Ly', 'iban': 'FR7630001005746963581943647', 'amount': 86.11, 'idCard': '100000', 'latitude': 51.3, 'longitude': -0.7, 'createDate': 1608301933009,
        'idServerTransactionProcessing': 'FR-SIPIOS1002941234567890595', 'merchantCodeCategory': '2', 'merchantId': '4', 'cardType': 'silver', 'transactionProcessingDuration': 122, 'bitcoinPriceAtTransactionTime': 10305, 'ethPriceAtTransactionTime': 290}


def is_transaction_fraudulent(transaction, transactions_set):
    fraudulent_names = ["fraud", "frauder", "superman", "robinwood", "picsou"]
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
        transaction["idCard"],
        transaction["idServerTransactionProcessing"],
        transaction["merchantCodeCategory"],
        transaction["merchantId"],
        transaction["cardType"],
        transaction["transactionProcessingDuration"],
        transaction["bitcoinPriceAtTransactionTime"],
        transaction["ethPriceAtTransactionTime"]
    )

    if common_transaction in transactions_set:
        return True
    else:
        transactions_set.add(common_transaction)

    return False


if __name__ == "__main__":
    print(is_transaction_fraudulent(test, set()))
