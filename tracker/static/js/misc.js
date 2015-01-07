function toggle(idToggleDiv, toggleLink) {
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
	var checkboxes = document.getElementsByClassName("checkbox");
	for (var i = 0; i < checkboxes.length; i++) {
		checkboxes[i].checked = source.checked;
	}
}