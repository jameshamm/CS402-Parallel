function refreshTable() {
    getBusData(writeToTable);
}

function getBusData(func) {
    var request = new XMLHttpRequest();
    var stop = 103381;
    var link = "https://data.dublinked.ie/cgi-bin/rtpi/realtimebusinformation?stopid=" + stop + "&format=xml";
    console.log(link);
    request.open("GET", link, false);
    request.send();
    // callback
    func(request.responseXML);
}

function writeToTable(data) {
    console.log(data.getElementsByTagName("results"));
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
        temp += "<td>" + (i+1) + "</td>"; //lolololol
        for(header in headers) {
            var x = "<td>"
            try{
                x += results[i].getElementsByTagName(header)[0].childNodes[0].nodeValue;
            }
            catch(err){

            }
            x += "</td>";
            temp += x;
        }
        temp += "</tr>";
        dom += temp;
    }

    document.getElementById("BusTimes").innerHTML = dom;
    document.getElementById("LastTime").innerHTML = "Data retrieved at " + data.getElementsByTagName("timestamp")[0].innerHTML;

}

function generateColumns(headers) {
    var dom = "<tr><th>#</th>";
    for(key in headers) {
        dom += "<th>" + headers[key] + "</th>";
    }
    dom += "</tr>";
    return dom;
}
