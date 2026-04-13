import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

function ResumeAnalyzer() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // User Info States
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  // AI Builder States
  const [builderInput, setBuilderInput] = useState("");
  const [generatedPoint, setGeneratedPoint] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [numCourses, setNumCourses] = useState(5);

  // 1. Handle Main Resume Analysis
  const handleUpload = async () => {
    if (!file) return alert("Please upload a resume (PDF)");
    if (!name || !email || !phone) return alert("Please fill in all contact fields");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("name", name);
    formData.append("email", email);
    formData.append("phone", phone);

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze-resume-full", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Error connecting to AI Backend. Make sure FastAPI is running.");
    } finally {
      setLoading(false);
    }
  };

  // 2. Handle AI Bullet Point Generation
  const generateAIPoint = async () => {
    if (!builderInput) return alert("Please describe a task first.");
    setIsGenerating(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/ai-resume-builder", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: builderInput }),
      });
      const data = await res.json();
      setGeneratedPoint(data.bullet_point);
    } catch (err) {
      alert("Error generating bullet point.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div style={styles.page}>
      {/* HEADER */}
      <motion.h1
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        style={styles.title}
      >
        🚀 AI Career Hub
      </motion.h1>

      <div style={styles.container}>
        {/* LEFT COLUMN: UPLOAD & BUILDER */}
        <div style={styles.leftCol}>
          <motion.div
            style={styles.card}
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h3 style={{ marginBottom: "15px" }}>📄 Upload Resume</h3>
            <input placeholder="Full Name" value={name} onChange={(e) => setName(e.target.value)} style={styles.input} />
            <input placeholder="Email Address" value={email} onChange={(e) => setEmail(e.target.value)} style={styles.input} />
            <input placeholder="Phone Number" value={phone} onChange={(e) => setPhone(e.target.value)} style={styles.input} />
            <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} style={styles.file} />

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleUpload}
              style={{ ...styles.button, background: "linear-gradient(135deg, #6366f1, #a855f7)" }}
              disabled={loading}
            >
              {loading ? "AI is Analyzing..." : "Run Deep Analysis"}
            </motion.button>
          </motion.div>

          {/* AI BUILDER CARD */}
          <motion.div
            style={{ ...styles.card, marginTop: "20px", border: "1px dashed #6366f1" }}
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h3 style={{ color: "#818cf8", marginBottom: "10px" }}>✨ AI Bullet Point Generator</h3>
            <textarea
              placeholder="e.g., I built a library system using Java"
              value={builderInput}
              onChange={(e) => setBuilderInput(e.target.value)}
              style={{ ...styles.input, height: "80px", resize: "none" }}
            />
            <button
              onClick={generateAIPoint}
              style={{ ...styles.button, background: "#1e293b", border: "1px solid #4f46e5", marginTop: "10px" }}
              disabled={isGenerating}
            >
              {isGenerating ? "Generating..." : "Professionalize Point"}
            </button>

            {generatedPoint && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                style={styles.aiResult}
              >
                <strong style={{ color: "#10b981" }}>AI Suggested Bullet:</strong>
                <p style={{ margin: "5px 0 0 0", fontSize: "13px" }}>{generatedPoint}</p>
              </motion.div>
            )}
          </motion.div>
        </div>

        {/* RIGHT COLUMN: RESULTS */}
        <div style={styles.rightCol}>
          <AnimatePresence>
            {result ? (
              <motion.div
                style={styles.resultCard}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
              >
                <div style={{ borderBottom: "1px solid #334155", paddingBottom: "15px" }}>
                  <h2 style={{ margin: 0 }}>{result.name}</h2>
                  <p style={{ color: "#94a3b8", margin: "5px 0" }}>{result.email}</p>
                </div>

                {/* SCORE */}
                {/* 📊 UPDATED: PROFESSIONAL ATS BREAKDOWN */}
                <Section title="📊 Professional ATS Analysis">
                  <div style={{ marginBottom: "20px" }}>
                    <div style={styles.progressBg}>
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${result.score}%` }}
                        style={{ 
                          ...styles.progress, 
                          width: `${result.score}%`,
                          background: result.score > 70 ? "#22c55e" : "#eab308" 
                        }}
                      >
                        Total Match: {result.score}%
                      </motion.div>
                    </div>
                  </div>

                  {/* Detailed Breakdown Grid */}
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "15px" }}>
                    {[
                      { label: "Role Match", val: result.breakdown?.role_match || 0, color: "#6366f1" },
                      { label: "Impact/STAR", val: result.breakdown?.impact_metrics || 0, color: "#10b981" },
                      { label: "Skill Depth", val: result.breakdown?.skill_depth || 0, color: "#f59e0b" },
                      { label: "Formatting", val: result.breakdown?.formatting || 0, color: "#a855f7" }
                    ].map((item, i) => (
                      <div key={i} style={{ background: "#1e293b", padding: "10px", borderRadius: "8px" }}>
                        <p style={{ fontSize: "11px", margin: "0 0 5px 0", color: "#94a3b8" }}>{item.label}</p>
                        <div style={{ height: "6px", background: "#334155", borderRadius: "3px", overflow: "hidden" }}>
                          <div style={{ width: `${item.val}%`, height: "100%", background: item.color }} />
                        </div>
                        <span style={{ fontSize: "12px", fontWeight: "bold" }}>{item.val}%</span>
                      </div>
                    ))}
                  </div>
                </Section>

                {/* SKILLS */}
                <Section title="🛠 Detected Skills">
                  {result.skills?.map((s, i) => (
                    <span key={i} style={styles.chip}>{s}</span>
                  ))}
                </Section>

                {/* MISSING KEYWORDS */}
                {result.missing_keywords && (
                  <Section title="🔍 Keywords to Add (Boost Score)">
                    {result.missing_keywords.map((word, i) => (
                      <span key={i} style={{ ...styles.chip, background: "#7f1d1d", border: "1px solid #ef4444" }}>
                        + {word}
                      </span>
                    ))}
                  </Section>
                )}

                {/* TIPS */}
                {/* 💡 AI CRITIQUE (Professional Detailed List) */}
                <Section title="💡 Detailed AI Critique">
                  <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
                    {result.tips?.map((tip, i) => (
                      <div key={i} style={{ 
                        padding: "12px", 
                        background: tip.type === "good" ? "rgba(34, 197, 94, 0.05)" : "rgba(239, 68, 68, 0.05)",
                        borderLeft: `4px solid ${tip.type === "good" ? "#22c55e" : "#ef4444"}`,
                        borderRadius: "4px"
                      }}>
                        <strong style={{ color: tip.type === "good" ? "#4ade80" : "#fb7185", fontSize: "12px", display: "block", marginBottom: "5px" }}>
                          {tip.type === "good" ? "✅ STRENGTH" : "🚩 IMPROVEMENT NEEDED"}
                        </strong>
                        <p style={{ color: "#cbd5e1", fontSize: "13px", lineHeight: "1.6", margin: 0 }}>
                          {tip.msg}
                        </p>
                      </div>
                    ))}
                  </div>
                </Section>

                {/* 📚 NEW: COURSE RECOMMENDATIONS */}
                <Section title="📚 Recommended Courses">
                  <div style={{ marginBottom: "15px", display: "flex", alignItems: "center", gap: "10px" }}>
                    <span style={{ fontSize: "12px", color: "#94a3b8" }}>Show: {numCourses}</span>
                    <input 
                      type="range" min="1" max="10" 
                      value={numCourses} 
                      onChange={(e) => setNumCourses(e.target.value)} 
                      style={{ flex: 1, cursor: "pointer" }}
                    />
                  </div>
                  <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                    {result.recommendations?.slice(0, numCourses).map((course, i) => (
                      <p key={i} style={{ fontSize: "13px", margin: 0, color: "#cbd5e1" }}>
                        • {Array.isArray(course) ? course[0] : course}
                      </p>
                    ))}
                  </div>
                </Section>

                {/* 🎬 NEW: PREPARATION VIDEOS */}
                <Section title="🎬 Bonus Preparation Videos">
                  <div style={{ display: "flex", gap: "10px", marginTop: "10px" }}>
                    <div style={{ flex: 1 }}>
                      <iframe 
                        width="100%" height="150" 
                        src="https://www.youtube.com/embed/Tt08KmFfIYQ" 
                        title="Resume Tips" 
                        style={{ borderRadius: "8px", border: "1px solid #334155" }}
                        allowFullScreen
                      ></iframe>
                    </div>
                    <div style={{ flex: 1 }}>
                      <iframe 
                        width="100%" height="150" 
                        src="https://www.youtube.com/embed/HG68Ymazo18" 
                        title="Interview Tips" 
                        style={{ borderRadius: "8px", border: "1px solid #334155" }}
                        allowFullScreen
                      ></iframe>
                    </div>
                  </div>
                </Section>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  onClick={() => window.location.href = "/interview"}
                  style={{ ...styles.button, background: "#4f46e5", marginTop: "30px" }}
                >
                  Proceed to Practice Interview ➔
                </motion.button>
              </motion.div>
            ) : (
              <div style={styles.emptyState}>
                <p>Upload your resume to see the AI analysis report here.</p>
              </div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}

const Section = ({ title, children }) => (
  <div style={{ marginTop: "25px" }}>
    <h4 style={{ marginBottom: "12px", color: "#818cf8", textTransform: "uppercase", letterSpacing: "1px" }}>{title}</h4>
    {children}
  </div>
);

const styles = {
  page: {
    minHeight: "100vh",
    background: "radial-gradient(circle at top, #1e293b, #020617)",
    color: "white",
    padding: "40px",
    fontFamily: "'Inter', sans-serif"
  },
  container: {
    display: "flex",
    maxWidth: "1200px",
    margin: "auto",
    gap: "30px"
  },
  leftCol: { flex: 1 },
  rightCol: { flex: 1.5 },
  title: { textAlign: "center", fontSize: "40px", marginBottom: "40px", fontWeight: "800" },
  card: {
    background: "rgba(30, 41, 59, 0.7)",
    backdropFilter: "blur(10px)",
    padding: "25px",
    borderRadius: "15px",
    border: "1px solid #334155",
    boxShadow: "0 10px 25px rgba(0,0,0,0.3)"
  },
  input: {
    width: "100%",
    padding: "12px",
    marginBottom: "12px",
    borderRadius: "8px",
    border: "1px solid #334155",
    background: "#0f172a",
    color: "white",
    boxSizing: "border-box"
  },
  file: { margin: "10px 0 20px 0", fontSize: "14px" },
  button: {
    width: "100%",
    padding: "14px",
    borderRadius: "8px",
    border: "none",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
    transition: "all 0.3s ease"
  },
  resultCard: {
    background: "#0f172a",
    padding: "30px",
    borderRadius: "20px",
    border: "1px solid #1e293b",
    boxShadow: "0 20px 50px rgba(0,0,0,0.5)"
  },
  chip: {
    display: "inline-block",
    padding: "6px 12px",
    margin: "4px",
    background: "#1e293b",
    border: "1px solid #334155",
    borderRadius: "6px",
    fontSize: "13px"
  },
  progressBg: { background: "#1e293b", borderRadius: "12px", height: "35px", overflow: "hidden" },
  progress: {
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: "bold",
    fontSize: "14px"
  },
  aiResult: {
    marginTop: "15px",
    padding: "12px",
    background: "rgba(16, 185, 129, 0.1)",
    border: "1px solid #10b981",
    borderRadius: "8px"
  },
  emptyState: {
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    border: "2px dashed #334155",
    borderRadius: "20px",
    color: "#64748b",
    textAlign: "center",
    padding: "40px"
  }
};

export default ResumeAnalyzer;