function toggle(idToggleDiv, toggleLink) {
	// Function to toggle account info form pane
	var curDiv = document.getElementById(idToggleDiv);
	var objToggle = document.getElementById(toggleLink);

	if (idToggleDiv == 'acctForm') {
		var preEleText = 'Edit Account Info';
		var postEleText = 'Hide Account Info'
	} else if (idToggleDiv == 'toggleDiv') {
		var preEleText = 'Log in';
		var postEleText = 'hide'
	} else if (idToggleDiv == 'shipForm') {
		var preEleText = 'Show Notes';
		var postEleText = 'Hide Notes'
	}

	if (curDiv.style.display == "block") {
		curDiv.style.display = "none";
		objToggle.innerHTML = preEleText;
	} else {
		curDiv.style.display = "block";
		objToggle.innerHTML = postEleText;
	}
}

function checkAll(source) {
	// Check all boxes in the table (of class 'checkbox' to make things easier)
	var checkboxes = document.getElementsByClassName("checkbox");
	for (var i = 0; i < checkboxes.length; i++) {
		checkboxes[i].checked = source.checked;
	}
}

function getParent(_element, strTagName) {
	// Get parent of _element with tag name strTagName
	if (_element == null) return null;
	else if (_element.nodeType == 1 && _element.tagName.toLowerCase() == strTagName.toLowerCase()) // Gecko bug, supposed to be uppercase
		return _element;
	else
		return getParent(_element.parentNode, strTagName);
}

function toggleSection(lnk) {

	var th = lnk.parentNode;
	var table = getParent(th, 'table');
	var len = table.rows.length;
	var tr = getParent(th, 'tr');
	var rowIndex = tr.rowIndex;
	var rowHead = table.rows[rowIndex].cells[1].innerText; // Ship ID

	lnk.innerHTML = (lnk.innerHTML == "+") ? "-" : "+";

	/* ternary operator for:
	if (table.rows[1].style.display != 'none'){
	  vStyle = 'none'
	} else {
	  vStyle = ''
	}; */
	vStyle = (table.rows[rowIndex + 1].style.display == 'none') ? '' : 'none';

	for (var i = rowIndex + 1; i < len; i++) {
		// Changing the child <p> of the tag allows the cell to continue
		// abiding by CSS appearance rules on the table
		if (table.rows[i].cells[1].children[0].innerHTML == rowHead) {
			table.rows[i].style.display = vStyle;
			table.rows[i].cells[1].children[0].style.visibility = "hidden";
		}
	}
}

function initShipTable() {
	var tbl = document.getElementsByClassName('expandable');
	if (tbl.length > 1) {
		alert("More than one table found (unexpected). Using first table.");
	}
	tbl = tbl[0];


}