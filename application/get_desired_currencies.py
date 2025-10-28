def get_desired_currencies(table: list[list]) -> list[str]:
    desired_currency = [elem[0] for elem in table]

    return desired_currency
