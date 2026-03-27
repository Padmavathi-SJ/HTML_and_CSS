let questions = [];
let currentIndex = 0;
let score = 0;
let selectedOption = null;

// ✅ Load JSON file
async function fetchQuestions() {
    try {
        const response = await fetch("questions.json");
        questions = await response.json();

        loadQuestion(); // ✅ correct call

    } catch (error) {
        document.getElementById("question").textContent = "Failed to load questions.";
    }
}

// ✅ Load single question
function loadQuestion() {
    const q = questions[currentIndex];

    document.getElementById("question").textContent = q.question;

    const optionsDiv = document.getElementById("options");
    optionsDiv.innerHTML = "";

    q.options.forEach(option => {
        const btn = document.createElement("div");
        btn.textContent = option;
        btn.classList.add("option");

        btn.addEventListener("click", () => {
            selectedOption = option;

            // Highlight selected
            document.querySelectorAll(".option").forEach(opt => {
                opt.classList.remove("selected");
            });

            btn.classList.add("selected");
        });

        // ✅ append outside click
        optionsDiv.appendChild(btn);
    });
}

// ✅ Next button
function nextQuestion() {
    if (selectedOption === null) {
        alert("Please select an option.");
        return;
    }

    if (selectedOption === questions[currentIndex].answer) {
        score++;
    }

    selectedOption = null;
    currentIndex++;

    if (currentIndex < questions.length) {
        loadQuestion();
    } else {
        showResult();
    }
}

// ✅ Show result
function showResult() {
    document.querySelector(".quiz-container").innerHTML = `
        <h2>Your Score: ${score}/${questions.length}</h2>
        <p>${score === questions.length ? "Excellent!" : "Good try!"}</p>
    `;
}

// ✅ Initial load
fetchQuestions();