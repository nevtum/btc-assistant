import time


def export():
    from dynamodb import DynamoDBReader

    storage = DynamoDBReader("crypto-market-data")
    for data in storage.enumerate_records("BTC"):
        print(data)
        time.sleep(0.01)


if __name__ == "__main__":
    export()
