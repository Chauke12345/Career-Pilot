const API_URL = "";


const button = document.getElementById("signupBtn");
const message = document.getElementById("message");


button.addEventListener("click", async () => {


    const username = document.getElementById("username").value;

    const email = document.getElementById("email").value;

    const password = document.getElementById("password").value;



    const response = await fetch(
        `${API_URL}/api/accounts/register/`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        }
    );


    const data = await response.json();


    console.log(data);


    if(response.ok){

        message.innerHTML = "✅ Account created successfully!";

        setTimeout(() => {
            window.location.href = "/login/";
        }, 1500);

    }
    else{

        message.innerHTML =
        "❌ " + JSON.stringify(data);

    }


});F