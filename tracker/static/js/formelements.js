var extraElement = "<label>Description<input type='text' name='description' placeholder='Description'></label><label>Quantity<input type='number' name='quantity' placeholder='Quantity'></label><label>Unit cost<input type='number' name='unit_cost' pattern='[0-9]+([\.|,][0-9]+)?' step='0.01' placeholder='Unit cost'></label>";
var extraCartonSetElement = "<label>Quantity<input type='number' name='quantity' placeholder='Quantity'></label><input id='dim-input' type='number' name='length' step='any' placeholder='Length'> x <input id='dim-input' type='number' name='width' step='any' placeholder='Width'> x <input id='dim-input' type='number' name='height' step='any' placeholder='Height'>";
var holdingArea = document.getElementById('extras-holder');

function addElement() {
    console.log('addElement called');
    var newExtra = document.createElement('div');
    newExtra.className = 'extra-row';
    newExtra.innerHTML = extraElement;
    holdingArea.appendChild(newExtra);
}

function removeElement() {
    //console.log('removeElement called');
    var childExtras = document.getElementsByClassName('extra-row');
    if (childExtras.length > 0) {
        var lastChild = childExtras[childExtras.length - 1];
        lastChild.remove();
    } else {
        alert('No more elements to remove!');
        return false;
    }
}

function addCartonSetElement() {
    //console.log('addCartonSetElement called');
    var newExtra = document.createElement('div');
    newExtra.className = 'extra-row';
    newExtra.innerHTML = extraCartonSetElement;
    holdingArea.appendChild(newExtra);
}