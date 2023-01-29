$(document).ready(function() {
    $('#id_owner').select2();
    $('#id_category').select2();
    $('#id_user').select2();
    // DatePickerInput
    //$('#id_date').on('input', ev => onlysave());
});
window.dbdpEvents_date = {
    // DatePickerInput
    // https://getdatepicker.com/4/Events/
    // https://django-bootstrap-datepicker-plus.readthedocs.io/en/latest/customization.html#customize-single-input
    "dp.change": e => onlysave(),
}
function formatFileSize(bytes,decimalPoint) {
    if(bytes == 0) return '0 Bytes';
    var k = 1000,
        dm = decimalPoint || 2,
        sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
        i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
 }

function checkAll(){
var items = document.getElementsByName('checkbox_items');

    if (document.getElementById("checkbox_all").checked == true){
        for (var i = 0; i < items.length; i++) {
            if (items[i].type == 'checkbox')
                items[i].checked = true;
        }
        document.getElementById('files_id_delete').classList.remove("not-visible")
    } else {
        for (var i = 0; i < items.length; i++) {
            if (items[i].type == 'checkbox')
                items[i].checked = false;
        }
        document.getElementById('files_id_delete').classList.add("not-visible")
    }
}

function enable_delete_files(){
    var items = document.getElementsByName('checkbox_items');

    for (var i = 0; i < items.length; i++) {
        if (items[i].checked == true){
            document.getElementById('files_id_delete').classList.remove("not-visible")
            return
        }
    }
    document.getElementById('files_id_delete').classList.add("not-visible")
}

function confirmDeleteFiles(){
var msg = ''
var items = document.getElementsByName('checkbox_items');

    for (var i = 0; i < items.length; i++) {
        if (items[i].checked == true){
            msg += items[i].getAttribute('id') + ' '
        }
    }
    if (msg.length > 0){
        return confirmMsg('Confirm Delete: ' + msg)
    }

    return false
}

function confirmMsg(msg){
    if(window.confirm(msg)){
        return true;
    }else{return false;};
}
//document.getElementById("myInput2").getAttribute("name");
//document.getElementById('checkbox_all').classList.add("not-visible")
//document.getElementById('checkbox_clear').classList.remove("not-visible")

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function to_db(db){
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin', // Do not send CSRF token to another domain.        
        url: "/documents/db_change/",
        data: {
            "db": db,
        },
        success: function (data) {
            window.location.href = data.url //redirect            
        },
        failure: function (data) {
            console.log("failure");
            console.log(data);
        },
    });

}

function onlysave(){
    // if creating new record it will return, otherwise there are form errors
    if( ! document.getElementById("save")) return

    document.getElementById('delete').classList.add("not-visible")
    document.getElementById('onlysave').hidden = true;

    document.getElementById('reload').classList.remove("not-visible")
    document.getElementById('save').classList.remove("not-visible")
}