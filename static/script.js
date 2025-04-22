// Bootstrap popover dependencies
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

document.addEventListener("DOMContentLoaded", function () {
    let toggleBtn = document.getElementById("toggleBtn");
    let sidebar = document.getElementById("sidebar");
    let mainContent = document.getElementById("mainContent");
    let menuText = document.querySelectorAll(".menu-text");

    // Function to update tooltips based on sidebar state
    function updateTooltips() {
        let isCollapsed = sidebar.style.width === "80px";

        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(tooltipEl => {
            let tooltipInstance = bootstrap.Tooltip.getInstance(tooltipEl);
            if (isCollapsed) {
                if (!tooltipInstance) {
                    new bootstrap.Tooltip(tooltipEl); // Initialize tooltip if collapsed
                }
            } else {
                if (tooltipInstance) {
                    tooltipInstance.dispose(); // Remove tooltip if expanded
                }
            }
        });
    }

    // Sidebar Toggle Logic
    toggleBtn.addEventListener("click", function () {
        if (sidebar.style.width === "250px") {
            sidebar.style.width = "80px";
            mainContent.style.marginLeft = "80px";
            menuText.forEach(text => text.style.display = "none");
        } else {
            sidebar.style.width = "250px";
            mainContent.style.marginLeft = "250px";
            menuText.forEach(text => text.style.display = "inline");
        }
        updateTooltips(); // Call function to update tooltips
    });

    // Initialize tooltips when page loads (if sidebar is already collapsed)
    updateTooltips();
});


// For subjects Edit
document.addEventListener("DOMContentLoaded", function () {
    const editButtons = document.querySelectorAll(".editSubjectBtn");

    editButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Get data from the clicked button to send it to form.
            const id = this.getAttribute("editSubjectId");
            const Name = this.getAttribute("editSubjectName");
            const Desc = this.getAttribute("editSubjectDesc");

            // Set modal form values so that admin can see previous values
            document.getElementById("editSubjectId").value = id;
            document.getElementById("editSubjectName").value = Name;
            document.getElementById("editSubjectDesc").value = Desc;
        });
    });
});

// For add chapter
document.addEventListener("DOMContentLoaded", function () {
    const editButtons = document.querySelectorAll(".addChapterBtn");

    editButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Get data from the clicked button to send it to form.
            const subjectId = this.getAttribute("subjectId");
            const subjectName = this.getAttribute("subjectName");

            // Set modal form values so that admin can see previous values
            document.getElementById("subjectId").value = subjectId;
            document.getElementById("subjectName").textContent = subjectName;
        });
    });
});

// for chapters edit
document.addEventListener("DOMContentLoaded", function () {
    const editButtons = document.querySelectorAll(".editChapterBtn");

    editButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Get data from the clicked button to send it to form.
            const id = this.getAttribute("chapterId");
            const Name = this.getAttribute("chapterName");
            const Desc = this.getAttribute("chapterDesc");
            const subjectName = this.getAttribute("editSubName");

            // Set modal form values so that admin can see previous values
            document.getElementById("chapterId").value = id;
            document.getElementById("editChapterName").value = Name;
            document.getElementById("editChapterDesc").value = Desc;
            document.getElementById("editSubName").textContent = subjectName;
        });
    });
});

// for quizzes edit
document.addEventListener("DOMContentLoaded", function () {
    const editButtons = document.querySelectorAll(".editQuizBtn");

    editButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Get data from the clicked button to send it to form.
            const id = this.getAttribute("editQuizId");
            const Name = this.getAttribute("editQuizName");
            const Date = this.getAttribute("editQuizDate");
            const Duration = this.getAttribute("editQuizDuration");
            const Desc = this.getAttribute("editQuizDesc");

            // Set modal form values so that admin can see previous values
            document.getElementById("editQuizId").value = id;
            document.getElementById("editQuizName").value = Name;
            document.getElementById("editQuizDate").value = Date;
            document.getElementById("editQuizDuration").value = Duration;
            document.getElementById("editQuizDesc").value = Desc;
        });
    });
});

// For add Question
document.addEventListener("DOMContentLoaded", function () {
    const editButtons = document.querySelectorAll(".addQuesBtn");

    editButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Get data from the clicked button to send it to form.
            const quizId = this.getAttribute("quizId");
            const quizName = this.getAttribute("quizName");

            // Set modal form values so that admin can see previous values
            document.getElementById("quizId").value = quizId;
            document.getElementById("quizName").textContent = quizName;
        });
    });
});

// for Questions edit
document.addEventListener("DOMContentLoaded", function () {
    const editButtons = document.querySelectorAll(".editQuesBtn");

    editButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Get data from the clicked button to send it to form.
            const Id = this.getAttribute("editQuesId");
            const QuizName = this.getAttribute("editQuesQuizName");
            const Title = this.getAttribute("editTitle");
            const Statement = this.getAttribute("editStatement");
            const Option1 = this.getAttribute("editOption1");
            const Option2 = this.getAttribute("editOption2");
            const Option3 = this.getAttribute("editOption3");
            const Option4 = this.getAttribute("editOption4");
            const CorrectOption = this.getAttribute("editCorrectOption");
            console.log("edit SubjectName:", QuizName);
            console.log(document.getElementById("editQuizName"));

            // Set modal form values so that admin can see previous values
            document.getElementById("editQuesId").value = Id;
            document.getElementById("editQuesQuizName").textContent = QuizName;
            document.getElementById("editTitle").value = Title;
            document.getElementById("editStatement").value = Statement;
            document.getElementById("editOption1").value = Option1;
            document.getElementById("editOption2").value = Option2;
            document.getElementById("editOption3").value = Option3;
            document.getElementById("editOption4").value = Option4;
            document.getElementById("editCorrectOption").value = CorrectOption;
        });
    });
});

// For viewing quiz
document.addEventListener("DOMContentLoaded", function () {
    const viewButtons = document.querySelectorAll(".viewQuizBtn");

    viewButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Get data attributes from button
            const quizName = this.getAttribute("quizName");
            const quizChap = this.getAttribute("quizChap");
            const quizSub = this.getAttribute("quizSub");
            const quesLen = this.getAttribute("quesLen");
            const quizDate = this.getAttribute("quizDate");
            const quizDuration = this.getAttribute("quizDuration");
            const quizDesc = this.getAttribute("quizDesc");

            // Update modal with quiz details
            document.getElementById("quizName").textContent = quizName;
            document.getElementById("quizSub").textContent = quizSub;
            document.getElementById("quizChap").textContent = quizChap;
            document.getElementById("quesLen").textContent = quesLen;
            document.getElementById("quizDate").textContent = quizDate;
            document.getElementById("quizDuration").textContent = quizDuration;
            document.getElementById("quizDesc").textContent = quizDesc;
        });
    });
});


// For attempting Quiz
document.addEventListener("DOMContentLoaded", function () {
    const attemptButtons = document.querySelectorAll(".attemptQuizBtn");

    attemptButtons.forEach(button => {
        button.addEventListener("click", function () {
            // Get quiz ID from the clicked button
            const quizId = this.getAttribute("data-quiz-id");
            // Store quiz ID in a hidden input field inside the modal (optional)
            document.getElementById("quizId").value = quizId;
            // Set a global variable (or update UI if needed)
            document.getElementById("quizIdDisplay").textContent = quizId;
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    let totalMinutes = parseInt(document.getElementById("duration-pill").dataset.duration);
    let totalSeconds = totalMinutes * 60;
    let remainingSeconds = totalSeconds;
    let warningShown = false;

    function updateTimer() {
        if (remainingSeconds <= 0) {
            clearInterval(timerInterval);
            alert("Time's up! Submitting your quiz...");
            document.getElementById("quizAttemptform").submit();
            return;
        }

        let minutes = Math.floor(remainingSeconds / 60);
        let seconds = remainingSeconds % 60;
        document.getElementById("duration-pill").innerText = minutes + ":" + (seconds < 10 ? "0" : "") + seconds;

        //  Update Progress Bar with time
        let progressPercent = ((totalSeconds - remainingSeconds) / totalSeconds) * 100;
        let progressBar = document.getElementById("progress-bar");
        progressBar.style.width = progressPercent + "%";

        //  Change Colors Based on Time Left
        let durationPill = document.getElementById("duration-pill");
        if (progressPercent < 50) {
            progressBar.className = "progress-bar progress-bar-striped bg-success";
            durationPill.className = "badge bg-success text-white rounded-pill px-4 py-2 fs-5";
        } else if (progressPercent < 75) {
            progressBar.className = "progress-bar progress-bar-striped bg-warning";
            durationPill.className = "badge bg-warning text-dark rounded-pill px-4 py-2 fs-5";
        } else {
            progressBar.className = "progress-bar progress-bar-striped bg-danger";
            durationPill.className = "badge bg-danger text-white rounded-pill px-4 py-2 fs-5";
        }

        //  Show Warning at 1 Minute Left
        if (remainingSeconds === 60 && !warningShown) {
            alert("⚠️ Warning! Only 1 minute left.");
            warningShown = true;
        }

        remainingSeconds--;
    }

    let timerInterval = setInterval(updateTimer, 1000);
});

// Function to generate admin Summary  charts
function generateCharts(userAttemptsData, avgScoresData) {
    // Extract Labels & Values
    const subjects = Object.keys(userAttemptsData);
    const userCounts = Object.values(userAttemptsData);
    const avgScores = Object.values(avgScoresData);

    // Users Attempted Chart
    const userAttemptsCtx = document.getElementById('userAttemptsChart').getContext('2d');
    new Chart(userAttemptsCtx, {
        type: 'bar',
        data: {
            labels: subjects,
            datasets: [{
                label: 'Users Attempted',
                data: userCounts,
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });

    // Average Score Chart
    const avgScoreCtx = document.getElementById('avgScoreChart').getContext('2d');
    new Chart(avgScoreCtx, {
        type: 'bar',
        data: {
            labels: subjects,
            datasets: [{
                label: 'Average Score',
                data: avgScores,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
}

