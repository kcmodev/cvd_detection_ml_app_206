document.getElementById("logoutButton").addEventListener("click", logoutUser)

function logoutUser() {
    $.ajax({
       type: "GET",
       url: "/index",
       success: function(){
           window.location.href = this.url
       }
    });
}