var req;

// Sends a new request to update 
function sendRequest() {
    
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }

    req.onreadystatechange = handleResponse;
    req.open("GET", "/blog/get-list", true);
    req.send(); 

    
    
}

// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponse() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }

    
    var list = document.getElementById("bl-list-unaut");
    if (list.hasChildNodes()) {
        
        
        for (var i = list.childNodes.length-1;i > 1 ; i--)
        {
            list.removeChild(list.childNodes[i]);

        }


    

    // Parses the XML response to get a list of DOM nodes representing items
    var xmlData = req.responseXML;
    var items = xmlData.getElementsByTagName("blogger");

    
    for (var i = 0; i < items.length; ++i) {
        
        
        var email = items[i].getElementsByTagName("email")[0].textContent

        var name = items[i].getElementsByTagName("name")[0].textContent
        
        var newItem = document.createElement("li");
        newItem.innerHTML = "<a href=\"/blog/watch?id=" + email + "\">"+name+"</a>"; 

        
        list.appendChild(newItem);
    }
}

else {  list = document.getElementById("bl-list-aut");

            if (list.hasChildNodes()) {
        
        for (var i = list.childNodes.length-1;i > 3 ; i--)
        {
            list.removeChild(list.childNodes[i]);

        }


    

    // Parses the XML response to get a list of DOM nodes representing items
    var xmlData = req.responseXML;
    var items = xmlData.getElementsByTagName("blogger");

    // Adds each new blogger to the list
    for (var i = 0; i < items.length; ++i) {
        
        
        var email = items[i].getElementsByTagName("email")[0].textContent

        var name = items[i].getElementsByTagName("name")[0].textContent
        
        var newItem = document.createElement("li");
        newItem.innerHTML = "<a href=\"/blog/follow?id=" + email + "\">"+name+"</a>"; 

        
        list.appendChild(newItem);
    }
}



    }
}

// causes the sendRequest function to run every 5 seconds
window.setInterval(sendRequest, 5000);
