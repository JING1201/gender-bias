#! /usr/bin/python

print "Content-type: text/html\n\n"
print "<html><h3>Echo!</h3><p>"


import cgi

form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")
print message 

print "</p></html>"
