console.log("Career Pilot AI dashboard loaded");


const API_URL = "";

const token = localStorage.getItem("access");



// =======================
// LOGOUT
// =======================

const logoutBtn = document.getElementById("logoutBtn");


if(logoutBtn){

    logoutBtn.addEventListener("click",()=>{

        localStorage.removeItem("access");
        localStorage.removeItem("refresh");

        window.location.href="/login/";

    });

}



// =======================
// LOAD DASHBOARD DATA
// =======================


async function loadDashboard(){


    if(!token){

        window.location.href="/login/";
        return;

    }



    const response = await fetch(

        `${API_URL}/api/dashboard/`,

        {

            headers:{

                "Authorization":
                `Bearer ${token}`

            }

        }

    );



    if(response.ok){


        const data = await response.json();


        document.getElementById(
            "totalApplications"
        ).innerHTML =
        data.total_applications || 0;



        document.getElementById(
            "interviews"
        ).innerHTML =
        data.interviews || 0;



        document.getElementById(
            "offers"
        ).innerHTML =
        data.offers || 0;



        document.getElementById(
            "successRate"
        ).innerHTML =
        `${data.success_rate || 0}%`;

    }



}



// =======================
// RECENT APPLICATIONS
// =======================


async function loadApplications(){


    const response = await fetch(

        `${API_URL}/api/applications/`,

        {

            headers:{

                "Authorization":
                `Bearer ${token}`

            }

        }

    );



    if(response.ok){


        const data = await response.json();


        const table =
        document.getElementById(
            "applicationsTable"
        );


        table.innerHTML="";



        data.results.forEach(app=>{


            table.innerHTML += `

            <tr>

            <td>${app.company}</td>

            <td>${app.position}</td>

            <td>${app.status}</td>

            <td>${app.date_applied}</td>

            </tr>

            `;


        });


    }


}



// =======================
// AI SKILL ANALYSIS
// =======================


const analyzeBtn =
document.getElementById(
    "analyzeBtn"
);



if(analyzeBtn){


analyzeBtn.addEventListener(
"click",

async()=>{


const jobDescription =
document.getElementById(
"jobDescription"
).value;



const results =
document.getElementById(
"results"
);



if(!jobDescription.trim()){


    results.innerHTML =
    "⚠ Please paste a job description";


    return;

}



results.innerHTML =
"🤖 AI analysing...";



const response = await fetch(

`${API_URL}/api/ai/analyze-job/`,

{


method:"POST",


headers:{


"Content-Type":
"application/json",


"Authorization":
`Bearer ${token}`


},


body:JSON.stringify({


job_description:
jobDescription


})


}

);



const data =
await response.json();



console.log(
"AI RESULT",
data
);



if(!response.ok){


results.innerHTML =
`
❌ ${JSON.stringify(data)}
`;

return;


}



// UPDATE CARDS


document.getElementById(
"matchScore"
).innerHTML =
`${data.match_score || 0}%`;



document.getElementById(
"skillsCount"
).innerHTML =
(data.skills_found || []).length;



document.getElementById(
"missingCount"
).innerHTML =
(data.missing_skills || []).length;




// SHOW REPORT


results.innerHTML = `


<div class="ai-report">


<h2>
🤖 Career Analysis
</h2>


<h1>
${data.match_score || 0}%
</h1>


<h3>
✅ Skills Found
</h3>

<p>

${(data.skills_found || []).join(", ")}

</p>



<h3>
⚠ Missing Skills
</h3>


<p>

${(data.missing_skills || []).join(", ")}

</p>



<h3>
🚀 Recommendation
</h3>


<p>
${data.recommendation || ""}
</p>



</div>


`;



}

);


}



// START

loadDashboard();

loadApplications();


