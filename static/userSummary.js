document.addEventListener("DOMContentLoaded", function () {
    if (typeof Chart === 'undefined') {
        console.error("Chart.js not loaded properly!");
        return;
    }

    generateUserCharts(quizzesAttemptedData, avgScoresData);
});

function generateUserCharts(quizzesAttemptedData, avgScoresData) {
    const subjects = Object.keys(quizzesAttemptedData);
    const quizCounts = Object.values(quizzesAttemptedData);
    const avgScores = Object.values(avgScoresData);

    console.log("Subjects:", subjects);
    console.log("Quiz Counts:", quizCounts);
    console.log("Avg Scores:", avgScores);

    // Ensure the canvas elements exist
    const quizzesAttemptedCanvas = document.getElementById('quizzesAttemptedChart');
    const avgScoreCanvas = document.getElementById('avgScoreChart');

    if (!quizzesAttemptedCanvas || !avgScoreCanvas) {
        console.error("Canvas elements not found!");
        return;
    }

    // Quizzes Attempted Chart
    const quizzesAttemptedCtx = quizzesAttemptedCanvas.getContext('2d');
    new Chart(quizzesAttemptedCtx, {
        type: 'bar',
        data: {
            labels: subjects,
            datasets: [{
                label: 'Quizzes Attempted',
                data: quizCounts,
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });

    // Average Score Chart
    const avgScoreCtx = avgScoreCanvas.getContext('2d');
    new Chart(avgScoreCtx, {
        type: 'bar',
        data: {
            labels: subjects,
            datasets: [{
                label: 'Average Score',
                data: avgScores,
                backgroundColor: 'rgba(255, 159, 64, 0.5)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } }
        }
    });
}
