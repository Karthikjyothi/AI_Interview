import streamlit.components.v1 as components


def start_camera_monitor():
    """
    Force webcam access and display camera feed
    """

    components.html(
        """
        <div style="position:fixed; bottom:10px; right:10px; z-index:9999;">
            <h4>🔒 Proctoring Camera Active</h4>
            <video id="video" width="320" height="240" autoplay muted></video>
        </div>

        <script>
        async function startCamera() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: true,
                    audio: false
                });

                const video = document.getElementById("video");
                video.srcObject = stream;

            } catch (error) {

                alert("⚠️ Camera access is required for this interview. Please enable your webcam.");

            }
        }

        startCamera();
        </script>
        """,
        height=300,
    )