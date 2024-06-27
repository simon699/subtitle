function  showLogin(){
        document.getElementById('loginview').style.display = 'block';
        document.getElementById('signview').style.display = 'none';

}

function  showRegister(){
    document.getElementById('signview').style.display = 'block';
    document.getElementById('loginview').style.display = 'none';

}

document.addEventListener('DOMContentLoaded', function() {


    if (name == 'login'){
        showLogin()
    }else if (name == 'sign'){
        showRegister()
    }
});