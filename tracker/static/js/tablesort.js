// from http://jsfiddle.net/zscQy/

function sortTable(table, col, reverse) {
	var tb = table.tBodies[0], // use `<tbody>` to ignore `<thead>` and `<tfoot>` rows
		tr = Array.prototype.slice.call(tb.rows, 0), // put rows into array
		i;
	reverse = -((+reverse) || -1);
	tr = tr.sort(function (a, b) { // sort rows
		return reverse
			* (a.cells[col].textContent.trim() // using `.textContent.trim()` for test
				.localeCompare(b.cells[col].textContent.trim(), undefined, {numeric: true})
			);
	});
	for (i = 0; i < tr.length; ++i) tb.appendChild(tr[i]); // append each row in order
}

function makeSortable(table) {
	var th = table.tHead, i;
	th && (th = th.rows[0]) && (th = th.children);
    if (th) i = th.length;
    else return; // if no `<thead>` then do nothing
    while (--i >= 0) (function (i) {
        var dir = 1;
		th[i].addEventListener('click', function () {sortTable(table, i, (dir = 1 - dir))});
	}(i));
}

function makeAllSortable(parent) {
	parent = parent || document.body;
	var t = parent.getElementsByTagName('table'), i = t.length;
	while (--i >= 0) {
		if (t[i].classList[0] != 'not-sortable') {
			makeSortable(t[i]);
		} else {
			console.log("Table of " + t[i].rows.length + " rows ignored as not sortable.");
		}
	}
}

window.onload = function () {
	makeAllSortable();
};