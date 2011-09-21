/**
 * Moving a window test software
 * compile with : g++ -o xdo_test -lxdo xdo_test.cpp
 * needs the package : libxdo-dev
 * tested with the kivy demo 'pictures'
 *
 */

#include <iostream>

using namespace std;

extern "C" {
#include "xdo.h"
#include <stdlib.h>
}

int main() {
	xdo_t * aXdo = xdo_new("");
	xdo_search_t aSearch;
	aSearch.title = "test";
	aSearch.winname = "Pictures";
	aSearch.searchmask = SEARCH_NAME;
	aSearch.require = xdo_search::SEARCH_ANY;

	Window **aWindowList=(Window**)calloc(8,sizeof(Window));
	int aWinCount = 0;
	xdo_window_search(aXdo, &aSearch, aWindowList, &aWinCount);
	if (0 < aWinCount) {
		cout << "'Pictures Window id : " << *aWindowList[0] << endl;
		xdo_window_activate(aXdo, *aWindowList[0]);
		usleep(500000);
		for (int x = 0; x < 1920; x+=2) {
			int y=0;
			xdo_window_move(aXdo, *aWindowList[0], x, y);
			int win_x, win_y;
			xdo_get_window_location(aXdo, *aWindowList[0], &win_x, &win_y,
					NULL);
			/* Permit imprecision to account for window borders and titlebar */
			while (abs(x - win_x) > 10
					&& abs(y - win_y) > 50) {
				xdo_get_window_location(aXdo, *aWindowList[0],
						&win_x, &win_y, NULL);
				usleep(10000);
			}
		}

	} else {
		cerr << "no 'Pictures' window found !!" << endl;
		return 1;
	}
	xdo_free(aXdo);
	free(aWindowList);
	return 0;
}
