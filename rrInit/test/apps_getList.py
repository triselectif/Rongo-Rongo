#! /usr/bin/env python

import dbus

if __name__ == '__main__':
    aDbus = dbus.SessionBus()
    anAppsObj = aDbus.get_object("org.rongorongo.rrinit","/Org/RongoRongo/Apps")
    anI2Apps = dbus.Interface(anAppsObj, dbus_interface="org.rongorongo.apps")
    anAppsList = anI2Apps.getList()
    for id in anAppsList:
        print "Title : " + anAppsList[id][0]
        print "id :"  + id
        print "image : " + anAppsList[id][2]
        print "webpage : " + anAppsList[id][1]
        print
        

