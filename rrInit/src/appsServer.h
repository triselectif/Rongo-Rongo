/*
 * appsServer.h
 *
 *  Created on: Sep 19, 2011
 *      Author: dolivari
 */

#ifndef APPSSERVER_H_
#define APPSSERVER_H_

#include <dbus-c++/dbus.h>
#include "rrinit_adaptor.h"

class AppsServer: public org::rongorongo::apps_adaptor,
		public DBus::IntrospectableAdaptor,
		public DBus::ObjectAdaptor

{
public:
	AppsServer(DBus::Connection &connection);
	virtual ~AppsServer();

	virtual std::map< std::string, ::DBus::Struct< std::string, std::string, std::string > > getList();
    virtual void open(const std::string& id);
    virtual void close(const std::string& id);

};

#endif /* APPSSERVER_H_ */
