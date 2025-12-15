const API_BASE_URL = "http://localhost:8000";


function loginPage() {
    const container = document.getElementById('app')
    const login = document.createElement('div')
    login.className = 'login-page'

    // login section
    const loginHeader = document.createElement('h1')
    loginHeader.textContent = "Login"
    loginHeader.className = 'login-header'

    login.appendChild(loginHeader);

    // login form
    const loginForm = document.createElement("form");
    loginForm.className = 'login-form'

    const usernameLabel = document.createElement("label");
    usernameLabel.textContent = "Username:";
    const usernameInput = document.createElement("input");
    usernameInput.type = "text";
    usernameInput.name = "username";
    usernameInput.required = true;

    const passwordLabel = document.createElement("label");
    passwordLabel.textContent = "Password:";
    const passwordInput = document.createElement("input");
    passwordInput.type = "password";
    passwordInput.name = "password";
    passwordInput.required = true;

    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = "Login";

    loginForm.appendChild(usernameLabel);
    loginForm.appendChild(usernameInput);
    loginForm.appendChild(passwordLabel);
    loginForm.appendChild(passwordInput);
    loginForm.appendChild(submitButton);

    login.appendChild(loginForm);

    // append to container

    // Register section
    const registerHeader = document.createElement('h1')
    registerHeader.textContent = "Don't have an account?"
    registerHeader.className = 'register-header'
    

    // register link
    const registerLink = document.createElement('a')
    registerLink.href = '#'
    registerLink.textContent = 'Register'
    registerLink.className = 'register-link'
    registerHeader.appendChild(registerLink);
    login.appendChild(registerHeader);

    // add event listener for register
    registerLink.addEventListener('click', function(e) {
        e.preventDefault();
        // Handle registration logic here
        renderRegisterPage()
    });
    container.appendChild(login);
}

function renderRegisterPage() {
    const container = document.getElementById('app')
    container.textContent = '';

    const register = document.createElement('div')
    register.className = 'register-page'

    const registerHeader = document.createElement('h1')
    registerHeader.textContent = "Register"
    registerHeader.className = 'register-header'

    register.appendChild(registerHeader);

    // registration form
    const registerForm = document.createElement("form");
    registerForm.className = 'register-form'

    const usernameLabel = document.createElement("label");
    usernameLabel.textContent = "Username:";
    const usernameInput = document.createElement("input");
    usernameInput.type = "text";
    usernameInput.name = "username";
    usernameInput.required = true;

    const passwordLabel = document.createElement("label");
    passwordLabel.textContent = "Password:";
    const passwordInput = document.createElement("input");
    passwordInput.type = "password";
    passwordInput.name = "password";
    passwordInput.required = true;

    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = "Register";

    registerForm.appendChild(usernameLabel);
    registerForm.appendChild(usernameInput);
    registerForm.appendChild(passwordLabel);
    registerForm.appendChild(passwordInput);
    registerForm.appendChild(submitButton);

    register.appendChild(registerForm);

    // append to container
    container.appendChild(register);
}

loginPage();