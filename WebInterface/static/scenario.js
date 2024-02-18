const timestamp = document.getElementById("timestamp");

/* Code from: https://www.w3schools.com/js/tryit.asp?filename=tryjs_timing_clock */
function startTime() {
    const today = new Date();
    let h = today.getHours();
    let m = today.getMinutes();
    let s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    timestamp.innerHTML = h + ":" + m + ":" + s;
    setTimeout(startTime, 1000);
}

function checkTime(i) {
    if (i < 10) { i = "0" + i };  // add zero in front of numbers < 10
    return i;
}

startTime();

const eventSource = new EventSource('/stream');
const dataContainer = document.getElementById('data-container');

var map = L.map('map').setView([37.766436, -122.441698], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/satellite-v9',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiZmx1ZmZpZ3BvdGF0aXMiLCJhIjoiY2xzcjFyZWd6MTZ2ejJscDdrb3duZWJnbCJ9.43hF6_pTXT0XS18c7BnFPQ' // Replace this with your Mapbox access token
}).addTo(map);

var marker1 = new L.Marker([37.785367, -122.406943]);
marker1.addTo(map)

var marker2 = new L.Marker([37.790927, -122.477368]);
marker2.addTo(map)

var marker3 = new L.Marker([37.788459, -122.387994]);
marker3.addTo(map)

eventSource.onmessage = function (event) {
    const newData = event.data;
    const result = newData.split(",")

    lat = parseFloat(result[1])
    long = parseFloat(result[2])

    if (result[0] == "ER1") {
        marker1.setLatLng([lat, long]).update();
    }
    if (result[0] == "ER2") {
        marker2.setLatLng([lat, long]).update();
    }
    if (result[0] == "ER3") {
        marker3.setLatLng([lat, long]).update();
    }

};