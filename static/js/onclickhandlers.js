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
                .then(function () {
                    //debugger;
                    const item = e.target.parentElement;
                    item.remove();
                })
                .catch(function () {
                    document.getElementById('error').className = '';
                })
            }
        }
    }
}

