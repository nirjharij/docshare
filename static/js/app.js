function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function listdir(current_directory,folder_name){
  $.ajax({  
    type: "GET",
    url: LISTDIR,
    data: {'folder_name':folder_name,'current_directory':current_directory},
    dataType: "json",
    
    // beforeSend: function(){$(".loader").show()},
    success: function(res) {
      console.log(res.data.directories)
      data = "<ul class='list-group'>"
      for (var i = 0; i < res.data.directories.length; ++i) {  
        data = data + '<a href="#" class="list-group-item">' + '<i class="glyphicon glyphicon-folder-open"></i>' +' &nbsp;&nbsp;&nbsp; ' + res.data.directories[i] + "</a>";
      }
      for (var i = 0; i < res.data.files.length; ++i) {
        data = data + '<a href="#" class="list-group-item">' + res.data.files[i] + "</a>";
      }
      data = data + '</ul>';
      $('#directory-div-'+folder_name).html(data);
    },
    error: function(res){
      console.log(res);
    }
  });
}

function download(current_directory,filename){
  $.ajax({  
    type: "GET",
    url: DOWNLOAD,
    data: {'folder_name':folder_name,'current_directory':current_directory},
    dataType: "json",
    // beforeSend: function(){$(".loader").show()},
    success: function(res) {
      msg="File downloaded Successfully at path: ";
      alert(msg+res.data);
    },
    error: function(res){
      console.log(res);
    }
  });
}



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function create_folder_request(x){
  var msg;
  var csrftoken = getCookie('csrftoken');
  var query = $('#query').valueOf();
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });
  $.ajax({  
    type: "POST",
    url: CREATE_FOLDER,
    data: JSON.stringify({'folder_name':x}),
    dataType: "json",
    // beforeSend: function(){$(".loader").show()},
    success: function(data) {
      console.log(data)
      msg="Folder Created Successfully";
      alert(msg);
    },
    error: function(data){
      console.log(res);
    }
  });
}

function create_folder() {
  var folder=prompt("Folder Name","New Folder");
  if (name!=null){
    create_folder_request(folder)
   }
}

function upload_file(){
  var x = document.createElement("INPUT");
  x.setAttribute("type", "file");
  document.body.appendChild(x);
}

function listOptions() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {

    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}