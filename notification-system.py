
def make_notification(type,area): # Type of notification and area in which it involves (area can be none)
    if type.lower() == "crowd":
        return("Warning - ",area," may be busy due to traffic")
    elif type.lower() == "reminder":
        return("Reminder - your gate closes soon, please make your way to gate", area)
    

# This is obviously not finished, may change the layout but didn't want to leave an empty file