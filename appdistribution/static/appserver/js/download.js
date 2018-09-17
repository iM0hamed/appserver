$(document).ready(function(){
  $("#appname").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    console.log(value);
    $("#appNameTable > tbody > tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

function refreshPage(field, value){
    $('#' + field).val(value);
    $('#' + field + 'btn').html(value + " <span class='caret'></span>");
    $('#downloadForm').submit();
}