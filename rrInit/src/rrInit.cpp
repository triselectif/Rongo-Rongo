/*
 * rrInit.cpp
 *
 *  Created on: Sep 19, 2011
 *      Author: dolivari
 */

#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <stdio.h>
#include <limits.h>
#include "appsServer.h"
DBus::BusDispatcher dispatcher;

void niam(int sig)
{
	dispatcher.leave();
}

int main()
{
	signal(SIGTERM, niam);
	signal(SIGINT, niam);

	DBus::default_dispatcher = &dispatcher;

	DBus::Connection conn = DBus::Connection::SessionBus();
	conn.request_name("org.rongorongo.rrinit");

	AppsServer server(conn);

	dispatcher.enter();

	return 0;
}
