var extraElement = "<label>Description<input type='text' name='description' placeholder='Description'></label><label>Quantity<input type='number' name='quantity' placeholder='Quantity'></label><label>Unit cost<input type='number' name='unit_cost' pattern='[0-9]+([\.|,][0-9]+)?' step='0.01' placeholder='Unit cost'></label>";
var extraCartonSetElement = "<label>Quantity<input type='number' name='quantity' placeholder='Quantity'></label><input id='dim-input' type='number' name='length' step='any' placeholder='Length'> x <input id='dim-input' type='number' name='width' step='any' placeholder='Width'> x <input id='dim-input' type='number' name='height' step='any' placeholder='Height'>";
var holdingArea = document.getElementById('extras-holder');

function addElement() {
    var newExtra = document.createElement('div');

    //console.log('addElement called');
    newExtra.className = 'extra-row';
    newExtra.innerHTML = extraElement;
    holdingArea.appendChild(newExtra);
}

$("input#remove-extra").on('click', function () {
    var childExtras = document.getElementsByClassName('extra-row');

    if (childExtras.length > 0) {
        var lastChild = childExtras[childExtras.length - 1];
        lastChild.remove();
    } else {
        alert('No more elements to remove!');
        return false;
    }
});

$("input#add-extra").on('click', function () {
    var newExtra = document.createElement('div');
    var holdingArea = $("div#extras-holder");

    newExtra.className = 'extra-row';
    newExtra.innerHTML = extraCartonSetElement;
    holdingArea.append(newExtra);
});

  //////////////////////////////
 // Order - Shipment Linking //
//////////////////////////////

$("a.link-shipment").on('click', function () {
    /* Fxn to populate select widget with unmatched shipments
     (Shipments that have no Work Order)
     */
    var self = $(this);

    $.ajax({
        url: "/unmatched_shipments/" + self.prop('id') + "/",
        dataType: "text",
        type: "GET",
        error: function (err) {
            alert("Error: " + err.statusText.toString())
        },
        success: function (data) {
            // Parse data
            var _data = JSON.parse(data).list;
            var btnGroup = self.parent().parent();
            var shipForm = $("form#" + self.prop('id') + ".match-order-form");
            var sibSelect = $("select#" + self.prop('id') + ".unmatched-shipment-select");

            if (!_data.length) {
                alert("This customer does not have any unmatched shipments. Try creating one instead.");
                // Disable the Link button
                self.addClass('disabled');
                return false
            }

            // Hide the initial button group
            btnGroup.hide();

            // Display form
            shipForm.css('display', '');

            // Populate select options
            sibSelect.children().remove();
            for (var i = 0; i < _data.length; i++) sibSelect.append("<option id=" + i + ">" + _data[i] + "</option>");
        }
    })
});


$("a.link-order").on('click', function () {
    /* Fxn to populate select widget with unmatched work orders
     (Work Orders that have no Shipment)
     */
    var self = $(this);
    $.ajax({
        url: '/unmatched_orders/' + self.prop('id') + '/',
        dataType: 'text',
        type: 'GET',
        error: function (err) {
            alert("Error: " + err.statusText.toString())
        },
        success: function (data) {
            // Parse data
            var _data = JSON.parse(data).list;
            var btnGroup = $(self).parent().parent();
            var orderForm = $("form#" + self.prop('id') + ".match-shipment-form");
            var sibSelect = $("select#" + self.prop('id') + ".unmatched-order-select");

            if (!_data.length) {
                alert("This customer does not have any unmatched work orders.\n\nThey will need to submit " +
                "an order before the shipment can be processed.");
                // Disable the Link button
                $(self).addClass('disabled');
                return false
            }

            // Hide the initial button group
            btnGroup.hide();

            // Display form
            orderForm.css('display', '');

            // Populate select options
            sibSelect.children().remove();
            for (var i = 0; i < _data.length; i++) sibSelect.append("<option>" + _data[i] + "</option>");
        }
    })
});

$(".delete-order").on('click', function () {
    return confirm("Would you really like to delete Work Order " + this.id + "?");
});