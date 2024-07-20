// ---------------calculate amount in child table--------------
function calculate_amount(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    if (row.qty && row.rate) {
        let amount = row.qty * row.rate;
        frappe.model.set_value(cdt, cdn, 'amount', amount);
    }
}



// -----------------------calculate total of each table individyally-----------------------

frappe.ui.form.on('BOM Item', {
    qty: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    }
});

