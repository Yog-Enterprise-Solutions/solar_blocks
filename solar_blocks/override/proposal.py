import frappe

def api_call(doc,method=None):
    # import requests

    url = "https://accounts.zoho.in/oauth/v2/token?refresh_token=1000.fd5ff1cf53c84f20e6ba9e0b4306d522.00994a550c4450e80e596e2671981ef5&client_id=1000.KEBX6XAN6ZLHX734ALY4NQ8378X9AO&client_secret=33451dcffc5dbb2e02787789928069dda01b284b5d&redirect_uri=https%3A%2F%2Fsign.zoho.com&grant_type=refresh_token"

    payload = {}
    headers = {
    'Cookie': 'stk=7d3f0f6cdb8923d655a0e965277b975a; 6e73717622=4440853cd702ab2a51402c119608ee85; JSESSIONID=8EF592361CA7C71932AC1B71F41E5D0F; _zcsr_tmp=de4477f6-8ca6-4ef7-842e-45f335d4c20b; iamcsr=de4477f6-8ca6-4ef7-842e-45f335d4c20b'
    }

    response = frappe.make_post_request(url, headers=headers, data=payload)

    frappe.response['message']=response

















    # request_data = frappe.form_dict
    # files = request_data.get('file')
    # # frappe.response['message']=files

    # url = "https://sign.zoho.in/api/v1/requests"

    # payload = {
    #     'data': {
    #       "requests": {
    #         "request_name": "NEW DOC2 ",
    #         "actions": [
    #           {
    #             "recipient_name": "NNNNNNNNNNNNNNNNNNN",
    #             "recipient_email": "nishita@onehash.ai",
    #             "action_type": "SIGN",
    #             "private_notes": "Please get back to us for further queries",
    #             "signing_order": 0,
    #             "verify_recipient": False
    #           }
    #         ],
    #         "expiration_days": 1,
    #         "is_sequential": True,
    #         "email_reminders": True,
    #         "reminder_period": 8
    #       }
    #     },
    # }
    # headers = {
    #     'Authorization': 'Zoho-oauthtoken 1000.e063e3289324300f4f3fa6d8d56f8e27.10137c1783d2e1db2e0e88444ed7a0e2',
    #     'Cookie': 'JSESSIONID=6A8CB3994904428BB637FFF097BF72D0; _zcsr_tmp=217e8094-1772-4b99-8d90-dec7497c4dfd; c61ac045a3=113a9c1fb3cc3c4bbabfd0f34ab32379; zscsrfcookie=217e8094-1772-4b99-8d90-dec7497c4dfd'
    # }

    # response=frappe.make_post_request(url, headers=headers,data={'payload': payload,'files':files})
    # frappe.response['message']=response

    # request_data = frappe.form_dict
    # files = request_data.get('file')
    # # frappe.response['message']=files

    # url = "https://sign.zoho.in/api/v1/requests"

    # payload = {
    #     'data': {
    #       "requests": {
    #         "request_name": "NEW DOC2 ",
    #         "actions": [
    #           {
    #             "recipient_name": "NNNNNNNNNNNNNNNNNNN",
    #             "recipient_email": "nishita@onehash.ai",
    #             "action_type": "SIGN",
    #             "private_notes": "Please get back to us for further queries",
    #             "signing_order": 0,
    #             "verify_recipient": False
    #           }
    #         ],
    #         "expiration_days": 1,
    #         "is_sequential": True,
    #         "email_reminders": True,
    #         "reminder_period": 8
    #       }
    #     },
    # }
    # headers = {
    #     'Authorization': 'Zoho-oauthtoken 1000.e063e3289324300f4f3fa6d8d56f8e27.10137c1783d2e1db2e0e88444ed7a0e2',
    #     'Cookie': 'JSESSIONID=6A8CB3994904428BB637FFF097BF72D0; _zcsr_tmp=217e8094-1772-4b99-8d90-dec7497c4dfd; c61ac045a3=113a9c1fb3cc3c4bbabfd0f34ab32379; zscsrfcookie=217e8094-1772-4b99-8d90-dec7497c4dfd'
    # }

    # response=frappe.make_post_request(url, headers=headers,data={'payload': payload,'files':files})
    # frappe.response['message']=response
