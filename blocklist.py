""" 
    This file just contains the blocklist  of the JWT tokens. It will be  imported by
    app and the logout resource so that can be added to the blocklist when the user's
    logout's.
"""

# Replace For a Redis Data Base
BLOCKLIST = set()
