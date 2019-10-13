//
// Delete / Update buttons handlers
//
// example of arguments for updates are: 
//
//  { selector: '.btnUpdate', method: 'PUT', collName: 'artists'}
//  { selector: '.btnUpdate', method: 'PUT', collName: 'venues'}
//  { selector: '.btnUpdate', method: 'PUT', collName: 'shows'}
//
// example of arguments for deletes are: 
//
//  { selector: '.btnDelete', method: 'DELETE', collName: 'artists'}
//  { selector: '.btnDelete', method: 'DELETE', collName: 'venues'}
//  { selector: '.btnDelete', method: 'DELETE', collName: 'shows'}
//
function addOnClickHandler(args) {
    //
    const _selector = args["selector"];
    const _method = args["method"];
    const _collName = args["collName"];
    //
    const _buttons = document.querySelectorAll(_selector);
    for (let i = 0; i < _buttons.length; i++) {
        const _button = _buttons[i];
        _button.onclick = function (e) {
            console.log('event', e);
            //debugger;
            let r = true;
            if (_method === "DELETE") {
                r = confirm("Delete item?");
            }
            if (r) {
                const _id = e.target.dataset['id'];
                fetch('/' + _collName + '/' + _id, {
                    method: _method
                })
                    .then(function(response) {
                        //debugger;
                        if (response.status === 200 ||
                            response.status === 521 || 
                            response.status === 522 ) {
                            return response.json();
                        }
                    })
                    .then(function(data)  {
                        //debugger;
                        if (data.type === 'error') {
                            alert(data.message);
                            console.log(data.type, data.message);
                        } else {
                            // On successful delete reload current page.
                            // 
                            // Ideally the way to go would be to remove page 
                            // elements in javascript similar to 
                            //  const item = e.target.parentElement;
                            //  item.remove();
                            // but it will involve more coding and testing from different 
                            // view for this  generic click handler. 
                            // Also, the elements will not be properly ligned 
                            // up / sorted if removed from within a page by JS calls.
                            location.reload();
                        }
                    })
                    .catch(function(err) {
                        //debugger;
                    console.log(err);
                });
            }
        }
    }
}

