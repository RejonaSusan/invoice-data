
def find_empty_row(table, headers):
    def is_row_empty(table, row_index):
        for col_index in range(table.num_cols):
            cell = table.cell(row_index, col_index)
            if cell and cell.value:
                return False
        return True

    rows = table.rows()
    empty_row = None

    for i in range(len(rows)):
        if is_row_empty(table, i):
            empty_row = i
            break

    if empty_row is None:
        empty_row = table.num_rows

    if empty_row == 0:
        for col_num, header in enumerate(headers):
            table.write(0, col_num, header)
        empty_row += 1

    return empty_row
