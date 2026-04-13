import React, { useState, useEffect, useRef } from "react";
import { FaceMesh } from "@mediapipe/face_mesh";
import { Camera } from "@mediapipe/camera_utils";
/* eslint-disable-next-line no-unused-vars */ import { motion } from "framer-motion";
import "../App.css";
import Editor from "@monaco-editor/react";


function Interview() {

  // ✅ STATES
  const [resumeText, setResumeText] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [score, setScore] = useState(0);
  const [mode, setMode] = useState("hr");
  const [totalQuestions, setTotalQuestions] = useState(5);
  const [messages, setMessages] = useState([]);
  const [time, setTime] = useState(0);
  const [questionType, setQuestionType] = useState("hr");
  const [code, setCode] = useState("");
  const [codingScore, setCodingScore] = useState(0);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [interviewEnded, setInterviewEnded] = useState(false);
  const [language, setLanguage] = useState("python");
  const [codeOutput, setCodeOutput] = useState(""); // To display run results
  const [name, setName] = useState("");
  const isListeningRef = useRef(false);
  const recognitionRef = useRef(null);
  
  const ws = useRef(null);
  const videoRef = useRef(null);
  

  // ⏱️ Timer
  useEffect(() => {
    const interval = setInterval(() => {
      setTime(prev => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);
  
  // Auto-hide AI feedback after 6 seconds
  useEffect(() => {
    if (feedback) {
      const timer = setTimeout(() => {
        setFeedback("");
      }, 6000);
      return () => clearTimeout(timer);
    }
  }, [feedback]);

  // 🔌 WebSocket
  useEffect(() => {
    let socket;
    
    const connect = () => {
      socket = new WebSocket("ws://localhost:8000/ws/user1");
      socket.onopen = () => console.log("Connected!");
      
      socket.onclose = () => {
        console.log("Disconnected! Retrying in 3 seconds...");
        setTimeout(connect, 3000); // 🔄 Auto-reconnect logic                                  
      };

      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setScore(data.cheating_score);
      };

      ws.current = socket;
    };

    connect();
    return () => socket.close();
  }, []);

  // 🚨 Safer Tab switch logic
  useEffect(() => {
    const handleVisibility = () => {
      if (document.hidden && ws.current && ws.current.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ event: "TAB_SWITCH" }));
      }
    };

    document.addEventListener("visibilitychange", handleVisibility);
    return () => document.removeEventListener("visibilitychange", handleVisibility);
  }, []);

  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition not supported");
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = true;

    recognitionRef.current = recognition;

    recognition.onresult = (event) => {
      let finalTranscript = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript;
        }
      }

      if (finalTranscript) {
        setAnswer(prev => prev + " " + finalTranscript);
      }
    };

    recognition.onerror = (e) => {
      console.error("Speech error:", e);
      setIsListening(false);
      isListeningRef.current = false;
    };

    recognition.onend = () => {
      if (isListeningRef.current) {
        try {
          recognition.start(); // 🔥 restart automatically
        } catch (e) {
          console.log("Restart blocked");
        }
      }
    };

  }, []);

  // 🎥 MediaPipe
  useEffect(() => {

  if (!videoRef.current) return; // 🔥 FIX 1

  const faceMesh = new FaceMesh({
    locateFile: (file) => {
      // Force a specific version to match the library
      return `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh@0.4/${file}`;
    },
  });

  faceMesh.setOptions({
    maxNumFaces: 1,
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
    if (ws.current && now - lastEventTime[eventName] > COOLDOWN) {
      ws.current.send(JSON.stringify({ event: eventName }));
      lastEventTime[eventName] = now;
    }
  }

  faceMesh.onResults((results) => {

    // 🛡️ SAFETY CHECK: If no face is detected, exit the function immediately
    if (!results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) {
      noFaceCount++;
      if (noFaceCount > 40) {
        sendEvent("NO_FACE");
        noFaceCount = 0;
      }
      return; // Stop execution here
    }

    const landmarks = results.multiFaceLandmarks[0];
    
    // 🔥 Double-check that landmarks exists before accessing indices
    if (!landmarks) return;

    const leftEye = landmarks[33];
    const rightEye = landmarks[263];
    const nose = landmarks[1];

    // Ensure nose and eyes exist before doing math
    if (!leftEye || !rightEye || !nose) return;

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

  // 🔥 FIX 2 — wait for camera properly
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {

      if (!videoRef.current) return;

      videoRef.current.srcObject = stream;

      const camera = new Camera(videoRef.current, {
        onFrame: async () => {
          if (videoRef.current) {
            await faceMesh.send({ image: videoRef.current });
          }
        },
        width: 300,
        height: 200
      });

      camera.start();
    })
    .catch(err => {
      console.error("Camera error:", err);
    });

}, []);

  // 📄 Resume Upload (✅ FIXED LOCATION)
  const uploadResume = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/upload-resume", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    setResumeText(data.resume_text);
  };

  // 🎯 Interview Start
  const startInterview = async () => {
    const res = await fetch(`http://localhost:8000/start?name=${name}`, {
  method: "POST"
})

    const data = await res.json();

    setMessages([{ role: "ai", text: data.question }]);
    setQuestion(data.question);
    speakQuestion(data.question);
  };
  // 🎯 Submit Answer
  const submitAnswer = async () => {
    if (questionType === "coding") return;
    if (answer.trim().length < 5) {
      alert("Please give a proper answer");
      return;
    }
    
    const res = await fetch("http://localhost:8000/next-question", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        answer,
        job_description: mode === "technical" ? "Technical Specialist" : "HR Manager", // 🔥 Dynamic Role
        resume_highlights: resumeText.slice(0, 3000),
        mode,
        name,
        total_questions: totalQuestions
      })
    });

    const data = await res.json();

    // 🎯 SMART PARSER: Extract real score and clean feedback string
    let displayFeedback = ""; 
    if (data.feedback && typeof data.feedback === 'object') {
        const numericScore = parseInt(data.feedback.score) || 0;
        setScore(prev => prev + numericScore); 
        displayFeedback = data.feedback.feedback || "Answer received.";
    } else {
        displayFeedback = data.feedback || "Answer received.";
    }

    setMessages(prev => [
      ...prev,
      ...(answer ? [{ role: "user", text: answer }] : []),
      { role: "ai", text: data.next_question }
    ]);

    setFeedback(displayFeedback); // ✅ FIXED: Uses 'displayFeedback' instead of undefined variable

    if (data.type === "end") {
      setInterviewEnded(true);
    } else {
      setQuestion(data.next_question);
    }
    speakQuestion(data.next_question);
    setQuestionType(data.type);
    setAnswer("");

    if (data.type === "end") {
      setInterviewEnded(true);
    } else {
      setQuestion(data.next_question);
    }
    speakQuestion(data.next_question);
    setQuestionType(data.type);
    setAnswer("");
  };

  const runCode = async () => {
    setCodeOutput("Compiling and Running...");
    try {
      const response = await fetch("http://localhost:8000/run-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, language })
      });
      const data = await response.json();
      
      // Use the 'output' field from our new Piston logic
      setCodeOutput(data.output || data.stderr || "No output.");
    } catch (error) {
      setCodeOutput("Error connecting to Piston engine.");
    }
  };

  const speakQuestion = (text) => {
    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";

    speech.onstart = () => setIsSpeaking(true);
    speech.onend = () => setIsSpeaking(false);

    window.speechSynthesis.speak(speech);
    };
  
  const submitCode = async () => {
    const res = await fetch("http://localhost:8000/evaluate-code", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code })
    });

    const data = await res.json();
    setCodingScore(data.score);
    
    setMessages(prev => [
      ...prev,
      { role: "ai", text: `💻 Coding Round Evaluation: ${data.score}/10. Great job!` }
    ]);

    // 🔥 THIS LINE ENDS THE INTERVIEW
    setInterviewEnded(true); 
    setQuestionType("end");
  };

  const startListening = () => {
    if (!recognitionRef.current) return;

    try {
      recognitionRef.current.start();
      setIsListening(true);
      isListeningRef.current = true;
    } catch (err) {
      console.log("Already listening...");
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
      isListeningRef.current = false;
    }
  };
  const chatBoxStyle = {
  flex: 1,
  background: "#020617",
  padding: "20px",
  overflowY: "auto",
  borderRadius: "10px",
  display: "flex",
  flexDirection: "column"
};
const avatarStyle = {
  width: "80px",
  height: "80px",
  borderRadius: "50%",
  background: "#1e293b",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  fontSize: "40px",
  animation: isSpeaking ? "talk 0.6s infinite" : "pulse 1.5s infinite",
  boxShadow: "0 0 20px rgba(79,70,229,0.5)"
};
// 🔥 ADVANCED DOWNLOAD LOGIC
  const downloadReport = async () => {
    try {
      const response = await fetch("http://localhost:8000/download-report", {
        method: 'GET',
      });

      if (!response.ok) throw new Error("Download failed");

      // Convert the response to a Blob (Binary Large Object)
      const blob = await response.blob();
      
      // Create a temporary local URL for the PDF
      const url = window.URL.createObjectURL(blob);
      
      // Create a hidden anchor element to trigger the download
      const link = document.createElement('a');
      link.href = url;
      
      // Name the file dynamically based on the candidate's name
      link.setAttribute('download', `Interview_Report_${name || 'Candidate'}.pdf`);
      
      document.body.appendChild(link);
      link.click();
      
      // Cleanup: remove the link and revoke the URL
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error("PDF Download Error:", error);
      alert("Could not download the report. Make sure the interview is finished!");
    }
  };


  return (
    <div className="dark-container" style={{ display: "flex", flexDirection: "column", height: "100vh", backgroundColor: "#020617", color: "white", overflow: "hidden" }}>
      
      {/* --- HEADER (Kept Exactly as is) --- */}
      <div style={{ display: "flex", justifyContent: "space-between", padding: "15px 20px", borderBottom: "1px solid #1e293b", background: "#0f172a" }}>
        <h2>🤖 AI Interview</h2>
        <div style={{ display: "flex", gap: "20px", alignItems: "center" }}>
          <div>⏱ {time}s</div>
          <div className="score">🚨 {score}</div>
        </div>
      </div>

      <div className="progress-bar">
        <div style={{ width: `${Math.min(score * 5, 100)}%` }} />
      </div>

      {/* --- MAIN CONTENT AREA (The Fix) --- */}
      {/* --- MAIN CONTENT AREA --- */}
      <div style={{ display: "flex", flex: 1, overflow: "hidden", position: "relative" }}>
        
        {/* 🔔 FLOATING FEEDBACK NOTIFICATION (Top Right of Chat Area) */}
        {feedback && (
          <div style={{ 
            position: "absolute", 
            top: "20px", 
            right: "370px", // Sits just to the left of the sidebar
            zIndex: 100, 
            width: "300px", 
            background: "rgba(30, 41, 59, 0.95)", 
            backdropFilter: "blur(10px)",
            padding: "15px", 
            borderRadius: "12px", 
            border: "1px solid #4f46e5",
            boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)",
            animation: "slideIn 0.3s ease-out"
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "5px" }}>
              <strong style={{ color: "#818cf8" }}>AI Evaluation</strong>
              <button onClick={() => setFeedback("")} style={{ background: "none", border: "none", color: "#94a3b8", cursor: "pointer" }}>✕</button>
            </div>
            <p style={{ fontSize: "13px", margin: 0, color: "#cbd5e1", lineHeight: "1.4" }}>
              {typeof feedback === 'string' ? feedback : "Evaluation received."}
            </p>
          </div>
        )}
        
        {/* CENTER COLUMN: Chat & Editor */}
        <div style={{ flex: 1, display: "flex", flexDirection: "column", padding: "20px", overflowY: "auto", position: "relative" }}>
          
          {/* AI AVATAR */}
          <div style={{ display: "flex", justifyContent: "center", margin: "15px 0" }}>
            <div style={avatarStyle}>🤖</div>
          </div>

          {/* CHAT MESSAGES (Restored: This ensures questions are displayed) */}
          <div style={chatBoxStyle}>
            {messages.map((msg, i) => (
              <div key={i} style={{
                alignSelf: msg.role === "ai" ? "flex-start" : "flex-end",
                background: msg.role === "ai" ? "#1e293b" : "#4f46e5",
                padding: "12px 18px",
                borderRadius: "15px",
                margin: "10px 0",
                maxWidth: "75%",
                float: msg.role === "ai" ? "left" : "right",
                clear: "both",
                boxShadow: "0 2px 5px rgba(0,0,0,0.2)"
              }}>
                {msg.text}
              </div>
            ))}
          </div>

          {/* MONACO EDITOR (Shows during coding round) */}
          {questionType === "coding" && (
            <div className="leetcode-container" style={{ width: "100%", textAlign: "left", marginTop: "10px" }}>
              {/* 🟢 RESTORED QUESTION BOX FOR CODING ROUND */}
              <div style={{ background: "#1e293b", padding: "15px", borderRadius: "10px", marginBottom: "15px", borderLeft: "4px solid #4f46e5" }}>
                <h4 style={{ margin: "0 0 5px 0", color: "#94a3b8" }}>Question:</h4>
                <p style={{ margin: 0, fontSize: "16px" }}>{question}</p>
              </div>
              <div className="editor-header" style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px" }}>
                <h3 style={{ margin: 0 }}>💻 Coding Challenge</h3>
                <div>
                  <select 
                    value={language} 
                    onChange={(e) => setLanguage(e.target.value)}
                    style={{ background: "#1e293b", color: "white", padding: "5px", borderRadius: "5px", marginRight: "10px" }}
                  >
                    <option value="python">Python 3</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                    <option value="javascript">JavaScript</option>
                  </select>
                  <button onClick={runCode} className="run-btn" style={{ background: "#10b981", color: "white", padding: "5px 15px", borderRadius: "5px" }}>
                    ▶ Run Code
                  </button>
                </div>
              </div>

              <Editor
                height="400px"
                theme="vs-dark"
                language={language}
                value={code}
                onChange={(value) => setCode(value)}
                options={{ fontSize: 14, minimap: { enabled: false }, automaticLayout: true }}
              />

              <div className="output-window" style={{ background: "#000", color: "#10b981", padding: "15px", marginTop: "10px", borderRadius: "5px", border: "1px solid #1e293b" }}>
                <h4 style={{ margin: "0 0 5px 0", color: "#94a3b8" }}>Output:</h4>
                <pre style={{ margin: 0, whiteSpace: "pre-wrap" }}>{codeOutput || "Run code to see results..."}</pre>
              </div>
            </div>
          )}
        </div>

        {/* RIGHT SIDEBAR (Moved back to right, fixed width) */}
        <div style={{ 
          width: "350px", 
          background: "#0f172a", 
          padding: "20px", 
          borderLeft: "1px solid #1e293b", 
          display: "flex", 
          flexDirection: "column", 
          gap: "15px",
          overflowY: "auto",
          height: "100%" 
        }}>

          <h4>📄 Interview Setup</h4>
          
          <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
            <label>Name:</label>
            <input type="text" placeholder="Enter name" value={name} onChange={(e) => setName(e.target.value)} style={{ padding: "8px", background: "#1e293b", color: "white", border: "1px solid #334155" }} />
            
            <label>Resume:</label>
            <input type="file" accept=".pdf" onChange={(e) => uploadResume(e.target.files[0])} />
            
            <label>Mode:</label>
            <select value={mode} onChange={(e) => setMode(e.target.value)} style={{ padding: "8px", background: "#1e293b", color: "white" }}>
              <option value="hr">HR Mode</option>
              <option value="technical">Technical Mode</option>
            </select>

            <label>Total Questions:</label>
            <input type="number" value={totalQuestions} onChange={(e) => setTotalQuestions(Number(e.target.value))} style={{ padding: "8px", background: "#1e293b", color: "white" }} />

            <button onClick={startInterview} disabled={!resumeText} style={{ padding: "12px", background: resumeText ? "#4f46e5" : "#334155", marginTop: "10px", borderRadius: "8px" }}>
              {resumeText ? "🚀 Start Interview" : "Upload Resume First"}
            </button>
          </div>

          <div style={{ marginTop: "auto", textAlign: "center" }}>
            <video ref={videoRef} autoPlay playsInline muted style={{ width: "100%", borderRadius: "8px", border: "1px solid #4f46e5" }} />
            <p style={{ fontSize: "11px", marginTop: "5px", color: "#94a3b8" }}>Proctoring Enabled 🛡️</p>
            <p style={{ fontWeight: "bold", color: "#10b981", marginTop: "10px" }}>Coding Score: {codingScore}</p>
          </div>
        </div>
      </div>

      {/* --- FOOTER CONTROLS --- */}
      <div className="input-box" style={{ padding: "20px", borderTop: "1px solid #1e293b", background: "#0f172a", display: "flex", justifyContent: "center", alignItems: "center", gap: "15px" }}>
        
        {questionType !== "coding" ? (
          <>
            <button onClick={startListening} disabled={isListening} style={{ padding: "10px 20px", borderRadius: "20px" }}>🎤 Speak</button>
            <button onClick={stopListening} style={{ padding: "10px 20px", borderRadius: "20px", background: "#334155" }}>⛔ Stop</button>
            <button onClick={submitAnswer} style={{ padding: "10px 30px", borderRadius: "20px", background: "#4f46e5" }}>Submit Answer</button>
          </>
        ) : (
          <button onClick={submitCode} style={{ padding: "10px 30px", borderRadius: "20px", background: "#10b981" }}>Submit Final Solution</button>
        )}

        {interviewEnded && (
          <button onClick={downloadReport} style={{ padding: "10px 20px", borderRadius: "20px", background: "#fff", color: "#000" }}>📄 Download Report</button>
        )}
      </div>

      {/* OVERLAYS (Voice Wave & Feedback) */}
      {isListening && <div className="wave"><span></span><span></span><span></span></div>}
      
      {answer && (
        <p style={{ position: "fixed", bottom: "100px", left: "50%", transform: "translateX(-50%)", color: "#94a3b8", background: "rgba(0,0,0,0.6)", padding: "5px 15px", borderRadius: "10px" }}>
          {answer}
        </p>
      )}
    </div>
  );
}

export default Interview;