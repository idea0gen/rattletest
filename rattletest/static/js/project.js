/* Project specific Javascript goes here. */

var form_elements = document.getElementsByClassName("form-control");
for(var i=0;i<form_elements.length;i++) {
  form_elements.item(i).classList.add('form-control-sm');
}


// window.setTimeout(function() {
//   $(".alert").fadeTo(5000, 0).slideUp(5000, function(){
//       $(this).remove();
//   });
// }, 2000);

setTimeout(function () {
    // Closing the alert
    console.log("setTimeOut")
  $('#alert').alert('close');
}, 5000);
