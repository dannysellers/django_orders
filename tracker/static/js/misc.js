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
