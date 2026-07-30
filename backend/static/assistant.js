async function askAssistant() {

    const question = document.getElementById("assistantQuestion").value;
    const answerBox = document.getElementById("assistantAnswer");
    const token = localStorage.getItem("access");

    if (!question.trim()) {
        answerBox.innerHTML = "Please enter a question.";
        return;
    }

    answerBox.innerHTML = "🤖 Career Pilot AI is thinking...";

    try {

        const response = await fetch("/api/ai/assistant/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Assistant request failed.");
        }

        answerBox.innerHTML = `
            <div class="ai-response">
                <h3>🤖 Career Pilot AI</h3>
                <p>${(data.answer || "").replace(/\n/g, "<br>")}</p>
            </div>
        `;

    } catch (error) {
        console.error(error);
        answerBox.innerHTML = `❌ ${error.message}`;
    }
}

const assistantBtn = document.getElementById("assistantBtn");

if (assistantBtn) {
    assistantBtn.addEventListener("click", askAssistant);
}