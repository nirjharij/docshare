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

    success: function(res) {
      $("#"+folder_name).click(function(){
        $("folder").hide();});
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

function create_folder_request(x,y){
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
    data: JSON.stringify({'folder_name':x,'folder_path':y}),
    dataType: "json",
    // beforeSend: function(){$(".loader").show()},
    success: function(data) {
      msg="Folder Created Successfully";
      alert(msg);
      location.reload();
    },
    error: function(data){
      console.log(res);
    }
  });
}

function create_folder() {
  var folder_path = $("#directory").val()
  var folder=prompt("Folder Name","New Folder");
  if (name!=null){
    create_folder_request(folder,folder_path)
   }
}

$(document).ready(function(){
  $('#upload_url').val(window.location.href)
  $("#search-box").keyup(function(){
    $.ajax({
    type: "GET",
    url: AUTOCOMPLETE,
    data: {'searchedfor':$("#search-box").val(),'path':'zenatix'},
    dataType: "json",
    // beforeSend: function(){
    //   $("#search-box").css("background","#FFF url(LoaderIcon.gif) no-repeat 165px");
    // },
    success: function(res){
      $("#suggesstion-box").show();
      console.log(res)
      data = "<ul class='list-group'>"
      for (var i = 0; i < res.directories.directory.length; ++i) {  

        data = data + "<a class='list-group-item' href='/?path=zenatix/"+ res.directories.path[i] + res.directories.directory[i] +"'> <i class='glyphicon glyphicon-folder-open'></i>" + " &nbsp;&nbsp;&nbsp; " + res.directories.directory[i] + "</a>";
      }
      for (var i = 0; i < res.files.file.length; ++i) {
        data = data + "<a class='list-group-item' href='/?path=zenatix" + res.files.path[i] + "'>" + res.files.file[i] + "</a>";
      }
      data = data + '</ul>';
      $("#suggesstion-box").html(data);
      $("#search-box").css("background","#FFF");
    }
    });
  });
  $("#search-box").focusout(function(){
    $("#suggesstion-box").hide('slow');
  });

  var csrftoken = getCookie('csrftoken');
  var query = $('#query').valueOf();
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
  });

  $(".deldir").on('click',function(e){
    e.preventDefault();
    var id = $(this).attr('id');
    var path = $("#path-"+id).val();
    $.ajax({
    type: "POST",
    url: DELETE,
    data: {'path':path,'dir':id},
    dataType: "json",
    success: function(data) {
      msg="Directory Deleted Successfully";
      alert(msg);
      location.reload();
    },
    error: function(data){
      console.log(data);
    }
  });
  });

  $(".delfile").on('click',function(e){
    e.preventDefault();
    var id = $(this).attr('id');
    var path = $("#directory").val();
    $.ajax({
    type: "POST",
    url: DELETE,
    data: {'path':path,'file':id },
    dataType: "json",
    success: function(data) {
      msg="File Deleted Successfully";
      alert(msg);
      location.reload();
    },
    error: function(data){
      console.log(data);
    }
  });
  });
  // $("#folder").oncontextmenu = function() {return false;};

  // $("#folder").mousedown(function(e){ 
  //   if( e.button == 2 ) { 
  //     alert('Right mouse button!'); 
  //     return false; 
  //   } 
  //   return true; 
  // }); 
});

function findFiles() {
  // $("#search-box").val();
  $("#suggesstion-box").hide();
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







