document.getElementById("logoutButton").addEventListener("click", logout)

function logout() {
    $.ajax({
       type: "GET",
       url: "/index",
       success: function(){
           window.location.href = this.url
       }
    });
}