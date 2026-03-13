from schemas import Transaction


def preproc(data: str) -> bool:
    
    try:
        data = Transaction.parse_raw(data)
        return data
    
    except ValueError as e:
        return e
    
def preproc_features(transaction: Transaction):
    pass