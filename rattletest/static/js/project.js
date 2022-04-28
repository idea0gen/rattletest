/* Project specific Javascript goes here. */

var form_elements = document.getElementsByClassName("form-control");
for(var i=0;i<form_elements.length;i++) {
  form_elements.item(i).classList.add('form-control-sm');
}

setTimeout(function () {
    // Closing the alert
  $('#alert').alert('close');
}, 5000);
