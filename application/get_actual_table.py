def get_actual_table(prices: dict[str, int], table: list[list]) -> list[list]:
    for r in range(len(table)):
        actual_price = prices.get(table[r][0], 'Unknown')
        table[r][3] = actual_price

        if actual_price != 'Unknown':
            start_price = float(table[r][1])
            table[r][2] = (float(actual_price) - start_price) / start_price * 100

        return table
