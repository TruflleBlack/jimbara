let menu = document.querySelector('#menu-btn');
let navbar = document.querySelector('.navbar');

menu.onclick = () =>{
    menu.classList.toggle('fa-times-circle');
    navbar.classList.toggle('active');
}

window.onscroll = () =>{
    menu.classList.remove('fa-times-circle');
    navbar.classList.remove('active');
}

document.addEventListener('DOMContentLoaded', function() {
    if (!document.body.classList.contains('test-page')) {
        const mulaiBtn = document.querySelector('.mulai-btn');
        const popupInfo = document.querySelector('.popup-info');
        const exitBtn = document.querySelector('.exit-btn');
        const main = document.querySelector('.main');


        mulaiBtn.onclick = () => {
            popupInfo.classList.add('active');
            main.classList.add('active');
        }

        exitBtn.onclick = () => {
            popupInfo.classList.remove('active');
            main.classList.remove('active');
        }
    }
});