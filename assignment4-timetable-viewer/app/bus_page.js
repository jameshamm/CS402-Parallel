function refreshTable() {
    document.getElementById("BusTimes").innerHTML = "";
    getBusData(writeToTable);
}

function getBusData(func) {
    var request = new XMLHttpRequest();
    var link = "https://data.dublinked.ie/cgi-bin/rtpi/realtimebusinformation?stopid=135001&format=xml";
    request.open("GET", link, false);
    request.send();
    // callback
    func(request.responseXML);
}

function writeToTable(data) {
    var results = data.getElementsByTagName("results")[0].childNodes;
    var headers = {
        "duetime": "Due Time",  // In minutes
        "route": "Route Number",
        "destination": "Destination",
        "origin": "Origin",
        "operator": "Operator"
    };
    var dom = generateColumns(headers);

    for(var i = 0; i < results.length; i++) {
        var temp = "<tr>";
        for(header in headers) {
            var x = "<td>"
            x += results[i].getElementsByTagName(header)[0].childNodes[0].nodeValue;
            x += "</td>";
            temp += x;
        }
        temp += "</tr>";
        dom += temp;
    }

    document.getElementById("BusTimes").innerHTML = dom;
}

function generateColumns(headers) {
    var dom = "<tr>";
    for(key in headers) {
        dom += "<th>" + headers[key] + "</th>";
    }
    dom += "</tr>";
    return dom;
}
