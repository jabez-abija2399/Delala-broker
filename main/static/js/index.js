// let signup = document.querySelector(".signup");
// let login = document.querySelector(".login");
// let slider = document.querySelector(".slider");
// let formSection = document.querySelector(".form-section");
 
// signup.addEventListener("click", () => {
    
//     window.location.href = '/register';  
// });
 
// login.addEventListener("click", () => {
//     window.location.href = '/login';  //
// });

// let signupBtn = document.querySelector(".register-btn");
// let loginBtn = document.querySelector(".login-btn");
// let slider = document.querySelector(".slider");
// let formSection = document.querySelector(".form-section");

// signupBtn.addEventListener("click", () => {

//     window.location.href = "{{ url_for('register') }}"; // Redirect to the register route
// });

// loginBtn.addEventListener("click", () => {
//     window.location.href = "{{ url_for('login') }}"; // Redirect to the login route
// });


// let signup = document.querySelector(".signup");
// let login = document.querySelector(".login");
// let slider = document.querySelector(".slider");
// let formSection = document.querySelector(".form-section");

// signup.addEventListener("click", () => {
//     console.log("Signup button clicked");
//     slider.classList.add("moveslider");
//     formSection.classList.add("form-section-move");
// });

// login.addEventListener("click", () => {
//     console.log("Login button clicked");
//     slider.classList.remove("moveslider");
//     formSection.classList.remove("form-section-move");
//     window.location.href = '/login';
// });


document.addEventListener('DOMContentLoaded', function () {
    const loginButton = document.querySelector('.login');
    const signupButton = document.querySelector('.signup');
    const slider = document.querySelector('.slider');
    const formSection = document.querySelector('.form-section');

    loginButton.addEventListener('click', () => {
        window.location.href = '/login';
    });

    signupButton.addEventListener('click', () => {
        window.location.href = '/register';  
    });

    signupButton.addEventListener('click', () => {
        formSection.classList.add('form-section-move');
        slider.style.left = '250px';
    });

    loginButton.addEventListener('click', () => {
        formSection.classList.remove('form-section-move');
        slider.style.left = '100px';
    });
});


