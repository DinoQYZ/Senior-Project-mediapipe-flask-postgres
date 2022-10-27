function determineVid() {
    var value = document.getElementById("actionChoose").selectedIndex;
    var val;

    if (value=="0"){
        val = "biceps_curl";
    }

    var src = "{{ url_for('" + val + "') }}";

    var img = document.createElement("img");
    img.src = src;
    img.id = "vidImg";

    document.getElementById("camara_display").appendChild(img);
}

function closeVid() {
    let value = document.getElementById("camara_display");
    value.removeChild(value.lastElementChild);
}

function showCloseBtn() {
    document.getElementById('closeBtn').style.display = "block";
    document.getElementById('startBtn').style.display = "none";
}

function showStartBtn() {
    document.getElementById('startBtn').style.display = "block";
    document.getElementById('closeBtn').style.display = "none";
}



