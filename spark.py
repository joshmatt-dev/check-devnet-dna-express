#####################################################################
#																	#
#	Module: 		spark.py				 						#
#	Author: 		Joshua Matthews 2017							#
#	Company: 		Cisco Systems									#
#	Description:	HTTP request functions for Cisco Spark API 		#
#																	#
#####################################################################

#####################################################################
#						Dependancy Imports							#
#####################################################################
import requests
import json

#####################################################################
#						Environment Settings						#
#####################################################################

# Cisco Spark
spark_uri = 'https://api.ciscospark.com/v1'

# Requests
requests.packages.urllib3.disable_warnings() 

#####################################################################
#						Function Definitions						#
#####################################################################

"""
Function: 		get_spark_user_info

Description:	Used to get Spark User identification information.
				A Spark person id can be obtained from the response.
				The person id could be used to join that user to a Spark room.

Arguments:		email - email address of user to request
				spark_token - Cisco Spark API user authentication token string

Return:			response - HTTP Request response
"""
def get_spark_user_info(email, spark_token):

	# Set API endpoint
	spark_endpoint = "/people"

	# Set request headers
	spark_headers = {'Authorization': 'Bearer ' + spark_token, 
					'Content-Type': 'application/json'}

	# Set request parameters
	spark_params = "?email=" + email

	# Send HTTP request
	r = requests.get(spark_uri+spark_endpoint+spark_params, headers=spark_headers, verify=False).json()

	# Return the HTTP response
	return r



"""
Function: 		get_spark_room_id

Description:	Used to get a Spark room id from a given room name.
				Useful for finding a room id for which to post messages, or add people.

Arguments:		room_name - Title of Cisco Spark room to query
				spark_token - Cisco Spark API user authentication token string

Return:			response - HTTP Request response
"""
def get_spark_room_id(room_name, spark_token):

	# Set API endpoint
	spark_endpoint = "/rooms"

	# Set request headers
	spark_headers = {'Authorization': 'Bearer ' + spark_token, 
					'Content-Type': 'application/json'}

	# Send HTTP request
	r = requests.get(spark_uri+spark_endpoint, headers=spark_headers, verify=False).json()

	# Parse response for room_id
	room_id = ""
	for items in r["items"]:
		if items["title"] == room_name:
			room_id = items["id"]

	# Return the HTTP response
	return room_id



"""
Function: 		get_spark_membership

Description:	Used to check which Spark rooms a user belongs.
				Useful to check if user already belongs to room with a given title.

Arguments:		person_id - Spark person id string
				spark_token - Cisco Spark API user authentication token string

Return:			response - HTTP Request response
"""
def get_spark_membership(person_id, spark_token):

	# Set API endpoint
	spark_endpoint = "/memberships"

	# Set request headers
	spark_headers = {'Authorization': 'Bearer ' + spark_token, 
					'Content-Type': 'application/json'}

	# Set request parameters
	spark_params = "?personId=" + person_id

	# Send HTTP request
	r = requests.get(spark_uri+spark_endpoint+spark_params, headers=spark_headers, verify=False)

	# Return the HTTP response
	return r



"""
Function: 		get_spark_room_memberships

Description:	Used to check which people belong to a given room.
				Useful for checking if a user already exists in a room.

Arguments:		room_id - Spark room id string
				spark_token - Cisco Spark API user authentication token string

Return:			response - HTTP Request response
"""
def get_spark_room_memberships(room_id, spark_token):

	# Set API endpoint
	spark_endpoint = "/memberships"

	# Set request headers
	spark_headers = {'Authorization': 'Bearer ' + spark_token, 
					'Content-Type': 'application/json'}

	# Set request parameters
	spark_params = "?roomId=" + room_id

	# Send HTTP request
	r = requests.get(spark_uri+spark_endpoint+spark_params, headers=spark_headers, verify=False)

	# Return the HTTP response
	return r



"""
Function: 		get_spark_message

Description:	Used to get a message content from the given message id.

Arguments:		message_id - the id string of the Cisco Spark message to get
				spark_token - Cisco Spark API user authentication token string

Return:			response - HTTP Request response
"""
def get_spark_message(message_id, spark_token):

	# Set API endpoint
	spark_endpoint = "/messages/"

	# Set request headers
	spark_headers = {'Authorization': 'Bearer ' + spark_token,
					'Content-Type': 'application/json'}

	# Send HTTP request
	r = requests.get(spark_uri+spark_endpoint+message_id, headers=spark_headers).json()

	# Parse the response
	message_text = r["text"]

	# Return the text content of the message
	return message_text


"""
Function: 		post_spark_message

Description:	Used to post a message to a given Cisco Spark room.

Arguments:		message - string to send to spark room
				room_id - Cisco Spark room id string
				spark_token - Cisco Spark API user authentication token string

Return:			response - HTTP Request response
"""
def post_spark_message(message, room_id, spark_token):

	# Set API endpoint
	spark_endpoint = "/messages"

	# Set request headers
	spark_headers = {'Authorization': 'Bearer ' + spark_token, 
					'Content-Type': 'application/json'}

	# Set request payload
	spark_payload = {"roomId":room_id, "text":message}

	# Send HTTP request
	r = requests.post(spark_uri+spark_endpoint, data=json.dumps(spark_payload), headers=spark_headers)

	# Return the HTTP response
	return r



"""
Function: 		post_spark_membership

Description:	Add a user to a given Spark room.
				Useful for signing up users to a room when just email is known.

Arguments:		email - email address of user to add into room
				room_id - Cisco Spark room id of which to add user
				spark_token - Cisco Spark API user authentication token string

Return:			membership_id - Spark user membership id string
"""
def post_spark_membership(email, room_id, spark_token):

	# Set API endpoint
	spark_endpoint = "/memberships"

	# Set request headers
	spark_headers = {'Authorization': 'Bearer ' + spark_token, 
					'Content-Type': 'application/json'}

	# Set request payload
	spark_payload = {"roomId":room_id, "personEmail":email}

	# Send HTTP request
	r = requests.post(spark_uri+spark_endpoint, data=json.dumps(spark_payload), headers=spark_headers).json()

	# Parse the response for room id
	membership_id = ""
	try:
		membership_id = r["id"]
	except Exception:
		print(Exception)

	# Return the HTTP response
	return membership_id



"""
Function: 		post_spark_create_room

Description:	Create a new Spark room

Arguments:		title - Title of room displayed to room members
				spark_token - Cisco Spark API user authentication token string

Return:			room_id - Cisco Spark room id string of created room
"""
def post_spark_create_room(title, spark_token):

	# Set API endpoint
	spark_endpoint = "/rooms"

	# Set request headers
	spark_headers = {'Authorization': 'Bearer ' + spark_token, 
					'Content-Type': 'application/json'}

	# Set request payload
	spark_payload = {"title":title}

	# Send HTTP request
	r = requests.post(spark_uri+spark_endpoint, data=json.dumps(spark_payload), headers=spark_headers).json()

	# Parse the response for room id
	room_id = r["id"]

	# Return the HTTP response
	return room_id



"""
Function: 		post_spark_create_webhook

Description:	Create a new webhook to post requests to a given url when an event such as a message posted into a Spark room happens.
				Useful for creating automation based on users input into a Spark room.
				Webhook url should accept and parse HTTP POST requests. 

Arguments:		name - Name of the created webhook
				target_url - URL for webhook to send HTTP requests against when triggered
				webhook_filter - Scope of triggers to cause webhook to send HTTP requests to target_url
				spark_token - Cisco Spark API user authentication token string

Return:			response - HTTP Request response
"""
def post_spark_create_webhook(name, target_url, webhook_filter, spark_token):

	# Set API endpoint
	spark_endpoint = "/webhooks"

	# Set request headers
	spark_headers = {'Authorization': 'Bearer ' + spark_token, 
					'Content-Type': 'application/json'}

	# Set request payload
	spark_payload = {"name":name,"targetUrl":target_url,"resource":"messages","event":"created","filter":webhook_filter}

	# Send HTTP request
	response = requests.post(spark_uri+spark_endpoint, data=json.dumps(spark_payload), headers=spark_headers).json()

	# Return the HTTP response
	return response
