const analyzeResumeBtn = document.getElementById("analyzeResumeBtn");

if (analyzeResumeBtn) {

    analyzeResumeBtn.addEventListener("click", async () => {

        const fileInput = document.getElementById("resumeFile");
        const results = document.getElementById("resumeResults");

        if (fileInput.files.length === 0) {

            results.innerHTML = "⚠ Please choose a PDF resume.";
            return;

        }

        const token = localStorage.getItem("access");

        const formData = new FormData();

        formData.append(
            "resume",
            fileInput.files[0]
        );

        results.innerHTML = "🤖 Analyzing your resume...";

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

            if (!response.ok) {

                console.error("Server Error:", data);

                results.innerHTML = `
                    <h3>❌ Error</h3>
                    <pre>${JSON.stringify(data, null, 2)}</pre>
                `;

                return;
            }

            results.innerHTML = `
                <div class="ai-response">

                    <h3>📄 ATS Score</h3>

                    <h1>${data.ats_score}%</h1>

                    <h3>✅ Strengths</h3>

                    <p>${(data.strengths || []).join("<br>")}</p>

                    <h3>⚠ Missing Skills</h3>

                    <p>${(data.missing_skills || []).join("<br>")}</p>

                    <h3>🚀 Recommendations</h3>

                    <p>${(data.recommendations || []).join("<br>")}</p>

                </div>
            `;

        } catch (error) {

            console.error("Resume Error:", error);

            results.innerHTML = `
                <h3>❌ Resume Analyzer Error</h3>
                <p>${error.message}</p>
            `;

        }

    });

}