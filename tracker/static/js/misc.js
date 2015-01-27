function togglePane(idToggleDiv, toggleLink) {
	// Function to toggle account info form pane
	var curDiv = document.getElementById(idToggleDiv);
	var objToggle = document.getElementById(toggleLink);

	if (idToggleDiv == 'acctForm') {
		var preEleText = 'Edit Account Info';
		var postEleText = 'Hide Account Info'
	} else if (idToggleDiv == 'toggleDiv') {
		preEleText = 'Log in';
		postEleText = 'hide'
	} else if (idToggleDiv == 'shipForm') {
		preEleText = 'Show Notes';
		postEleText = 'Hide Notes'
	}

	var eleText = (curDiv.style.display == 'block') ? preEleText : postEleText;
	var styleDisplay = (curDiv.style.display == 'block') ? 'none' : 'block';

	objToggle.innerHTML = eleText;
	curDiv.style.display = styleDisplay;
}

function getParent(_element, strTagName) {
	// From http://js-code.blogspot.com/p/table-tr-td-th-border-stylesolid-border.html
	// Get parent of _element with tag name strTagName
	if (_element == null) return null;
	else if (_element.nodeType == 1 && _element.tagName.toLowerCase() == strTagName.toLowerCase()) // Gecko bug, supposed to be uppercase
		return _element;
	else
		return getParent(_element.parentNode, strTagName);
}

function checkAll(source) {
	// Check all boxes in the table (of class 'checkbox')
	var table = getParent(source.parentNode, 'table');
	var checkboxes = table.getElementsByClassName('checkbox');
	for (var i = 0; i < checkboxes.length; i++) {
		checkboxes[i].checked = source.checked;
	}
}

function toggleSection(lnk) {
	// Toggles sections of a table, as for folding of shipment <tr>s
	var th = lnk.parentNode;
	var table = getParent(th, 'table');
	var len = table.rows.length;
	var tr = getParent(th, 'tr');
	var rowIndex = tr.rowIndex;
	var rowHead = table.rows[rowIndex].cells[1].children[0].innerText; // Ship ID

	lnk.innerHTML = (lnk.innerHTML == "+") ? "-" : "+";

	/* ternary operator for:
	if (table.rows[1].style.display == 'none'){
	  vStyle = 'none'
	} else {
	  vStyle = ''
	}; */
	var vStyle = (table.rows[rowIndex + 1].style.display == 'none') ? '' : 'none';

	for (var i = rowIndex + 1; i < len; i++) {
		// Changing the child <p> of the tag allows the cell to continue
		// abiding by CSS appearance rules on the table
		if (table.rows[i].cells[1].children[0].innerHTML == rowHead) {
			table.rows[i].style.display = vStyle;
			table.rows[i].cells[1].children[0].style.visibility = "hidden";
		}
	}
}

function simpleTableToggle(lnk) {
	var th = lnk.parentNode;
	var table = getParent(th, 'table');
	var len = table.rows.length;
	var tr = getParent(th, 'tr');
	var rowIndex = tr.rowIndex;

	lnk.innerHTML = (lnk.innerHTML == "+") ? "-" : "+";

	var vStyle = (table.rows[rowIndex + 1].style.display == 'none') ? '' : 'none';

	for (var i = rowIndex + 1; i < len; i++) {
		table.rows[i].style.display = vStyle;
	}
}

function verifyAllChecked(tableId, formId) {
	// If all or none of the checkboxes are checked, the form submits. Else, confirm
	var table = document.getElementsByClassName(tableId)[0];
	var checkboxes = table.getElementsByClassName('checkbox');
	var headChecked = checkboxes[0].checked; // Value of checkbox in head row
	var complete = true;
	var numChecked = 0;  // If all the boxes are checked but not the header, it's fine
	var sForm = document.forms[formId];

	// If the top box is checked and any other is different, the set is incomplete
	for (var i = 1; i < checkboxes.length; i++) {
		if (checkboxes[i].checked) {
			numChecked += 1;
		}
		if (checkboxes[i].checked != headChecked) {
			complete = false
		}
	}
	if (complete == false && numChecked != checkboxes.length - 1) {
		if (confirm("Not all items in this shipment were selected! Continue? Shipment status will not change (only item statuses).\nTo change shipment statuses, select all their component items.")) {
			sForm.submit();
		} else {
			return false
		}
	} else {
		sForm.submit();
	}
}

function disableElements(eleForm) {
	var sForm = document.getElementById(eleForm);
	// TODO: Check whether it's disable-able?
	for (var i = 0; i < sForm.childElementCount; i++) {
		var c = sForm.children[i];
		for (var j = 0; j < c.childElementCount; j++) {
			if (c.children[j].name != 'csrfmiddlewaretoken') {
				c.children[j].disabled = true;
			}
		}
	}
}

function confirmAcctRemove(itemsInStorage) {
	// itemsInStorage should be passed as {{ customer.inventory_set.all|stored_count }}
	if (itemsInStorage > 0) {
		alert("This customer still has items in inventory! Please process those first before proceeding.")
	} else if (itemsInStorage == 0) {
		document.location.href = "/accounts?remove={{ customer.acct }}";
	} else {
		alert("No itemsInStorage passed to confirmAcctRemove(). Check the onclick of the Remove Account link.")
	}
}