

for idx, invoice in enumerate(invoices.documents):
    row = []
    print("--------Recognizing invoice #{}--------".format(idx + 1))
    vendor_name = invoice.fields.get("VendorName")
    if vendor_name:
        row.append(vendor_name.value if vendor_name else "")
        
    vendor_address = invoice.fields.get("VendorAddress")
    if vendor_address:
        row.append(vendor_address.value if vendor_name else "")

    vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
    if vendor_address_recipient:
        row.append(vendor_address_recipient.value if vendor_name else "")

    customer_name = invoice.fields.get("CustomerName")
    if customer_name:
        row.append(customer_name.value if vendor_name else "")

    customer_id = invoice.fields.get("CustomerId")
    if customer_id:
        row.append(vendor_name.value if vendor_name else "")

    customer_address = invoice.fields.get("CustomerAddress")
    if customer_address:
        row.append(customer_address.value if vendor_name else "")

    customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
    if customer_address_recipient:
        row.append(customer_address_recipient.value if vendor_name else "")

    invoice_id = invoice.fields.get("InvoiceId")
    if invoice_id:
        row.append(invoice_id.value if vendor_name else "")

    invoice_date = invoice.fields.get("InvoiceDate")
    if invoice_date:
        row.append(invoice_date.value if vendor_name else "")

    invoice_total = invoice.fields.get("InvoiceTotal")
    if invoice_total:
        row.append(invoice_total.value if vendor_name else "")

    due_date = invoice.fields.get("DueDate")
    if due_date:
        row.append(due_date.value if vendor_name else "")

    purchase_order = invoice.fields.get("PurchaseOrder")
    if purchase_order:
        row.append(purchase_order.value if vendor_name else "")

    billing_address = invoice.fields.get("BillingAddress")
    if billing_address:
        row.append(billing_address.value if vendor_name else "")

    billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
    if billing_address_recipient:
        row.append(billing_address_recipient.value if vendor_name else "")

    shipping_address = invoice.fields.get("ShippingAddress")
    if shipping_address:
        row.append(shipping_address.value if vendor_name else "")

    shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
    if shipping_address_recipient:
        row.append(shipping_address_recipient.value if vendor_name else "")

    for idx, item in enumerate(invoice.fields.get("Items").value):
        item_description = item.value.get("Description")
        if item_description:
            row.append(item_description.value if vendor_name else "")

        item_quantity = item.value.get("Quantity")
        if item_quantity:
            row.append(item_quantity.value if vendor_name else "")

        unit = item.value.get("Unit")
        if unit:
            row.append(unit.value if vendor_name else "")

        unit_price = item.value.get("UnitPrice")
        if unit_price:
            row.append(unit_price.value if vendor_name else "")

        product_code = item.value.get("ProductCode")
        if product_code:
            row.append(product_code.value if vendor_name else "")

        item_date = item.value.get("Date")
        if item_date:
            row.append(item_date.value if vendor_name else "")

        tax = item.value.get("Tax")
        if tax:
            row.append(tax.value if vendor_name else "")

        amount = item.value.get("Amount")
        if amount:
            row.append(amount.value if vendor_name else "")

    subtotal = invoice.fields.get("SubTotal")
    if subtotal:
        row.append(subtotal.value if vendor_name else "")

    total_tax = invoice.fields.get("TotalTax")
    if total_tax:
        row.append(total_tax.value if vendor_name else "")

    previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
    if previous_unpaid_balance:
        row.append(previous_unpaid_balance.value if vendor_name else "")

    amount_due = invoice.fields.get("AmountDue")
    if amount_due:
        row.append(amount_due.value if vendor_name else "")

    service_start_date = invoice.fields.get("ServiceStartDate")
    if service_start_date:
        row.append(service_start_date.value if vendor_name else "")

    service_end_date = invoice.fields.get("ServiceEndDate")
    if service_end_date:
        row.append(service_end_date.value if vendor_name else "")

    service_address = invoice.fields.get("ServiceAddress")
    if service_address:
        row.append(service_address.value if vendor_name else "")

    service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
    if service_address_recipient:
        row.append(service_address_recipient.value if vendor_name else "")

    remittance_address = invoice.fields.get("RemittanceAddress")
    if remittance_address:
        row.append(remittance_address.value if vendor_name else "")

    remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
    if remittance_address_recipient:
        row.append(remittance_address_recipient.value if vendor_name else "")
