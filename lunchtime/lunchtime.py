# -*- coding: utf-8 -*-
import appindicator
import pynotify
import gtk
import getpass
import json
import requests
import datetime

previous_suggestion = ""

a = appindicator.Indicator('wallch_indicator', 'user-invisible-panel', appindicator.CATEGORY_APPLICATION_STATUS)
a.set_status( appindicator.STATUS_ACTIVE )
m = gtk.Menu()

pynotify.init('user-idle-panel')

suggestion_no_text = "Nobody has suggested lunch yet"

suggestion_item = gtk.MenuItem(suggestion_no_text)
suggestion_separator = gtk.SeparatorMenuItem()
check_now_item = gtk.MenuItem( 'Check now' )
ci_5 = gtk.MenuItem( 'Suggest lunch in 5 min' )
ci_10 = gtk.MenuItem( 'Suggest lunch in 10 min' )
ci_15 = gtk.MenuItem( 'Suggest lunch in 15 min' )
quit_separator = gtk.SeparatorMenuItem()
qi = gtk.MenuItem( 'Exit' )

m.append(suggestion_item)
m.append(suggestion_separator)
m.append(check_now_item)
m.append(ci_5)
m.append(ci_10)
m.append(ci_15)
m.append(quit_separator)
m.append(qi)

a.set_menu(m)

suggestion_item.show()
suggestion_separator.show()
check_now_item.show()
ci_5.show()
ci_10.show()
ci_15.show()
quit_separator.show()
qi.show()

suggestion_item.set_sensitive(False)

def quit_app(item):
    gtk.main_quit()

def check_status(*args):
    global previous_suggestion
    url = "http://comp-phys.net/lunch"
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    if len(data) < 1:
        a.set_icon("user-invisible-panel")
        suggestion_item.set_label(suggestion_no_text)
    else:        
        current_suggestion = data[0]["username"] + data[0]["time"]
        suggestion_text = data[0]["username"] + " suggests lunch in " + data[0]["eta"] + " min"
        suggestion_item.set_label(suggestion_text)
        if int(data[0]["eta"]) <= 5:
            a.set_icon("user-away-panel")    
        else:
            a.set_icon("user-idle-panel")
        if current_suggestion != previous_suggestion:
            n = pynotify.Notification(suggestion_text)
            n.show()
            previous_suggestion = current_suggestion
    return True

def propose_lunch(delay):
    url = "http://comp-phys.net/lunch?suggest=" + str(delay) + "&username=" + getpass.getuser()
    requests.get(url=url)
    check_status()

def propose_lunch_5(item):
    propose_lunch(5)

def propose_lunch_10(item):
    propose_lunch(10)

def propose_lunch_15(item):
    propose_lunch(15)
    
ci_5.connect('activate', propose_lunch_5)
ci_10.connect('activate', propose_lunch_10)
ci_15.connect('activate', propose_lunch_15)
check_now_item.connect('activate', check_status)
qi.connect('activate', quit_app)

gtk.timeout_add(1000*60, check_status) # call every min

def main():
    check_status()
    gtk.main()
    
if __name__ == "__main__":
    main()