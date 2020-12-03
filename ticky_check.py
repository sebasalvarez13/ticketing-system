#!/usr/bin/env python3

import re
import sys
import csv

error_list = []
errorname_list = []
userdata_list = [] #will be a list of per_user dictionaries
username_list = [] #a list just for usernames

with open(sys.argv[1], "r") as logfile:
    events = logfile.readlines() #creates a list will all lines of file, ex:[line1, line2, etc]
    for error in events:
        pattern = r"ticky: ERROR (\w.*) \("
        result = re.search(pattern, error)
        if result and result[1] not in errorname_list:
            errorname_list.append(result[1])

    for error_name in errorname_list:
        error = {"Error": "", "Count": 0}
        error["Error"] = error_name
        for line in events:
            if re.search(r"ERROR " + error_name + " \(", line):
                error["Count"] = error.get("Count", 0) + 1 #error counts are appended to error dictionary
        error_list.append(error)
    #sorts the error list by the counts of each error, from most to less ocurring
    error_sorted = sorted(error_list, key = lambda x: x["Count"], reverse = True)

#-----------username, INFO , ERROR code---------#
    for user in events:
        result = re.search(r"\((\w.+)\)", user) #takes the username as catching group
        if result and result[1] not in username_list:
            username_list.append(result[1])
            username_list.sort()

    for name in username_list:
        per_user = {"Username":"", "INFO":0, "ERROR":0}
        per_user["Username"] = name
        for line in events:
            if re.search(r"INFO \w.* \(" + name + "\)", line):
                per_user["INFO"] = per_user.get("INFO", 0) + 1
            elif re.search(r"ERROR \w.* \(" + name + "\)", line):
                per_user["ERROR"] = per_user.get("ERROR", 0) + 1

        userdata_list.append(per_user)

#----------generate error_message.csv-----------#
keys = ["Error", "Count"]
with open("error_message.csv", "w") as error_message_report:
    writer = csv.DictWriter(error_message_report, fieldnames = keys)
    writer.writeheader()
    writer.writerows(error_sorted)

#----------generate user_statistics.csv-----#
keys = ["Username", "INFO", "ERROR"]
with open("user_statistics.csv", "w") as user_statistics_report:
    writer = csv.DictWriter(user_statistics_report, fieldnames = keys)
    writer.writeheader()
    writer.writerows(userdata_list)
