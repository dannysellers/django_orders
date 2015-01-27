var extraElement = "Description: <input type='text' name='description' placeholder='Description'><br/>Quantity: <input type='number' name='quantity' placeholder='Quantity'><br/>Unit cost: <input type='number' name='unit_cost' pattern='[0-9]+([\.|,][0-9]+)?' step='0.01' placeholder='Unit cost'>";
var holdingArea = document.getElementById('extras-holder');

function addElement() {
	console.log('addElement called');
	var newExtra = document.createElement('div');
	newExtra.className = 'extra-row';
	newExtra.innerHTML = extraElement;
	holdingArea.appendChild(newExtra);
}

function removeElement() {
	console.log('removeElement called');
	var childExtras = document.getElementsByClassName('extra-row');
	if (childExtras.length > 0) {
		var lastChild = childExtras[childExtras.length - 1];
		lastChild.remove();
	} else {
		console.log('No more elements to remove!');
		return false;
	}
}