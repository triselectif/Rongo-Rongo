/*
 * appsServer.cpp
 *
 *  Created on: Sep 19, 2011
 *      Author: dolivari
 */

#include "appsServer.h"

using namespace std;

AppsServer::AppsServer(DBus::Connection &connection) :
		DBus::ObjectAdaptor(connection, "/Org/RongoRongo/Apps")
{

}

AppsServer::~AppsServer()
{
}

map<string, ::DBus::Struct< string, string, string> > AppsServer::getList()
{
	map<string, ::DBus::Struct< string, string, string> >  aMap;

	for (uint aCounter = 0; aCounter < 16; aCounter++)
	{
		::DBus::Struct< string, string, string> aStruct;
		stringstream aTempOut;
		aTempOut << aCounter;
		string aStringCounter = aTempOut.str();
		aStruct._1 = "Application Test ";
		aStruct._1 += aStringCounter;
		aStruct._2 = "http://localhost/apps/default.html";
		aStruct._3 = "http://localhost/img/default.png";

		aMap["testapp"+aStringCounter] = aStruct;
	}
	return aMap;
}

void AppsServer::open(const std::string& id)
{

}

void AppsServer::close(const std::string& id)
{

}
