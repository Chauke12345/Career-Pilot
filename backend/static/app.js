console.log("Career Pilot AI JS loaded");


const API_URL = "http://127.0.0.1:8000";



// ELEMENTS

const analyzeBtn =
document.getElementById("analyzeBtn");


const results =
document.getElementById("results");


const matchScore =
document.getElementById("matchScore");


const skillsCount =
document.getElementById("skillsCount");


const missingCount =
document.getElementById("missingCount");



console.log("Analyze button:", analyzeBtn);
console.log("Results:", results);





// ANALYZE BUTTON

if(analyzeBtn){


analyzeBtn.addEventListener(
"click",
async function(){



    const jobDescription =
    document
    .getElementById("jobDescription")
    .value;



    if(!jobDescription.trim()){


        results.innerHTML = `

        <div class="ai-report">

        ⚠ Please paste a job description first.

        </div>

        `;


        return;

    }




    const token =
    localStorage.getItem("access");



    if(!token){


        alert(
            "Please login again."
        );


        window.location.href="/login/";

        return;

    }





    results.innerHTML = `

    <div class="ai-report">

    🤖 AI is analyzing the job description...

    </div>

    `;




    try{


        const response =
        await fetch(

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


        });


        



        const data =
        await response.json();



        console.log(
            "AI RESPONSE:",
            data
        );





        if(!response.ok){


            throw new Error(

                data.detail ||
                "AI analysis failed"

            );


        }






        // DASHBOARD CARDS


        if(matchScore){


            matchScore.innerHTML =

            `${data.match_score || 0}%`;


        }




        if(skillsCount){


            skillsCount.innerHTML =

            data.skills_found?.length || 0;


        }





        if(missingCount){


            missingCount.innerHTML =

            data.missing_skills?.length || 0;


        }






        // SHOW REPORT


        results.innerHTML = `


        <div class="ai-report">


            <h2>
            🤖 Career Analysis
            </h2>



            <div class="score">

                <h1>
                ${data.match_score || 0}%
                </h1>


                <p>
                Skill Match
                </p>


            </div>




            <h3>
            ✅ Skills Found
            </h3>


            <div class="tags">


            ${
            (data.skills_found || [])
            .map(skill =>

            `<span>${skill}</span>`

            )
            .join("")
            }


            </div>





            <h3>
            ⚠ Missing Skills
            </h3>



            <div class="tags missing">


            ${
            (data.missing_skills || [])
            .map(skill =>

            `<span>${skill}</span>`

            )
            .join("")
            }


            </div>





            <h3>
            🚀 Recommendation
            </h3>



            <p>

            ${
            data.recommendation ||
            "No recommendation available."
            }

            </p>



        </div>


        `;




    }



    catch(error){



        console.error(
            "AI ERROR:",
            error
        );



        results.innerHTML = `


        <div class="ai-report">


            <h3>
            ❌ Analysis Error
            </h3>


            <p>
            ${error.message}
            </p>


        </div>


        `;



    }



});


}

else{


console.error(
"Analyze button missing"
);


}