import streamlit.components.v1 as components


def start_advanced_proctoring():

    components.html(
        """
        <div style="position:fixed; bottom:10px; right:10px; z-index:9999;">
            <video id="video" width="260" height="200" autoplay muted></video>
            <canvas id="canvas" width="260" height="200"></canvas>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/face_mesh.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>

        <script>

        const video = document.getElementById("video");
        const canvas = document.getElementById("canvas");
        const ctx = canvas.getContext("2d");

        let violations = {
            lookAway: 0,
            noFace: 0,
            multipleFaces: 0,
            blinking: 0
        };

        let cheatingScore = 0;

        function alertUser(msg){
            console.log(msg);
            alert(msg);
        }

        const faceMesh = new FaceMesh({
            locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
        });

        faceMesh.setOptions({
            maxNumFaces: 2,
            refineLandmarks: true,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        faceMesh.onResults(results => {

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (!results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) {
                violations.noFace++;

                if(violations.noFace > 30){
                    alertUser("⚠️ Face not detected!");
                    cheatingScore += 2;
                    violations.noFace = 0;
                }
                return;
            }

            if(results.multiFaceLandmarks.length > 1){
                violations.multipleFaces++;

                if(violations.multipleFaces > 20){
                    alertUser("⚠️ Multiple people detected!");
                    cheatingScore += 3;
                    violations.multipleFaces = 0;
                }
            }

            const landmarks = results.multiFaceLandmarks[0];

            // Eye + Nose points
            const leftEye = landmarks[33];
            const rightEye = landmarks[263];
            const nose = landmarks[1];

            // ===== HEAD ROTATION (LEFT/RIGHT) =====
            let faceCenter = (leftEye.x + rightEye.x) / 2;

            if(Math.abs(nose.x - faceCenter) > 0.08){
                violations.lookAway++;

                if(violations.lookAway > 15){
                    alertUser("⚠️ Looking away from screen!");
                    cheatingScore += 1;
                    violations.lookAway = 0;
                }
            }

            // ===== BLINK DETECTION =====
            const eyeTop = landmarks[159];
            const eyeBottom = landmarks[145];

            let eyeDistance = Math.abs(eyeTop.y - eyeBottom.y);

            if(eyeDistance < 0.01){
                violations.blinking++;

                if(violations.blinking > 10){
                    alertUser("⚠️ Excessive blinking detected!");
                    cheatingScore += 1;
                    violations.blinking = 0;
                }
            }

            // ===== PHONE USAGE (approximation) =====
            if(nose.y > 0.7){
                alertUser("⚠️ Looking down (possible phone usage)");
                cheatingScore += 2;
            }

            // ===== DRAW CAMERA =====
            ctx.drawImage(results.image, 0, 0, canvas.width, canvas.height);

            // ===== DISPLAY SCORE =====
            ctx.fillStyle = "red";
            ctx.font = "14px Arial";
            ctx.fillText("Cheating Score: " + cheatingScore, 10, 20);

        });

        const camera = new Camera(video, {
            onFrame: async () => {
                await faceMesh.send({image: video});
            },
            width: 260,
            height: 200
        });

        navigator.mediaDevices.getUserMedia({video:true})
        .then(stream => {
            video.srcObject = stream;
            camera.start();
        })
        .catch(err => {
            alert("Camera is required!");
        });

        </script>
        """,
        height=0
    )