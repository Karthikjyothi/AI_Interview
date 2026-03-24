import React, { useEffect, useRef, useState } from "react";
import { FaceMesh } from "@mediapipe/face_mesh";
import { Camera } from "@mediapipe/camera_utils";
import { motion } from "framer-motion";
import "./App.css";

function App() {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [score, setScore] = useState(0);
  const [mode, setMode] = useState("hr");
  const [messages, setMessages] = useState([]);
  const [time, setTime] = useState(0);
  const [resumeText, setResumeText] = useState("");

  const ws = useRef(null);
  const videoRef = useRef(null);

  // ⏱️ Timer
  useEffect(() => {
    const interval = setInterval(() => {
      setTime(prev => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // 🔌 WebSocket
  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/ws/user1");

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setScore(data.cheating_score);
    };
  }, []);

  // 🚨 Tab switch
  useEffect(() => {
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        ws.current.send(JSON.stringify({ event: "TAB_SWITCH" }));
      }
    });
  }, []);

  // 🎥 MediaPipe (same logic — untouched)
  useEffect(() => {

    const faceMesh = new FaceMesh({
      locateFile: (file) =>
        `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
    });

    faceMesh.setOptions({
      maxNumFaces: 2,
      refineLandmarks: true,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    });

    let lookAwayCount = 0;
    let noFaceCount = 0;

    let lastEventTime = {
      LOOK_AWAY: 0,
      NO_FACE: 0,
      MULTIPLE_FACES: 0
    };

    const COOLDOWN = 5000;

    function sendEvent(eventName) {
      const now = Date.now();
      if (now - lastEventTime[eventName] > COOLDOWN) {
        ws.current.send(JSON.stringify({ event: eventName }));
        lastEventTime[eventName] = now;
      }
    }

    faceMesh.onResults((results) => {

      if (!results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) {
        noFaceCount++;
        if (noFaceCount > 40) {
          sendEvent("NO_FACE");
          noFaceCount = 0;
        }
        return;
      } else {
        noFaceCount = 0;
      }

      if (results.multiFaceLandmarks.length > 1) {
        sendEvent("MULTIPLE_FACES");
      }

      const landmarks = results.multiFaceLandmarks[0];
      const leftEye = landmarks[33];
      const rightEye = landmarks[263];
      const nose = landmarks[1];

      let center = (leftEye.x + rightEye.x) / 2;

      if (Math.abs(nose.x - center) > 0.12) {
        lookAwayCount++;
        if (lookAwayCount > 25) {
          sendEvent("LOOK_AWAY");
          lookAwayCount = 0;
        }
      } else {
        lookAwayCount = 0;
      }

      if (nose.y > 0.85) {
        sendEvent("LOOK_AWAY");
      }
    });

    const camera = new Camera(videoRef.current, {
      onFrame: async () => {
        await faceMesh.send({ image: videoRef.current });
      },
      width: 300,
      height: 200
    });

    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        videoRef.current.srcObject = stream;
        camera.start();
      });

  }, []);

  // 🎯 Interview logic
  const startInterview = async () => {
    const res = await fetch("http://localhost:8000/start?name=Karthik", {
      method: "POST"
    });
    const data = await res.json();

    setMessages([{ role: "ai", text: data.question }]);
    setQuestion(data.question);
  };

  const submitAnswer = async () => {

    const res = await fetch("http://localhost:8000/next-question", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        answer,
        job_description: "Software Engineer",
        resume_highlights: resumeText, 
        mode
      })
    });

    const data = await res.json();

    setMessages(prev => [
      ...prev,
      { role: "user", text: answer },
      { role: "ai", text: data.next_question }
    ]);

    setFeedback(data.feedback.feedback);
    setQuestion(data.next_question);
    setAnswer("");
  };

  return (
    <div className="dark-container">

      {/* Top Bar */}
      <div className="top-bar">
        <h2>🤖 AI Interview</h2>
        <div>⏱ {time}s</div>
        <div className="score">🚨 {score}</div>
      </div>

      {/* Progress */}
      <div className="progress-bar">
        <div style={{ width: `${Math.min(score * 5, 100)}%` }} />
      </div>

      {/* Main */}
      <div className="main">

        {/* Chat */}
        <div className="chat-box">
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={msg.role === "ai" ? "ai-msg" : "user-msg"}
            >
              {msg.text}
            </motion.div>
          ))}
        </div>

        {/* Side Panel */}
        <div className="side-panel">
          <select onChange={(e) => setMode(e.target.value)}>
            <option value="hr">HR</option>
            <option value="technical">Technical</option>
          </select>

          <button onClick={startInterview}>Start</button>

          <video ref={videoRef} autoPlay />
        </div>

      </div>
      <input
  type="file"
  accept=".txt"
  onChange={(e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = (e) => {
      setResumeText(e.target.result);
    };

    reader.readAsText(file);
  }}
/>

      {/* Input */}
      <div className="input-box">
        <input
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Type your answer..."
        />
        <button onClick={submitAnswer}>Send</button>
      </div>

      {/* Feedback */}
      <div className="feedback">{feedback}</div>

    </div>
    
  );
}

export default App;