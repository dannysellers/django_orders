function setSelect(selectId) {
	// Sets the specified select widget to the same as the last query
	// Otherwise, it would reset to the first element in the select on load
	var widgetSelect = document.getElementById(selectId);
	var curLoc = document.location.href;
	var re = /.*items=(\S+).*/;
	var curSelectedItems = curLoc.match(re);
	// ^ Returns a list with the URL and the match
	if (curSelectedItems) {
		for (var i = 0; i < widgetSelect.length; i++) {
			if (widgetSelect[i].value == curSelectedItems[1]) {
				widgetSelect.selectedIndex = i;
			}
		}
	}
}

function submitPaginationForm(formId) {
	// Hijacks the page form submission and manually submits all values.
	// Otherwise, if the user doesn't explicitly change the select widget
	// (i.e. if it's changed in a previous query), the value is not submitted
	// at all in the new request.
	// TODO: This doesn't preserve any existing GET keywords...
	var formPagination = document.getElementById(formId);
	var strQuery = [];
	for (var i = 0; i < formPagination.length; i++) {
		var element = formPagination.elements[i];
		if (element.name == 'page' && !element.value) {
			strQuery.push(encodeURIComponent(element.name) + "=1")
		} else if (!element.name && !element.value) {
			continue;
		} else {
			strQuery.push(encodeURIComponent(element.name) + "=" + encodeURIComponent(element.value));
		}
	}

	strQuery = strQuery.join("&");
	var curLoc = document.location.href.split('?')[0];
	document.location.href = curLoc + "?" + strQuery;
}