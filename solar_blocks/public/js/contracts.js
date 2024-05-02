frappe.ui.form.on('Contracts', {
    refresh(frm) {
        if(frm.doc.email && frm.doc.attach_contract && frm.doc.name1){
            frm.add_custom_button(__("Upload Contract First"), function(){
                frappe.call({
                    method: 'zohosign.api.docsign',
                     args: { 
                        "client_id":"1000.QSU22EBIADBWHSSJUPZ2EB91N8TN4C",
                        "refresh_token":"1000.92cfefcc3ab63fbf3cab9a19e8d41a1a.5fdef19fa0e1bf10019e2975528f1d79",
                        "client_secret":"ad50a49c9e8d49afb82ba8c3bf4186bda3b16fdcc0",
                         'file_url': frm.doc.attach_contract, 
                         'request_name': frm.doc.name, 
                         'recipient_name': frm.doc.name1, 
                         'recipient_email': frm.doc.email
                    //  'access_token':frm.doc.access_token
                     }, 
                    callback: function (r) {
                        // frappe.msgprint(r);
                        console.log(r)
                    },
                });
                });
    }
    },
    status(frm) {
	    if(frm.doc.status=="Signed"){
            frappe.call({
            method: 'update_contract_status_on_opportunity',
                args:
                {
                    'opportunity':frm.doc.opportunity,
                },
                callback: function(r) {
                }
            })
	    }
	},
	before_save(frm){
	    var con="https://solarblocks.onehash.is/api/method/frappe.utils.print_format.download_pdf?doctype=Contracts&name="+cur_frm.doc.name+"&format=Sample%20Solar%20Agreement&no_letterhead=0&letterhead=Solar%20Block&settings=%7B%7D&_lang=en"
	    frm.set_value('contract_attachment_link',con)
	    
	},
	refresh(frm){
        frm.add_custom_button(__("Go back to Opportunity"), function(){
            frappe.set_route('Form', 'Opportunity', frm.doc.opportunity)
        });	
        
        frm.add_custom_button(__("Send Mail"), function(){
   
   
	    var cons="https://solarblocks.onehash.is/api/method/frappe.utils.print_format.download_pdf?doctype=Contracts&name="+cur_frm.doc.name+"&format=Sample%20Solar%20Agreement&no_letterhead=0&letterhead=Solar%20Block&settings=%7B%7D&_lang=en"
        var con =encodeURIComponent(cons)
        console.log(con,"con")
        var url = "https://solarblocks.onehash.is/contract/new?customer_name="+cur_frm.doc.name+"&email="+cur_frm.doc.email+"&url_att="+con;
        console.log(url,"nnnnnnnnnnn")
            frappe.msgprint("Contract is send for Signature")
    
           var link = url
           console.log(link)
           frm.set_value("web_form_url" , link)
            frappe.call({
                method:'doc_submission_mail',
                type:"POST",
                args : {
                email_id : frm.doc.email,
                url:link
                },
                callback: function(response) {
                console.log(response);
                }
            })
           frm.save()
    })
	}
});

