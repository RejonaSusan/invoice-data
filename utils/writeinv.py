def write_invoices(invoices_data, table, empty_row):

    for idx, invoice in enumerate(invoices_data):
        row = []
        vendor_name = invoice.fields.get("VendorName")
        if vendor_name:
            row.append(vendor_name.value if vendor_name else "")
        invoice_id = invoice.fields.get("InvoiceId")
        if invoice_id:
            row.append(invoice_id.value if invoice_id else "")

        invoice_date = invoice.fields.get("InvoiceDate")
        if invoice_date:
            row.append(invoice_date.value if invoice_date else "")

        total_due = invoice.fields.get("AmountDue")
        if total_due:
            row.append(total_due.value if total_due else "")
        
        invoice_total = invoice.fields.get("InvoiceTotal")
        if invoice_total:
            row.append(invoice_total.value if invoice_total else "")

        for col_num, value in enumerate(row):
            table.write(empty_row, col_num, str(value))
        empty_row += 1
