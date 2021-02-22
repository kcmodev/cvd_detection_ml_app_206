document.getElementById("showDatasetButton").addEventListener('click', showDataset)
document.getElementById("logoutButton").addEventListener("click", logout)

function showDataset() {
    $.ajax({
       type: "GET",
       url: "/dashapp/",
       success: function(){
           window.location.href = '/dashapp/'
       }
    });
}

function logout() {
    $.ajax({
       type: "GET",
       url: "/logout",
       success: function(){
           window.location.href = '/index'
       }
    });
}