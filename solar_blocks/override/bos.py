import frappe

def safe_float_conversion(value):
    try:
        return float(value.replace(',', ''))
    except (ValueError, AttributeError):
        return 0.0  # or any default value you prefer


# Calculate profit and profit percentage
def calculate_and_set_profit(amount, grand_total, project):
    amount = safe_float_conversion(amount)

    custom_profit = amount - grand_total
    profit_per = (custom_profit / grand_total) * 100 if grand_total != 0 else 0

    frappe.db.set_value('Project', project, {'custom_profit': custom_profit, 'custom_profit_percentage': profit_per})






def calculate_totals_and_subtotal(doc, method=None):
    # Initialize totals for each group
    child_table=doc.totals_of__services

    totals = {
        'SOLAR ITEMS': 0,
        'ELECTRICAL': 0,
        'IRONRIDGE SKIRTS': 0,
        'ROOF TECH PITCHED ROOF ATTACHMENTS': 0,
        'UNIRAC FLAT ROOF': 0,
        'IRONRIDGE PITCHED ROOF': 0,
        'IRONRIDGE FLAT ROOF': 0,
        'CONDUITS AND ACCESORIES (METTALIC)': 0,
        'WIRES/CABLES': 0,
        'APPROVALS/FEES': 0,
        'MANPOWER': 0
    }

    group_to_field_map = {
        'SOLAR ITEMS': 'solar_items',
        'ELECTRICAL': 'electrical',
        'IRONRIDGE SKIRTS': 'ironridge_skirts',
        'ROOF TECH PITCHED ROOF ATTACHMENTS': 'roof_tech_pitched_roof_attachments',
        'UNIRAC FLAT ROOF': 'unirac_flat_roof',
        'IRONRIDGE PITCHED ROOF': 'ironridge_pitched_roof',
        'IRONRIDGE FLAT ROOF': 'ironridge_flat_roof',
        'CONDUITS AND ACCESORIES (METTALIC)': 'conduits_and_accesories_mettalic',
        'WIRES/CABLES': 'wires_cables',
        'APPROVALS/FEES': 'approvals_fees',
        'MANPOWER': 'manpower'
    }
    # Loop through each child table and sum the 'amount' field
    for group, field_name in group_to_field_map.items():
        child=getattr(doc, field_name, [])
        for i in child:
            if i.amount:
                totals[group]+=i.amount
    for key,value in totals.items():
        for i in child_table:
            if key==i.service_name:
                i.total=value
    
    # Calculate grand total
    grand_total = sum(totals.values())
    doc.sub_total = grand_total
    project=frappe.get_doc('Project',doc.project)
    project.custom_totals_of__services=[]
    for key, value in totals.items():
        project.append('custom_totals_of__services', {
            'service_name': key,
            'total': value
        })

    project.save()
    amount = project.cash_amount or project.financing_amount or project.lease_amount
    if isinstance(amount, str):
        amount = safe_float_conversion(amount)
    quoted_system_size=project.quoted_system_size
    if amount:
        calculate_and_set_profit(amount,grand_total,project.name)
    else:
        pass
    if quoted_system_size and amount:
        by_thousnd=float(quoted_system_size)*1000
        watt_price=float(quoted_system_size)/amount
        frappe.db.set_value('Project',project.name, {'custom_per_watt_price': watt_price})
    

