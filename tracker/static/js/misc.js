$("a#acctFormToggle").on('click', function() {
    // Toggle account info form pane
    var curDiv = $("#acctForm");
    var self = $(this);

    var showText = 'Edit Account Info';
    var hideText = 'Hide Account Info';

    var eleText = (curDiv.css('display') === 'block') ? showText : hideText;
    var styleDisplay = (curDiv.css('display') === 'block') ? 'none' : 'block';

    self.html(eleText);
    curDiv.css('display', styleDisplay);
});

function getParent(_element, strTagName) {
    // From http://js-code.blogspot.com/p/table-tr-td-th-border-stylesolid-border.html
    // Get parent of _element with tag name strTagName
    if (_element == null) return null;
    else if (_element.nodeType == 1 && _element.tagName.toLowerCase() == strTagName.toLowerCase()) // Gecko bug, supposed to be uppercase
        return _element;
    else
        return getParent(_element.parentNode, strTagName);
}

$('th > input.checkbox').on('click', function () {
    // Check all boxes in the table (of class 'checkbox')
    var table = getParent(this.parentNode, 'table');
    var checkboxes = table.getElementsByClassName('checkbox');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = this.checked;
    }
});

$('td.ship-toggle').on('click', function () {
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
     vStyle = ''
     } else {
     vStyle = 'none'
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
});

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
    // Disable elements of eleForm (used for account and shipment info forms).
    // The div 'eleForm' must be inside the <form> tags
    var sForm = document.getElementById(eleForm);
    for (var i = 0; i < sForm.childElementCount; i++) {
        var c = sForm.children[i];
        for (var j = 0; j < c.childElementCount; j++) {
            if (c.children[j].name != 'csrfmiddlewaretoken') {
                c.children[j].disabled = true;
            }
        }
    }
}

$('a.remove-link').on('click', function () {
    // this.id should be {{ customer.inventory.all|stored_count }}
    if (this.id > 0) {
        alert("This customer still has items in inventory! Please process those first before proceeding.")
    } else {
        // Allow the browser to navigate normally
        return true;
    }
});