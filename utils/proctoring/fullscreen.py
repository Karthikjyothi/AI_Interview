import streamlit.components.v1 as components


def start_fullscreen():
    components.html(
        """
        <div style="text-align:center;margin:20px;">
            <button id="fullscreenBtn"
                style="
                padding:12px 20px;
                font-size:16px;
                background:#e63946;
                color:white;
                border:none;
                border-radius:8px;
                cursor:pointer;">
                🔒 Start Secure Interview (Fullscreen)
            </button>
        </div>

        <script>

        const btn = document.getElementById("fullscreenBtn");

        btn.addEventListener("click", async () => {

            try {

                const elem = document.body;

                if (elem.requestFullscreen) {
                    await elem.requestFullscreen();
                }

            } catch (err) {

                alert("Fullscreen could not be started: " + err);

            }

        });


        // Detect fullscreen exit
        document.addEventListener("fullscreenchange", () => {

            if (!document.fullscreenElement) {

                alert("⚠️ Fullscreen is required during the interview.");

            }

        });


        // Detect tab switching
        document.addEventListener("visibilitychange", () => {

            if (document.hidden) {

                alert("⚠️ Tab switching detected!");

            }

        });


        // Detect window blur
        window.addEventListener("blur", () => {

            alert("⚠️ Window focus lost!");

        });

        </script>
        """,
        height=120,
    )