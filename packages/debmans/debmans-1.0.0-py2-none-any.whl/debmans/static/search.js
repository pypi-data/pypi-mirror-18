goto = function(btn, prefix){
    btn.disabled=true;
    var page = document.getElementById('pageinput').value;
    var suite = document.getElementById('suiteinput').value;
    var parts = page.split('.');
    var manpage;
    var section = 1; // sane default
    manpage = parts[0];
    if (parts.length > 1) {
        section = parts[1];
    }
    else {
        parts = page.split(/[()]/); // guess it's man(1)
        manpage = parts[0];
        if (parts.length > 1) {
            section = parts[1];
        }
        else {
            console.warn('cannot parse section, assuming section ' + section);
        }
    }
    // what a shame, javascript, no fkn printf??
    path = prefix + suite + '/man/man' + section + '/' + manpage + '.' + section + '.html';
    var request = new XMLHttpRequest();
    console.log('opening new HTTP request to page ' + path)
    request.open('GET', path, true);
    request.onreadystatechange = function(){
        if (request.readyState === 4){
            if (request.status === 404) {  
                window.location = prefix + '404.html?page=' + page
                btn.disabled=false;
                return false;
            }
            else {
                console.log("redirecting to "+ path)
                window.location = path;
                btn.disabled=false;
                return false;
            }
        }
    };
    request.send();
    btn.disabled=false;
    return false;
}
