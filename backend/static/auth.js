const API_URL = "";


const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");


loginForm.addEventListener("submit", async function(event) {

    event.preventDefault();


    const username =
        document.getElementById("username").value;


    const password =
        document.getElementById("password").value;


    try {

        const response = await fetch(
            `${API_URL}/api/token/`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username,
                    password
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {
            throw new Error(
                data.detail || "Login failed"
            );
        }


        localStorage.setItem(
            "access",
            data.access
        );


        localStorage.setItem(
            "refresh",
            data.refresh
        );


        message.innerHTML =
            "Login successful ✅";


        window.location.href = "index.html";


    } catch(error) {

        message.innerHTML =
            "Login failed ❌ " + error.message;


        console.error(error);

    }

});