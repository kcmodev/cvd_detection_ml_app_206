window.addEventListener('load', function () {
    let element = document.getElementById("logoutButton")

    if (element){
        element.addEventListener('click', logoutUser);
    }
})

function logoutUser() {
        console.log('logout clicked');
        window.location.href = "/logout";
}

