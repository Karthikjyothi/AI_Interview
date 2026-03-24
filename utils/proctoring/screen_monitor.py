import streamlit as st
import streamlit.components.v1 as components


def start_screen_monitor():

    if "cheating_score" not in st.session_state:
        st.session_state["cheating_score"] = 0

    components.html(
        """
        <div style="position:fixed; top:10px; left:10px; z-index:9999;">
            <button id="startShare">Start Screen Sharing</button>
            <video id="screenVideo" width="300" height="200" autoplay muted></video>
        </div>

        <script>

        let mediaRecorder;
        let recordedChunks = [];

        const video = document.getElementById("screenVideo");

        document.getElementById("startShare").onclick = async () => {

            try {

                const stream = await navigator.mediaDevices.getDisplayMedia({
                    video: true,
                    audio: true
                });

                video.srcObject = stream;

                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = function(e) {
                    if (e.data.size > 0) {
                        recordedChunks.push(e.data);
                    }
                };

                mediaRecorder.onstop = function() {

                    const blob = new Blob(recordedChunks, { type: 'video/webm' });

                    const url = URL.createObjectURL(blob);

                    const a = document.createElement("a");
                    a.href = url;
                    a.download = "screen_recording.webm";
                    a.click();

                    alert("✅ Recording downloaded. Please upload it below to complete the interview.");
                };

                mediaRecorder.start();

                // Detect stop sharing
                stream.getVideoTracks()[0].addEventListener("ended", () => {

                    alert("⚠️ Screen sharing stopped!");

                });

            } catch(err) {

                alert("Screen sharing required!");

            }

        };

        </script>
        """,
        height=0
    )

    # 👇 Upload recording manually
    st.markdown("### 📤 Upload Screen Recording (Required)")

    uploaded_file = st.file_uploader("Upload your screen recording", type=["webm"])

    if uploaded_file:

        import os

        name = st.session_state.get("name", "candidate")

        os.makedirs("recordings", exist_ok=True)

        file_path = f"recordings/{name}_screen.webm"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"Recording saved: {file_path}")