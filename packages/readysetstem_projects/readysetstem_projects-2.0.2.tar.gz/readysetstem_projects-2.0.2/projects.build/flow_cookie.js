//
// Cookie functions from w3schools.com
//
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}

function getFlowName() {
    return getCookie("flow_name");
}

function setFlowName() {
    setCookie("flow_name", flow.value, 999);
}

function getFlowIndex() {
    flow_name = getFlowName();
    if (flow_name.length > 0) {
        return pg_flows[flow_name];
    } else {
        for (var f in pg_flows) {
            return pg_flows[f];
        }
    }
}
