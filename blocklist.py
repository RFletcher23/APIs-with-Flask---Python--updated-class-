# This file contins the blocklist of the JWT tokens. 
# It will be imported by app and the logout resource so that tokens can be added to the blocklist when a user logs out.

BLOCKLIST = set() #This is a set because we don't want duplicates