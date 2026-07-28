async function askAssistant() {

    const question = document.getElementById(
        "assistantQuestion"
    ).value;


    const answerBox = document.getElementById(
        "assistantAnswer"
    );


    const token = localStorage.getItem(
        "access"
    );


    if (!question.trim()) {

        answerBox.innerHTML =
            "Please enter a question.";

        return;
    }


    answerBox.innerHTML =
        "🤖 Career Pilot AI is thinking...";


    const response = await fetch(
        "/api/ai/assistant/",
        {
            method: "POST",

            headers: {

                "Content-Type": "application/json",

                "Authorization":
                `Bearer ${token}`

            },

            body: JSON.stringify({

                question: question

            })

        }
    );


    const data = await response.json();


    answerBox.innerHTML =
    `
    <div class="ai-response">

        <h3>
        🤖 Career Pilot AI
        </h3>

        <p>
        ${(data.answer || data.detail).replace(/\n/g, "<br>")}
        </p>

    </div>
    `;

}