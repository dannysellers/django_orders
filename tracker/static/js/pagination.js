function setSelect(selectId) {
	// Sets the specified select widget to the same as the last query
	// Otherwise, it would reset to the first element in the select on load
	var widgetSelect = document.getElementById(selectId);
	var curLoc = document.location.href;
	// Captures the items param value whether it's proceeded by ? or &
	var itemRegEx = /.*&items=(\d+)|\?items=(\d+)/;
	var itemParam = curLoc.match(itemRegEx)[1];

	if (itemParam) {
		for (var i = 0; i < widgetSelect.length; i++) {
			if (widgetSelect[i].value == itemParam) {
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
	// First, though, we get all the existing GET params and pass them on too

	// Get url params
	var urlParamRegEx = /.*\?(.+)$/;
	var urlParams = document.location.href.match(urlParamRegEx)[1];
	// Split into list of 'key=value'
	urlParams = urlParams.split('&');

	// Make and obj (dict) for easy key matching later
	var urlObj = {};
	for (p in urlParams) {
		var key = urlParams[p].split('=')[0];
		var value = urlParams[p].split('=')[1];
		urlObj[key] = value;
	}

	// Get form params
	var formParams = [];
	var formPagination = document.getElementById(formId);
	for (i = 0; i < formPagination.length; i++) {
		var element = formPagination.elements[i];
		if (element.name == 'page' && !element.value) {
			// If no page number is specified, put in 1
			formParams.push(encodeURIComponent(element.name) + '=1')
		} else if (!element.name && !element.value) {
			// The submit button submits an empty name and value--disregard this
			continue;
		} else {
			// Otherwise, append 'key=value'
			formParams.push(encodeURIComponent(element.name) + '=' + encodeURIComponent(element.value));
		}
	}

	var formObj = {};
	for (p in formParams) {
		var key = formParams[p].split('=')[0];
		var value = formParams[p].split('=')[1];
		formObj[key] = value;
	}

	// formObj has a predetermined length and composition,
	// so we just override the urlObj values from formObj
	for (param in formObj) {
		urlObj[param] = formObj[param];
	}

	var newParams = '';
	for (var property in urlObj) {
		if (urlObj.hasOwnProperty(property)) {
			newParams += property + "=" + urlObj[property] + "&";
		}
	}

	var curLoc = document.location.href.split('?')[0];
	return document.location.href = curLoc + "?" + newParams;
}