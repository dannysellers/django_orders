var request = new XMLHttpRequest();

function draw(data) {
	var table = document.getElementById("op_history");
	var row = document.getElementById("op_row");
	var output = [];
	for (var index = 0; index < data.length; index++) {
		var item = data[index];
		console.log(item);
		var text = row.innerHTML;
		for (var p in item) {
			if (item.hasOwnProperty(p)) {
				text = text.replace("{phone." + p + "}", item[p])
			}
		}
		output.push(text); //append
	}
	table.innerHTML = "<li>" + output.join("</li><li") + "</li>";
}


function onRequestChange() {
	console.log(request.readyState, request.status);
	if ((request.readyState == 4) && (request.status == 200)) {
		var data = JSON.parse(request.responseText);
		draw(data);
	}
}


function fetch() {
	request.onreadystatechange = onRequestChange;
	request.open("GET", "/manage_items/", true); //ajax url
	request.send();
}

function load() {
	fetch();
}