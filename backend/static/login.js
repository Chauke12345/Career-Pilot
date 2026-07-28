const API_URL = "http://127.0.0.1:8000";


const form = document.getElementById("loginForm");
const message = document.getElementById("message");


form.addEventListener("submit", async (event)=>{

    event.preventDefault();


    const username =
    document.getElementById("username").value;


    const password =
    document.getElementById("password").value;



    try {

        const response = await fetch(
            `${API_URL}/api/token/`,
            {
                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );


        const data = await response.json();


        console.log(data);



        if(response.ok){

            localStorage.setItem(
                "access",
                data.access
            );


            localStorage.setItem(
                "refresh",
                data.refresh
            );


            message.innerHTML =
            "Login successful";


            window.location.href =
            "/dashboard/";

        }
        else{

            message.innerHTML =
            data.detail || "Login failed";

        }



    } catch(error){

        console.log(error);

        message.innerHTML =
        "Server error";

    }


});