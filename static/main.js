$(document).ready(function(){
$('#add-task-form').on('submit', function(e) {
e.preventDefault();
var title=$('#title').val();
var description=$('#description').val();
var due_date=$('#due-date').val();

$.ajax({
url:'/task',
method:'POST',
contentType:'application/json',
dataType:'json',
data:JSON.stringify({title:title,description:description,due_date:due_date}),
success:function(response){
location.reload();
}
});
});

window.deleteTask=function(id){
$.ajax({
url:'/task/'+id,
type:'DELETE',
success:function(result){
location.reload();
}
});
}

window.editTask=function(id){
// Fetch current values first
$.ajax({
url: '/task/' + id,
type: 'GET',
success:function(result){
var title=prompt("Enter new title", result.title);
var description=prompt("Enter new description", result.description);
var due_date=prompt("Enter new due date", result.due_date);

// Update with new values
$.ajax({
url: '/task/' + id,
type: 'PUT',
contentType: 'application/json',
dataType: 'json',
data: JSON.stringify({
'title': title,
'description': description,
'due_date': due_date
}),
success:function(result){
location.reload();
}
});
}
});
}
});
