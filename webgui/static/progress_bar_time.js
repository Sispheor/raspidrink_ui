$(document).ready(function () {
    var start = new Date();
    var maxTime = document.getElementById("max_time").value;
    var timeoutVal = Math.floor(maxTime/100);
    animateUpdate();

    function updateProgress(percentage) {
        $('#progress_bar').css("width", percentage + "%");
    }

    function animateUpdate() {
        var now = new Date();
        var timeDiff = now.getTime() - start.getTime();
        var perc = Math.round((timeDiff/maxTime)*100);
        console.log(perc);
          if (perc <= 100) {
           updateProgress(perc);
           setTimeout(animateUpdate, timeoutVal);
          }else{
            $('#myModal').modal('show');
          }
    }

});


