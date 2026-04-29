import React, { useState, useEffect, useCallback } from "react";
import Editor from "@monaco-editor/react";

const SECTIONS = [
  { name: "Numerical", duration: 1800 },
  { name: "Verbal", duration: 1200 },
  { name: "Reasoning", duration: 1500 },
  { name: "Advanced quants & reasoning", duration: 1800 },
  { name: "Coding", duration: 2700 }
];

const TcsMockTest = () => {
  const [examData, setExamData] = useState({});
  const [activeSecIdx, setActiveSecIdx] = useState(0);
  const [currentQIdx, setCurrentQIdx] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(SECTIONS[0].duration);
  const [codeAnswers, setCodeAnswers] = useState({});
  const [loading, setLoading] = useState(true);
  const [selectedLang, setSelectedLang] = useState("python");
  const [stdin, setStdin] = useState("");
  const [runOutput, setRunOutput] = useState("");
  const [submitResult, setSubmitResult] = useState(null);
  const [codingScores, setCodingScores] = useState({});
  const [finalResult, setFinalResult] = useState(null);
  const [fullscreenViolations, setFullscreenViolations] = useState(0);
  const [examStarted, setExamStarted] = useState(false);

// ✅ FETCH DATA
useEffect(() => {
  if (Object.keys(examData).length > 0) return;

  const loadMockTest = async () => {
    try {
      const res = await fetch("http://localhost:8000/get-mock-test");
      const data = await res.json();
      console.log("FULL EXAM DATA:", data);
      setExamData(data);
      setLoading(false);
    } catch (err) {
      console.error("MOCK FETCH ERROR:", err);
      setLoading(false);
    }
  };

  loadMockTest();
}, [examData]);

const getStarterCode = (lang) => {
  if (lang === "python") {
    return `# Write your Python code here
n = int(input())
arr = [int(input()) for _ in range(n)]

# your logic here
print()`;
  }

  if (lang === "cpp") {
    return `#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> arr(n);
    for(int i=0;i<n;i++) cin >> arr[i];

    // your logic here
    return 0;
}`;
  }

  if (lang === "c") {
    return `#include <stdio.h>

int main() {
    int n;
    scanf("%d",&n);
    int arr[n];
    for(int i=0;i<n;i++) scanf("%d",&arr[i]);

    // your logic here
    return 0;
}`;
  }

  if (lang === "java") {
    return `import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] arr = new int[n];
        for(int i=0;i<n;i++) arr[i] = sc.nextInt();

        // your logic here
    }
}`;
  }

  if (lang === "javascript") {
    return `const fs = require('fs');
const input = fs.readFileSync(0,'utf8').trim().split(/\\s+/);
let idx = 0;
let n = parseInt(input[idx++]);
let arr = [];
for(let i=0;i<n;i++) arr.push(parseInt(input[idx++]));

// your logic here`;
  }

  return "";
};

const extractSampleInput = (questionText) => {
  if (!questionText) return "";
  const match = questionText.match(/Example 1:[\\s\\S]*?Input:\\s*([\\s\\S]*?)Output:/i);
  return match && match[1] ? match[1].trim() : "";
};

const currentSectionName = SECTIONS[activeSecIdx]?.name || "Numerical";

const currentQuestions =
  examData[currentSectionName] ||
  examData[currentSectionName?.toLowerCase()] ||
  examData[currentSectionName?.toUpperCase()] ||
  examData["questions"] ||
  [];

const currentQ = currentQuestions[currentQIdx] || {};

useEffect(() => {
  if (currentQ?.type === "coding") {
    setStdin(extractSampleInput(currentQ.question));
    setRunOutput("");
    setSubmitResult(null);
  }
}, [currentQIdx, activeSecIdx]);

const submitTest = useCallback(async () => {
  const res = await fetch("http://localhost:8000/submit-mock-test", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answers })
  });

  const data = await res.json();
  const mcqPercentage = data.percentage || 0;

  const codingVals = Object.values(codingScores);
  const codingAvg = codingVals.length
    ? codingVals.reduce((a, b) => a + b, 0) / codingVals.length
    : 0;

  const finalOverall = (mcqPercentage * 0.7 + codingAvg * 0.3).toFixed(2);

  let level = "Needs Improvement";
  if (finalOverall >= 80) level = "Excellent";
  else if (finalOverall >= 60) level = "Good";

  const weakAreas = [];
  const strongAreas = [];

  Object.keys(data.section_total || {}).forEach(sec => {
    const secTotal = data.section_total[sec];
    const secScore = data.section_score[sec] || 0;
    const secPerc = (secScore / secTotal) * 100;

    if (secPerc >= 75) strongAreas.push(sec);
    if (secPerc < 50) weakAreas.push(sec);
  });

  let aiMessage = "";

  if (strongAreas.length) {
    aiMessage += `💪 Strong Areas: ${strongAreas.join(", ")}\n`;
  }

  if (weakAreas.length) {
    aiMessage += `⚠ Needs Improvement: ${weakAreas.join(", ")}\n`;
  }

  if (codingAvg >= 70) {
    aiMessage += `💻 Coding problem solving is strong.\n`;
  } else {
    aiMessage += `💻 Coding logic needs more timed practice.\n`;
  }

  if (mcqPercentage < 60) {
    aiMessage += `📚 Aptitude accuracy is below expected TCS benchmark.\n`;
  }

  setFinalResult({
    mcqScore: `${data.score}/${data.total}`,
    mcqPercentage,
    codingAvg,
    finalOverall,
    level,
    aiMessage
  });
}, [answers, codingScores]);

const moveToNextSection = useCallback(() => {
  if (currentSectionName === "Coding" && !submitResult) {
    alert("Please submit your code before leaving Coding section.");
    return;
  }

  if (activeSecIdx < SECTIONS.length - 1) {
    const next = activeSecIdx + 1;
    setActiveSecIdx(next);
    setCurrentQIdx(0);
    setTimeLeft(SECTIONS[next].duration);
  } else {
    submitTest();
  }
}, [activeSecIdx, currentSectionName, submitResult, submitTest]);

// ⏱ TIMER
useEffect(() => {
  const timer = setInterval(() => {
    setTimeLeft(prev => {
      if (prev <= 1) {
        moveToNextSection();
        return 0;
      }
      return prev - 1;
    });
  }, 1000);

  return () => clearInterval(timer);
}, [moveToNextSection]);

if (loading) {
  return (
    <div style={{
      height: "100vh",
      background: "#020617",
      color: "white",
      display: "flex",
      justifyContent: "center",
      alignItems: "center"
    }}>
      🚀 Loading AI Mock Test...
    </div>
  );
}

if (!currentQuestions || currentQuestions.length === 0) {
  return (
    <div style={{ color: "white", padding: "50px" }}>
      ⚠ No questions available for {currentSectionName}
    </div>
  );
}

const handleFinalSubmit = async () => {
  const ok = window.confirm("Are you sure you want to submit the entire mock test? Once submitted test will end.");
  if (!ok) return;

  await submitTest();
};
if (finalResult) {
  return (
    <div style={{
      minHeight: "100vh",
      background: "#020617",
      display: "flex",
      justifyContent: "center",
      alignItems: "center"
    }}>
      <div style={{
        width: "600px",
        background: "#0f172a",
        borderRadius: "18px",
        padding: "30px",
        color: "white"
      }}>
        <h2 style={{ color: "#38bdf8", marginBottom: "20px" }}>
          📊 TCS Mock Test Performance Dashboard
        </h2>

        <div style={{ background:"#1e293b", padding:"15px", borderRadius:"10px", marginBottom:"15px" }}>
          <h3>MCQ Aptitude Score</h3>
          <p>{finalResult.mcqScore}</p>
          <p>{finalResult.mcqPercentage.toFixed(2)}%</p>
        </div>

        <div style={{ background:"#1e293b", padding:"15px", borderRadius:"10px", marginBottom:"15px" }}>
          <h3>Coding Performance</h3>
          <p>{finalResult.codingAvg.toFixed(2)}%</p>
        </div>

        <div style={{ background:"#1d4ed8", padding:"20px", borderRadius:"12px", marginBottom:"15px" }}>
          <h2>Overall Score: {finalResult.finalOverall}%</h2>
          <h3>{finalResult.level}</h3>
        </div>

        <div style={{
          background:"#1e293b",
          padding:"15px",
          borderRadius:"10px",
          marginTop:"15px",
          whiteSpace:"pre-line",
          color:"#facc15"
        }}>
          <h3>🤖 AI Performance Feedback</h3>
          <p>{finalResult.aiMessage}</p>
        </div>
      </div>
    </div>
  );
}
const enterFullScreen = () => {
  const elem = document.documentElement;

  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.webkitRequestFullscreen) {
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) {
    elem.msRequestFullscreen();
  }
};

  return (
  <div style={{ display: "flex", height: "100vh", background: "#020617" }}>

    {/* TOP BAR */}
    <div style={{
      position: "fixed",
      top: 0,
      width: "100%",
      height: "60px",
      background: "#020617",
      display: "flex",
      alignItems: "center",
      padding: "0 30px",
      borderBottom: "1px solid #334155",
      zIndex: 100
    }}>
      {SECTIONS.map((sec, i) => (
        <div
          key={i}
          onClick={() => {
            setActiveSecIdx(i);
            setCurrentQIdx(0);
          }}
          style={{
            marginRight: "30px",
            cursor: "pointer",
            color: activeSecIdx === i ? "#3b82f6" : "#94a3b8"
          }}
        >
          {sec.name}
        </div>
      ))}

      <button
        onClick={handleFinalSubmit}
        style={{
          background: "#dc2626",
          color: "white",
          border: "none",
          padding: "10px 20px",
          borderRadius: "8px",
          fontWeight: "bold",
          cursor: "pointer"
        }}
      >
        Final Submit Test
      </button>

      <div style={{
        marginLeft: "auto",
        color: timeLeft < 60 ? "red" : "#38bdf8"
      }}>
        ⏱ {Math.floor(timeLeft / 60)}:{String(timeLeft % 60).padStart(2, "0")}
      </div>
    </div>

    {/* MAIN */}
    <div style={{ flex: 1, marginTop: "60px", padding: "30px" }}>

      {currentQ.type === "mcq" ? (

        <div style={{
          background: "#1e293b",
          padding: "30px",
          borderRadius: "16px",
          color: "white"
        }}>
          <h3>{currentSectionName} • Q{currentQIdx + 1}</h3>

          <p style={{ marginTop: "20px", whiteSpace: "pre-wrap" }}>
            {currentQ.question}
          </p>

          <div style={{ marginTop: "20px" }}>
            {currentQ.options.map((opt, i) => (
              <button
                key={i}
                onClick={() =>
                  setAnswers({ ...answers, [currentQ.id]: i })
                }
                style={{
                  width: "100%",
                  marginBottom: "10px",
                  padding: "12px",
                  background:
                    answers[currentQ.id] === i ? "#2563eb" : "#020617",
                  color: "white",
                  border: "1px solid #334155",
                  borderRadius: "8px"
                }}
              >
                {opt}
              </button>
            ))}
          </div>
        </div>

      ) : (

        <div style={{
          display: "flex",
          gap: "20px",
          height: "calc(100vh - 140px)"
        }}>

          {/* LEFT QUESTION PANEL */}
          <div style={{
            width: "42%",
            background: "#1e293b",
            borderRadius: "16px",
            padding: "25px",
            color: "white",
            overflowY: "auto"
          }}>
            <h3>{currentSectionName} • Q{currentQIdx + 1}</h3>

            <pre style={{
              whiteSpace: "pre-wrap",
              fontFamily: "inherit",
              lineHeight: "1.6",
              marginTop: "20px"
            }}>
              {currentQ.question}
            </pre>
          </div>

          {/* RIGHT CODING PANEL */}
          <div style={{
            width: "58%",
            background: "#1e293b",
            borderRadius: "16px",
            padding: "20px",
            color: "white",
            overflowY: "auto"
          }}>
            <h4 style={{ color: "#38bdf8" }}>💻 Coding Challenge</h4>

            <select
              value={selectedLang}
              onChange={(e) => {
                const lang = e.target.value;
                setSelectedLang(lang);

                if (!codeAnswers[currentQ.id]) {
                  setCodeAnswers({
                    ...codeAnswers,
                    [currentQ.id]: getStarterCode(lang)
                  });
                }
              }}
              style={{
                padding: "10px",
                marginTop: "10px",
                marginBottom: "10px",
                background: "#020617",
                color: "white",
                border: "1px solid #334155"
              }}
            >
              <option value="python">Python</option>
              <option value="cpp">C++</option>
              <option value="c">C</option>
              <option value="java">Java</option>
              <option value="javascript">JavaScript</option>
            </select>

            <div style={{
              background: "#0f172a",
              padding: "10px",
              borderRadius: "8px",
              marginBottom: "10px",
              fontSize: "13px",
              color: "#facc15"
            }}>
              ⚠ Important Instructions:<br/>
              • Read values only using standard input<br/>
              • Do not print Enter/Input prompts<br/>
              • Print only the final answer<br/>
              • For Java use <b>public class Main</b>
            </div>

            <Editor
              height="300px"
              theme="vs-dark"
              language={selectedLang}
              value={codeAnswers[currentQ.id] || getStarterCode(selectedLang)}
              onChange={(val) =>
                setCodeAnswers({ ...codeAnswers, [currentQ.id]: val })
              }
            />

            <textarea
              placeholder="Sample input auto loaded here. You can modify and Run Code..."
              value={stdin}
              onChange={(e) => setStdin(e.target.value)}
              style={{
                width: "100%",
                height: "80px",
                marginTop: "10px",
                background: "#020617",
                color: "white",
                border: "1px solid #334155",
                padding: "10px"
              }}
            />

            <div style={{ display: "flex", gap: "10px", marginTop: "10px" }}>
              <button
                onClick={async () => {
                  const res = await fetch("http://localhost:8000/run-code", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                      language: selectedLang,
                      code: codeAnswers[currentQ.id] || "",
                      stdin: stdin
                    })
                  });

                  const data = await res.json();
                  setRunOutput(data.output);
                }}
                style={{
                  padding: "10px 20px",
                  background: "#2563eb",
                  color: "white",
                  border: "none",
                  borderRadius: "8px"
                }}
              >
                ▶ Run Code
              </button>

              <button
                onClick={async () => {
                  console.log("FULL CURRENT QUESTION =", currentQ);
                  console.log("SUBMITTING KEYWORD =", currentQ.correct);
                  const res = await fetch("http://localhost:8000/submit-code", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                      language: selectedLang,
                      code: codeAnswers[currentQ.id] || "",
                      keyword: currentQ.correct
                    })
                  });

                  const data = await res.json();
                  setSubmitResult(data);

                  setCodingScores(prev => ({
                    ...prev,
                    [currentQ.id]: data.score
                  }));
                }}
                style={{
                  padding: "10px 20px",
                  background: "#16a34a",
                  color: "white",
                  border: "none",
                  borderRadius: "8px"
                }}
              >
                ✅ Submit Code
              </button>
            </div>

            <div style={{
              marginTop: "15px",
              background: "#000",
              color: "#22c55e",
              padding: "12px",
              minHeight: "70px",
              borderRadius: "8px",
              whiteSpace: "pre-wrap"
            }}>
              <b>Console Output:</b><br />
              {runOutput}
            </div>

            {submitResult && (
              <div style={{
                marginTop: "15px",
                background: "#0f172a",
                padding: "15px",
                borderRadius: "10px",
                color: "white"
              }}>
                <h4 style={{ marginBottom: "10px", color: "#38bdf8" }}>
                  ✅ Submission Verdict
                </h4>

                <div>Passed: {submitResult.passed}/{submitResult.total}</div>
                <div>Score: {submitResult.score}%</div>
                <div>Status: {submitResult.status}</div>

                <hr style={{ margin: "12px 0", borderColor: "#334155" }} />

                {submitResult.details && submitResult.details.map((tc, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: tc.passed ? "#052e16" : "#450a0a",
                      padding: "10px",
                      marginBottom: "10px",
                      borderRadius: "8px"
                    }}
                  >
                    <div>
                      Testcase {tc.case}: {tc.passed ? "✅ Passed" : "❌ Failed"}
                    </div>

                    {!tc.passed && (
                      <>
                        <div style={{ marginTop: "6px", fontSize: "13px" }}>
                          <b>Expected:</b> {tc.expected}
                        </div>
                        <div style={{ marginTop: "4px", fontSize: "13px" }}>
                          <b>Your Output:</b> {tc.got || "(no output)"}
                        </div>
                      </>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>

    {/* RIGHT PANEL */}
    <div style={{
      width: "250px",
      marginTop: "60px",
      padding: "20px",
      background: "#020617",
      borderLeft: "1px solid #334155"
    }}>
      <h4 style={{ color: "white" }}>Palette</h4>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(4, 1fr)",
        gap: "8px",
        marginTop: "15px"
      }}>
        {currentQuestions.map((q, i) => (
          <button
            key={i}
            onClick={() => setCurrentQIdx(i)}
            style={{
              height: "35px",
              background:
                currentQIdx === i
                  ? "#3b82f6"
                  : (answers[q.id] !== undefined || codingScores[q.id] !== undefined)
                  ? "#10b981"
                  : "#1e293b",
              color: "white",
              border: "none"
            }}
          >
            {i + 1}
          </button>
        ))}
      </div>

      <button
        onClick={moveToNextSection}
        style={{
          width: "100%",
          marginTop: "20px",
          padding: "12px",
          background: "#3b82f6",
          color: "white",
          border: "none",
          borderRadius: "8px"
        }}
      >
        Next →
      </button>
    </div>
  </div>
);
};

export default TcsMockTest;