# Python snippet for clearing the output of Convert-ToJson from encoding rudiments
# NOTE: that's a dumb way, better open the file with uncoding utf-16-le and later resave with normal one

users = users.replace("яю", "").replace("\x00","")
