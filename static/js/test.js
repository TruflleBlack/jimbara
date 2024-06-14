document.addEventListener('DOMContentLoaded', function() {
    const totalQuestions = 42; // Sesuaikan dengan jumlah total pertanyaan Anda
    let currentQuestion = 1;

    let answers = {};  // Objek untuk menyimpan jawaban

    function showQuestion(questionId) {
        const questions = document.querySelectorAll('.question');
        questions.forEach(question => {
            question.classList.add('hide');
        });

        // Gunakan requestAnimationFrame untuk animasi yang lebih smooth
        requestAnimationFrame(() => {
            setTimeout(() => {
                questions.forEach(question => {
                    question.classList.remove('show');
                    question.classList.remove('hide');
                });

                const nextQuestion = document.getElementById('question' + questionId);
                if (nextQuestion) {
                    nextQuestion.classList.add('show');
                }
            }, 300); // Waktu tunggu dikurangi
        });
    }

    function nextQuestion() {
        let currentQuestion = document.querySelector('.question.show');
        if (currentQuestion) {
            let currentId = parseInt(currentQuestion.id.replace('question', ''));
            let nextId = currentId + 1;
            let nextQuestion = document.getElementById('question' + nextId);
            if (nextQuestion) {
                showQuestion(nextId);
            }
        }
    }

    function previousQuestion() {
        let currentQuestion = document.querySelector('.question.show');
        if (currentQuestion) {
            let currentId = parseInt(currentQuestion.id.replace('question', ''));
            let prevId = currentId - 1;
            let prevQuestion = document.getElementById('question' + prevId);
            if (prevQuestion) {
                showQuestion(prevId);
            }
        }
    }

    function selectOption(questionId, option) {
        answers[questionId] = option;  // Simpan jawaban
        document.getElementById('DASS' + questionId).value = option;
        if (questionId < totalQuestions) {
            nextQuestion();
        } else {
            document.getElementById('testForm').submit();
        }
    }

    window.selectOption = selectOption; // Membuat fungsi global agar dapat diakses di HTML

    // Inisialisasi tampilan pertanyaan pertama
    showQuestion(1);
});
