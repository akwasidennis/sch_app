let dropzone = document.getElementById('dropzone');
let btn = document.getElementById('butt');

function highlight(event){
    event.preventDefault();
    dropzone.style.backgroundColor = "#2f4f4f";
    event.target.style.backgroundColor = "#2f4f4f";
    dropzone.style.zIndex = '2';
    // btn.style.display = 'block'
}

function unhighlight(event) {
    event.preventDefault();
    dropzone.style.backgroundColor = "#ffffff";
    event.target.style.backgroundColor = "#ffffff";
    // btn.style.display = 'none'
    location.reload(true);
    
}

function cancel(){
    location.reload(true);
}


$(function() { //on page load

    $( ".row" ).each(function( index ) { //replace each url
      var url = $(this).attr('href'); //get current url
      var encodedUrl = encodeURIComponent(url); //enconde url
      $(this).attr("href", encodedUrl); //replace
    });

});

function toBottom(){
    window.scrollTo(0, document.body.scrollHeight);
}