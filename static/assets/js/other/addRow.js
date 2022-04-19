function addRow(id) {
    var root = document.getElementById(id).getElementsByTagName('tbody')[0];
    var rows = root.getElementsByTagName('tr');
    var clone = rows[rows.length - 1].cloneNode(true);
    cleanUpInputs(clone);
    root.appendChild(clone);
}

function removeLastRow(id) {
    var table = document.getElementById(id);
    var rowCount = table.rows.length;
    if (rowCount > 2) {table.deleteRow(rowCount - 1);}
}

function cleanUpInputs(obj) {
    for (let i = 0; i < obj.childNodes.length; ++i) {
        let n = obj.childNodes[i];
        if (n.childNodes && n.tagName !== 'INPUT') {
            cleanUpInputs(n);
        } else if (n.tagName === 'INPUT') {
            n.value = '';
        }
    }
}

window.onload = function addEventListeners() {
    const collectionAdd = document.getElementsByClassName("btn-multi-rows-add");
    Array.from(collectionAdd).forEach(btn => btn.addEventListener("click",
        function(){addRow(btn.getAttribute("target"))}, false));
    const collectionRemove = document.getElementsByClassName("btn-multi-rows-remove");
    Array.from(collectionRemove).forEach(btn => btn.addEventListener("click",
        function(){removeLastRow(btn.getAttribute("target"))}, false));
}
