

var sliceFile = function(file, callback) {
    var formData = new FormData();
    formData.append('stl', file, file.name);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'slice', true);
    xhr.onload = function () {
      if (xhr.status === 200) {
        return callback(null, xhr.response);
      } else {
        return callback(xhr.response, null);
      }
    };
    xhr.send(formData);
}

var createDataUrl = function(type, data) {
    data = btoa(data);
    return "data:"+type+";base64,"+data;
}

var main = function() {
    var form = document.getElementById('file-form');
    var fileSelect = document.getElementById('file-select');
    var uploadButton = document.getElementById('upload-button');
    var downloadLink = document.getElementById('download-link');
    var output = document.getElementById('output');

    form.onsubmit = function(event) {
        event.preventDefault();
        uploadButton.innerHTML = 'Slicing...';

        sliceFile(fileSelect.files[0], function(err, result) {            
            uploadButton.innerHTML = (err) ? 'Failed' : 'Slice';
            if (!err) {
                output.innerHTML = result.slice(0, 100);
                downloadLink.setAttribute('href', createDataUrl("text/plain", result));
            }
        });
    }
}

window.addEventListener('load', main, false);
