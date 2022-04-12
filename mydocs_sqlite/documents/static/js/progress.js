// based on https://anshu-dev.medium.com/file-upload-progress-bar-using-django-and-ajax-ba4eb7482d9c

const uploadForm = document.getElementById('upload_form');
const input_file = document.getElementById('file_name');
const progress_bar = document.getElementById('progress');

$("#upload_form").submit(function(e){
    e.preventDefault();
    $form = $(this)
    var formData = new FormData(this);
    const media_data = input_file.files[0];
    if(media_data != null){
        console.log(media_data);
        progress_bar.classList.remove("not-visible");

        var fi = document.getElementById('file_name');
        var progress_label = 'Uploading:<br>'
        var fsize = 0
        for (var i = 0; i <= fi.files.length - 1; i++) {
            progress_label += '<b>' + fi.files.item(i).name + '</b> - size ' + 
                                formatFileSize(fi.files.item(i).size) + '<br>'
            fsize += fi.files.item(i).size
        }
        progress_label += 'Total size: ' + formatFileSize(fsize) + '<br>'
        document.getElementById('progress_label').innerHTML = progress_label
    }

    $.ajax({
        type: 'POST',
        url:'/documents/file_upload/'+ document.getElementById('document_id').value,
        data: formData,
        dataType: 'json',
        beforeSend: function(){

        },
        xhr:function(){
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e=>{
                if(e.lengthComputable){
                    const percentProgress = (e.loaded/e.total)*100;
                    console.log(percentProgress);
                    progress_bar.innerHTML = 
                    `<div class="progress-bar progress-bar-striped bg-success" role="progressbar"
                    style="width: ${percentProgress}%" aria-valuenow="${percentProgress}"
                    aria-valuemin="0" aria-valuemax="100"></div>`
                }
            });
            return xhr
        },
        success: function(response){
            console.log(response);
            uploadForm.reset()
            progress_bar.classList.add('not-visible')
            document.getElementById('progress_label').innerHTML = ''
            window.location.href='/documents/file_upload/'+ document.getElementById('document_id').value
        },
        error: function(err){
            console.log(err);
        },
        cache: false,
        contentType: false,
        processData: false,
    });
});
