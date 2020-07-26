#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.client
import json

ApiKey = "---YOUR-API-KEY-HERE---"
conn = http.client.HTTPSConnection("api.sendgrid.com")

def GetAllList(pagesize):
	payload = "{}"
	headers = { 'authorization': "Bearer " + ApiKey }
	conn.request("GET", "/v3/marketing/lists?page_size="+str(pagesize), payload, headers)
	res = conn.getresponse()
	data = res.read()
	json_data = json.loads(data.decode("utf-8"))
	for i in range(len(json_data['result'])):
			print("List name: " + str(json_data['result'][i]['name'].encode("utf-8")))
			print("List ID: " + str(json_data['result'][i]['id']))
			print("List user count: " + str(json_data['result'][i]['contact_count']))
			print(str(30 * "-"))

def AddUserIntoList(listId, firstname, lastname, email):
	payload = '{\"list_ids\":[\"'+str(listId)+'\"],\"contacts\":[{\"address_line_1\":\"\",\"address_line_2\":\"\",\"alternate_emails\":[\"'+str(email)+'\"],\"city\":\"\",\"country\":\"\",\"email\":\"'+str(email)+'\",\"first_name\":\"'+str(firstname)+'\",\"last_name\":\"'+str(lastname)+'\",\"postal_code\":\"\",\"state_province_region\":\"\",\"custom_fields\":{}}]}'
	headers = {
		'authorization': "Bearer " + ApiKey,
		'content-type': "application/json"
		}
	conn.request("PUT", "/v3/marketing/contacts", payload, headers)
	res = conn.getresponse()
	data = res.read()
	if "job_id" in data.decode("utf-8"):
		print("The user has been added successfully into list.")
	else:
		print("The user cannot be added to the list. Reason: " + str(data.encode("utf-8")))

def GetUserInformations(username,listId):
	payload = "{\"query\":\"email LIKE '" + str(username) + "%' AND CONTAINS(list_ids, '"+str(listId)+"')\"}"
	headers = {
	    'authorization': "Bearer " + ApiKey,
	    'content-type': "application/json"
	    }
	conn.request("POST", "/v3/marketing/contacts/search", payload, headers)
	res = conn.getresponse()
	json_data = json.loads(res.read())
	if not 'result' in json_data or len(json_data['result']) == 0:
		print("User not found.\n\n")
	else: 
		for i in range(len(json_data['result'])):
			print("User email : " + json_data['result'][i]['email'])
			print("User ID: " + json_data['result'][i]['id'])
			print("List ID: " + json_data['result'][i]['list_ids'][0])
			print(str(30 * "-"))

def UserDelete(userId, listId):
	payload = "{}"
	headers = { 'authorization': "Bearer " + ApiKey }
	conn.request("DELETE", "/v3/marketing/lists/"+str(listId)+"/contacts?contact_ids=" +str(userId)+", payload, headers)")
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))

	payload = "{}"
	headers = { 'authorization': "Bearer " + ApiKey }
	conn.request("DELETE", "/v3/marketing/lists/" + str(listId) + "/contacts?contact_ids=" + str(userId) + "", payload, headers)
	res = conn.getresponse()
	data = res.read()
	if "job_id" in data.decode("utf-8"):
		print("The user has been removed successfully.")
	else:
		print("The user cannot be removed. Sebebi : " + str(data.encode("utf-8")))

if __name__ =="__main__":
	while True:
		print("1. Search some user")
		print("2. Remove user from list")
		print("3. Add user into list")
		print("4. List details")
		option = raw_input("Please select an option: (1, 2, 3, 4): ")

		if option=="1":
			listId = raw_input("Enter List ID ınformation to which list you want to search: ")
			username = raw_input("Search: ")
			GetUserInformations(username,listId)	
		elif option=="2":
			listId = raw_input("Which list do you want to remove user? (List ID): ")
			userId = raw_input("Which user do you want to remove? (User ID): ")
			UserDelete(userId,listId)
		elif option=="3":
			GetAllList(100)
			listId = raw_input("Enter List ID information to which list you want to add the user (List ID): ")
			firstname = raw_input("Firstname: ")
			lastname = raw_input("Lastname: ")
			email = raw_input("Email: ")
			AddUserIntoList(listId,firstname,lastname,email)
		elif option=="4":
			GetAllList(100)
		else: 
			print("You entered something wrong..\n\n")
