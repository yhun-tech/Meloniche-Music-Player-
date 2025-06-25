from feed import Feed

def go_to_feed(parent):
    global feed
    feed = Feed()
    feed.grab_set()
    parent.withdraw()  # Hide the Index window

def close_feed():
    feed.destroy()



