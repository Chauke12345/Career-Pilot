const API_URL = "";

const token = localStorage.getItem("access");



async function loadApplications() {


    if (!token) {

        alert("Please login first.");

        window.location.href = "/login/";

        return;

    }



    const response = await fetch(

        `${API_URL}/api/applications/`,

        {

            headers: {

                "Authorization":
                `Bearer ${token}`,

                "Content-Type":
                "application/json"

            }

        }

    );



    if (!response.ok) {


        alert(
            "Session expired. Please login again."
        );


        localStorage.removeItem("access");


        window.location.href = "/login/";


        return;

    }




    const data = await response.json();



    const tbody =
    document.getElementById(
        "applicationsBody"
    );



    tbody.innerHTML = "";



    data.results.forEach(app => {



        tbody.innerHTML += `


        <tr>


            <td>
                ${app.company}
            </td>


            <td>
                ${app.position}
            </td>


            <td>
                ${app.status}
            </td>


            <td>
                ${app.date_applied}
            </td>



            <td>


                <button
                onclick="editApplication(${app.id})">

                    Edit

                </button>



                <button
                onclick="deleteApplication(${app.id})">

                    Delete

                </button>


            </td>



        </tr>


        `;



    });



}






// CREATE APPLICATION


document
.getElementById("applicationForm")
.addEventListener(

"submit",

async function(e){


    e.preventDefault();



    const response = await fetch(

        `${API_URL}/api/applications/`,

        {


            method:"POST",



            headers:{


                "Content-Type":
                "application/json",


                "Authorization":
                `Bearer ${token}`


            },



            body:JSON.stringify({


                company:

                document
                .getElementById("company")
                .value,



                position:

                document
                .getElementById("position")
                .value,



                location:

                document
                .getElementById("location")
                .value,



                status:

                document
                .getElementById("status")
                .value,



                date_applied:

                document
                .getElementById("date_applied")
                .value,



                job_link:

                document
                .getElementById("job_link")
                .value,



                notes:

                document
                .getElementById("notes")
                .value



            })


        }

    );



    const data =
    await response.json();



    console.log(data);




    if(response.ok){


        alert(
            "Application saved!"
        );



        document
        .getElementById("applicationForm")
        .reset();



        loadApplications();



    }

    else{


        console.log(
            "Save error:",
            data
        );


        alert(
            "Failed to save application"
        );


    }



}

);









// DELETE APPLICATION


async function deleteApplication(id){



    if(
        !confirm(
            "Delete this application?"
        )
    ){

        return;

    }




    const response = await fetch(

        `${API_URL}/api/applications/${id}/`,

        {


            method:"DELETE",



            headers:{


                "Authorization":
                `Bearer ${token}`


            }


        }

    );





    if(response.ok){



        alert(
            "Application deleted!"
        );



        loadApplications();



    }

    else{


        alert(
            "Delete failed"
        );


    }



}









// EDIT APPLICATION

let editingId = null;



async function editApplication(id){


    editingId = id;


    const response = await fetch(

        `${API_URL}/api/applications/${id}/`,

        {

            headers:{

                "Authorization":
                `Bearer ${token}`

            }

        }

    );


    const app = await response.json();



    document.getElementById(
        "edit_company"
    ).value = app.company;



    document.getElementById(
        "edit_position"
    ).value = app.position;



    document.getElementById(
        "edit_location"
    ).value = app.location;



    document.getElementById(
        "edit_status"
    ).value = app.status;



    document.getElementById(
        "edit_job_link"
    ).value = app.job_link;



    document.getElementById(
        "edit_notes"
    ).value = app.notes;



    document.getElementById(
        "editModal"
    ).style.display = "flex";


}





function closeEdit(){


    document.getElementById(
        "editModal"
    ).style.display = "none";


}





async function saveEdit(){


    const response = await fetch(

        `${API_URL}/api/applications/${editingId}/`,

        {


            method:"PATCH",


            headers:{


                "Content-Type":
                "application/json",


                "Authorization":
                `Bearer ${token}`


            },


            body:JSON.stringify({


                company:
                document.getElementById(
                    "edit_company"
                ).value,


                position:
                document.getElementById(
                    "edit_position"
                ).value,


                location:
                document.getElementById(
                    "edit_location"
                ).value,


                status:
                document.getElementById(
                    "edit_status"
                ).value,


                job_link:
                document.getElementById(
                    "edit_job_link"
                ).value,


                notes:
                document.getElementById(
                    "edit_notes"
                ).value


            })


        }


    );



    if(response.ok){


        alert(
            "Application updated!"
        );


        closeEdit();


        loadApplications();


    }

    else{


        alert(
            "Update failed"
        );


    }


}