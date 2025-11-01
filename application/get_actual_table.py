def get_actual_table(prices: dict[str, float], table: list[list]) -> list[list]:
    for r in range(len(table)):
        actual_price = prices.get(table[r][0], "Unknown")
        table[r][4] = actual_price

        if actual_price != "Unknown":
            start_price = float(table[r][2])
            table[r][3] = f"{(float(actual_price) - start_price) / start_price * 100:.2f}%"

    return table
