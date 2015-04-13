// TODO: Load sample graphs on pageload
var elemCanvas = document.createElement('canvas');

function getData() {
    var startDate = $('#start-date');
    var endDate = $('#end-date');
    var queryList = [$("#model-select").val().toLowerCase(), $("#model-attr-select").val(), $("#op-select").val().toLowerCase()];
    var kwQuery = queryList.join(",");
    var kwSummation = $('#sum-select').find(':selected').text().toLowerCase();
    var params = {
        start: startDate.val(),
        finish: endDate.val(),
        query: kwQuery,
        summation: kwSummation
    };
    $.ajax({
        url: "/query_ajax?" + jQuery.param(params),
        dataType: "text",
        type: "GET",
        error: function (err) {
            alert("Error: " + err.statusText.toString())
        },
        success: function (data) {
            var _data = JSON.parse(data)[0];
            var chartArgs = JSON.parse(data)[1];
            drawGraph(_data, chartArgs, "custom-chart");
            $("#json-response").html(JSON.stringify(_data['query'], null, 4))
                .show();
        }
    });
}

function drawGraph(data, options, graph) {
    var ctx = document.getElementById(graph).getContext("2d");
    if (typeof(lineChart) != 'undefined') {
        // Avoid overlapping charts
        lineChart.destroy();
    }
    lineChart = new Chart(ctx).Line(data, options);
}

$("#model-select").change(function () {
    $.ajax({
        url: "/form_ajax/" + $("#model-select").val(),
        dataType: "text",
        type: "GET",
        error: function (err) {
            alert("Error: " + err.statusText.toString())
        },
        success: function (data) {
            var attrs = JSON.parse(data).attr_list;
            var modelSelect = $("#model-attr-select");
            modelSelect.children().remove();
            for (var i = 0; i < attrs.length; i++) modelSelect.append("<option id=" + i + ">" + attrs[i] + "</option>");
        }
    })
});

$("#op-select").change(function () {
    if ($("#op-select").val().toLowerCase() == 'count') {
        $("#model-attr-select").attr('disabled', true);
    } else {
        $("#model-attr-select").attr('disabled', false);
    }
});

var oldEvt = window.onload;
window.onload = function () {
    if (oldEvt) oldEvt();
    if (!elemCanvas.getContext) {
        // Chart.js relies on <canvas> support
        document.write("HTML5 Canvas not supported by your browser!")
    }
    $('.datepicker').pikaday({format: 'YYYY-MM-DD'});
};