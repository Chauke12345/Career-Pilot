document.getElementById("analyzeResumeBtn").addEventListener(
    "click",
    async () => {


        const fileInput = document.getElementById("resumeFile");

        const file = fileInput.files[0];


        if (!file) {

            alert("Please upload your resume PDF");

            return;

        }



        const formData = new FormData();


        formData.append(
            "resume",
            file
        );



        const token = localStorage.getItem("access");



        try {


            const response = await fetch(
                "/api/resume/analyze/",
                {

                    method: "POST",

                    headers: {

                        "Authorization": `Bearer ${token}`

                    },

                    body: formData

                }
            );



            const data = await response.json();



            console.log(data);



            document.getElementById(
                "resumeResults"
            ).innerHTML = `

                <h3>Resume Analysis</h3>

                <pre>
${JSON.stringify(data, null, 2)}
                </pre>

            `;



        } catch(error) {


            console.error(
                "Resume Analyzer Error:",
                error
            );


            document.getElementById(
                "resumeResults"
            ).innerHTML =
            "❌ Resume analysis failed";


        }


    }
);