import streamlit.components.v1 as components


def start_gaze_monitor():

    components.html(
        """
        <div style="position:fixed; bottom:10px; right:10px; z-index:9999;">
            <video id="video" width="240" height="180" autoplay muted></video>
            <canvas id="canvas" width="240" height="180"></canvas>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js"></script>

        <script>

        const videoElement = document.getElementById('video');
        const canvasElement = document.getElementById('canvas');
        const canvasCtx = canvasElement.getContext('2d');

        let lookAwayCount = 0;

        const faceMesh = new FaceMesh({
            locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`;
            }
        });

        faceMesh.setOptions({
            maxNumFaces: 1,
            refineLandmarks: true,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        faceMesh.onResults(results => {

            canvasCtx.save();
            canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
            canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

            if(results.multiFaceLandmarks && results.multiFaceLandmarks.length > 0){

                const landmarks = results.multiFaceLandmarks[0];

                const leftEye = landmarks[33];
                const rightEye = landmarks[263];
                const nose = landmarks[1];

                let faceCenter = (leftEye.x + rightEye.x)/2;

                if(Math.abs(nose.x - faceCenter) > 0.08){

                    lookAwayCount++;

                    if(lookAwayCount > 20){
                        alert("⚠️ Please look at the screen during the interview.");
                        lookAwayCount = 0;
                    }

                }

            }

            canvasCtx.restore();

        });

        const camera = new Camera(videoElement, {
            onFrame: async () => {
                await faceMesh.send({image: videoElement});
            },
            width: 240,
            height: 180
        });

        navigator.mediaDevices.getUserMedia({video:true})
        .then(stream => {
            videoElement.srcObject = stream;
            camera.start();
        })
        .catch(err => {
            alert("Camera access required for interview monitoring.");
        });

        </script>
        """,
        height=0
    )