document.addEventListener("DOMContentLoaded", function () {

    // COPY BUTTON

    const copyBtn =
        document.getElementById("copy-btn");

    copyBtn.addEventListener("click", function () {

        const translatedText =
            document.getElementById("translated-text").innerText;

        if (translatedText.trim() === "") {

            alert("No translated text!");

            return;
        }

        navigator.clipboard.writeText(translatedText);

        copyBtn.innerText = "✅ Copied";

        setTimeout(function () {

            copyBtn.innerText = "📋 Copy";

        }, 2000);

    });




    // SPEECH TO TEXT

    const micBtn =
        document.getElementById("mic-btn");

    micBtn.addEventListener("click", function () {

        try {

            const SpeechRecognition =
                window.SpeechRecognition ||
                window.webkitSpeechRecognition;

            if (!SpeechRecognition) {

                alert("Speech Recognition not supported");

                return;
            }

            const recognition =
                new SpeechRecognition();

            recognition.lang = "en-US";

            recognition.interimResults = false;

            recognition.maxAlternatives = 1;

            recognition.start();

            recognition.onstart = function () {

                micBtn.innerText =
                    "🎙 Listening...";

            };

            recognition.onend = function () {

                micBtn.innerText =
                    "🎤 Voice Input";

            };

            recognition.onresult = function (event) {

                const transcript =
                    event.results[0][0].transcript;

                document.getElementById("input-text").value =
                    transcript;

            };

            recognition.onerror = function (event) {

                alert("Error: " + event.error);

            };

        }

        catch (error) {

            alert("Speech feature not supported");

        }

    });




    // LANGUAGE SWAP

    const swapBtn =
        document.getElementById("swap-btn");

    swapBtn.addEventListener("click", function () {

        const selects =
            document.querySelectorAll("select");

        const temp =
            selects[0].value;

        selects[0].value =
            selects[1].value;

        selects[1].value =
            temp;

    });

});