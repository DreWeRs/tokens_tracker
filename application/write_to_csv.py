import csv


def write_to_csv(file_path: str, header_labels: list[str], table: list[list]) -> None:
    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(header_labels)
        for r in range(len(table)):
            row = []
            for c in range(len(table[r])):
                item = table[r][c]
                row.append(item)

            writer.writerow(row)
