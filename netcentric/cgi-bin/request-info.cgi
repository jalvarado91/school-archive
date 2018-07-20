#!/usr/bin/python

import sys
import os

sys.stderr = sys.stdout

environ =  os.environ

accept_header 	= environ["HTTP_ACCEPT"]
accept_language = environ["HTTP_ACCEPT_LANGUAGE"]
user_agent 	= environ["HTTP_USER_AGENT"]
request_method	= environ["REQUEST_METHOD"]
if environ["QUERY_STRING"] == "":
	query_string = "Query string is empty"
else:
	query_string = environ["QUERY_STRING"]

html = """\
<html>
<head>
	<title>Request Stats</title>
</head>
<body>
	<h2>Juan Alvarado</h2>
	<h5>jalva327</h5>

	<hr/>

	<p>Accept: {0}</p>
	<p>Accept-Language: {1}</p>
	<p>Query-String: {2}</p>
	<p>User-Agent: {3}</p>
	<p>Request-Method: {4}</p>
</body>
</html>
""".format(
	accept_header,
	accept_language,
	query_string,
	user_agent,
	request_method)

print "Content-Type: text/html\n"
print html