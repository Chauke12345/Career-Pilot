console.log("match.js loaded");


document.addEventListener(
    "DOMContentLoaded",
    function () {


        const matchBtn = document.getElementById(
            "matchBtn"
        );


        if (!matchBtn) {

            console.error(
                "Match button not found"
            );

            return;

        }



        matchBtn.addEventListener(
            "click",
            async function () {


                console.log(
                    "Match button clicked"
                );



                const resumeInput =
                    document.getElementById(
                        "matchResume"
                    );


                const jobDescriptionInput =
                    document.getElementById(
                        "matchJobDescription"
                    );


                const results =
                    document.getElementById(
                        "matchResults"
                    );



                console.log(
                    "Textarea element:",
                    jobDescriptionInput
                );



                if (!resumeInput || !jobDescriptionInput || !results) {

                    console.error(
                        "Required elements missing"
                    );

                    return;

                }



                const resume =
                    resumeInput.files[0];



                const jobDescription =
                    jobDescriptionInput.value.trim();



                console.log(
                    "Job Description length:",
                    jobDescription.length
                );


                console.log(
                    "Job Description content:",
                    jobDescription
                );




                if (!resume) {


                    results.innerHTML = `

                    <p>
                    ⚠ Please upload your CV.
                    </p>

                    `;


                    return;

                }




                if (!jobDescription) {


                    results.innerHTML = `

                    <p>
                    ⚠ Please paste a job description.
                    </p>

                    `;


                    return;

                }




                const token =
                    localStorage.getItem(
                        "access"
                    );



                if (!token) {


                    results.innerHTML = `

                    <p>
                    ⚠ Session expired. Please login again.
                    </p>

                    `;


                    return;

                }




                const formData =
                    new FormData();



                formData.append(
                    "resume",
                    resume
                );



                formData.append(
                    "job_description",
                    jobDescription
                );




                results.innerHTML = `

                <p>
                🤖 AI is comparing your CV with the job...
                </p>

                `;



                try {


                    const response =
                        await fetch(
                            "/api/ai/match-resume/",
                            {

                                method: "POST",

                                headers: {

                                    "Authorization":
                                    `Bearer ${token}`

                                },

                                body: formData

                            }
                        );



                    const data =
                        await response.json();



                    console.log(
                        "JOB MATCH RESPONSE:",
                        data
                    );



                    if (!response.ok) {


                        throw new Error(
                            JSON.stringify(
                                data,
                                null,
                                2
                            )
                        );

                    }




                    results.innerHTML = `


                    <div class="match-card">


                    <h2>
                    🎯 Resume Job Match
                    </h2>


                    <h1>
                    ${data.match_score || 0}%
                    </h1>



                    <h3>
                    ✅ Matching Skills
                    </h3>


                    <ul>

                    ${
                        (data.matching_skills || [])
                        .map(
                            skill =>
                            `<li>${skill}</li>`
                        )
                        .join("")
                        ||
                        "<li>No matching skills found</li>"
                    }

                    </ul>





                    <h3>
                    ⚠ Missing Skills
                    </h3>


                    <ul>

                    ${
                        (data.missing_skills || [])
                        .map(
                            skill =>
                            `<li>${skill}</li>`
                        )
                        .join("")
                        ||
                        "<li>No missing skills found</li>"
                    }

                    </ul>





                    <h3>
                    🚀 Recommendations
                    </h3>


                    <ul>

                    ${
                        (data.recommendations || [])
                        .map(
                            item =>
                            `<li>${item}</li>`
                        )
                        .join("")
                        ||
                        "<li>No recommendations available</li>"
                    }

                    </ul>


                    </div>


                    `;



                }

                catch(error) {


                    console.error(
                        "JOB MATCH ERROR:",
                        error
                    );



                    results.innerHTML = `


                    <div class="error">


                    <h3>
                    ❌ Resume Matching Failed
                    </h3>


                    <pre>
                    ${error.message}
                    </pre>


                    </div>


                    `;


                }


            }
        );


    }
);