import React, { useEffect, useState } from "react";
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, BarChart, Bar 
} from 'recharts';

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#a855f7'];

function Admin() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/admin/results")
      .then(res => {
        if (!res.ok) throw new Error("Route not found");
        return res.json();
      })
      .then(res => {
        // Map the database columns to clear object keys
        // Assuming: row[1]=name, row[3]=score, row[4]=skills, row[5]=role, row[6]=timestamp
        const formatted = res.data.map(row => ({
          name: row[1],
          score: row[3],
          missing_keywords: row[4] || "", // Ensure this exists in your DB select
          role: row[5] || "Full Stack Developer", 
          timestamp: row[6] || new Date().toISOString()
        }));
        setData(formatted);
        setLoading(false);
      })
      .catch(err => console.error("Fetch error:", err));
  }, []);

  // --- 📈 DATA PROCESSING FOR CHARTS ---
  
  // 1. Score Trend (Average Score per Day)
  const chartData = data.reduce((acc, curr) => {
    const date = new Date(curr.timestamp).toLocaleDateString();
    const existing = acc.find(item => item.date === date);
    if (existing) {
      existing.score = Math.round((existing.score + curr.score) / 2);
    } else {
      acc.push({ date, score: curr.score });
    }
    return acc;
  }, []).slice(-7);

  // 2. Role Popularity (Pie Chart)
  const roleData = data.reduce((acc, curr) => {
    const role = curr.role;
    const existing = acc.find(item => item.name === role);
    if (existing) existing.value++;
    else acc.push({ name: role, value: 1 });
    return acc;
  }, []);

  // 3. Skill Gap Heatmap (Bar Chart of missing keywords)
  const skillGapData = data.reduce((acc, curr) => {
    const missing = curr.missing_keywords ? curr.missing_keywords.split(",") : [];
    missing.forEach(skill => {
      const trimmed = skill.trim();
      if (!trimmed) return;
      const existing = acc.find(item => item.skill === trimmed);
      if (existing) existing.count++;
      else acc.push({ skill: trimmed, count: 1 });
    });
    return acc;
  }, []).sort((a, b) => b.count - a.count).slice(0, 5);

  if (loading) return <div style={{padding: "40px", color: "white"}}>Loading Analytics...</div>;

  const handleResetData = async () => {
    if (window.confirm("⚠️ Are you sure? This will delete ALL student records forever.")) {
      try {
        const res = await fetch("http://127.0.0.1:8000/admin/clear-data", {
          method: "DELETE",
        });
        const result = await res.json();
        if (result.message) {
          setData([]); // Clear the UI immediately
          alert("Database wiped clean! You can start fresh now.");
        }
      } catch (err) {
        alert("Failed to clear data.");
      }
    }
  };

  return (
    <div style={styles.adminPage}>
      <h1 style={{ marginBottom: "30px" }}>📊 Placement Analytics Dashboard</h1>

      {/* STATS SUMMARY CARDS */}
      <div style={styles.statsRow}>
        <div style={styles.statCard}>
          <p style={styles.statLabel}>Total Students</p>
          <h2 style={styles.statValue}>{data.length}</h2>
        </div>
        <div style={{...styles.statCard, borderLeft: "4px solid #10b981"}}>
          <p style={styles.statLabel}>Avg Batch Score</p>
          <h2 style={styles.statValue}>
            {data.length ? (data.reduce((a, b) => a + b.score, 0) / data.length).toFixed(1) : 0}%
          </h2>
        </div>
      </div>

      {/* 📊 TREND ANALYTICS SECTION */}
      <div style={styles.chartGrid}>
        
        {/* Line Chart: Score Trend */}
        <div style={styles.chartCard}>
          <h4 style={styles.chartTitle}>📈 Average Score Trend (Last 7 Days)</h4>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
              <XAxis dataKey="date" stroke="#94a3b8" fontSize={10} tickLine={false} />
              <YAxis stroke="#94a3b8" fontSize={10} tickLine={false} axisLine={false} />
              <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid #334155", color: "white" }} />
              <Line type="monotone" dataKey="score" stroke="#6366f1" strokeWidth={3} dot={{ r: 4, fill: '#6366f1' }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Bar Chart: Skill Gaps */}
        <div style={styles.chartCard}>
          <h4 style={{...styles.chartTitle, color: '#ef4444'}}>🚩 Top Skill Deficiencies</h4>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={skillGapData}>
              <XAxis dataKey="skill" stroke="#94a3b8" fontSize={10} tickLine={false} />
              <Tooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{background: '#0f172a', border: '1px solid #334155'}} />
              <Bar dataKey="count" fill="#ef4444" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Pie Chart: Role Interest */}
        <div style={styles.chartCard}>
          <h4 style={{...styles.chartTitle, color: '#10b981'}}>🥧 Targeted Roles</h4>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={roleData} innerRadius={50} outerRadius={70} paddingAngle={5} dataKey="value">
                {roleData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{background: '#0f172a', border: '1px solid #334155'}} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>📊 Placement Analytics Dashboard</h1>
        <button 
          onClick={handleResetData}
          style={{
            background: "#ef4444",
            color: "white",
            border: "none",
            padding: "10px 20px",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: "bold"
          }}
        >
          🗑️ Reset All Data
        </button>
      </div>

      {/* ENHANCED TABLE */}
      <h2 style={{ marginTop: "40px", marginBottom: "20px" }}>📋 Student Performance Data</h2>
      <div style={styles.tableContainer}>
        <table style={styles.table}>
          <thead>
            <tr style={{ background: "#1e293b" }}>
              <th style={styles.th}>Name</th>
              <th style={styles.th}>Role</th>
              <th style={styles.th}>ATS Score</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i} style={{ borderBottom: "1px solid #1e293b" }}>
                <td style={styles.td}>{row.name}</td>
                <td style={{...styles.td, color: "#818cf8"}}>{row.role}</td>
                <td style={styles.td}>
                    <span style={{
                        padding: "4px 10px", 
                        borderRadius: "12px", 
                        background: row.score > 75 ? "#064e3b" : "#450a0a",
                        fontSize: "12px"
                    }}>
                        {row.score}%
                    </span>
                </td>
                <td 
                  onClick={() => setSelectedUser(row)} 
                  style={{ cursor: "pointer", color: "#818cf8", textDecoration: "underline" }}
                >
                  {row.name}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* 🔍 DEEP VIEW MODAL */}
      {selectedUser && (
        <div style={styles.modalOverlay}>
          <div style={styles.modalContent}>
            {/* Header */}
            <div style={styles.modalHeader}>
              <h2 style={{margin: 0}}>🔍 Deep Analysis: {selectedUser.name}</h2>
              <button onClick={() => setSelectedUser(null)} style={styles.closeBtn}>✕ Close</button>
            </div>

            <div style={styles.splitScreen}>
              {/* LEFT: PDF VIEWER */}
              <div style={styles.pdfContainer}>
                <h4 style={styles.panelTitle}>📄 Original Resume</h4>
                {/* Note: In production, you'd serve the file from your backend URL */}
                <iframe 
                  src={`http://127.0.0.1:8000/files/${selectedUser.filename || 'temp_resume.pdf'}`} 
                  style={{ width: "100%", height: "100%", border: "none", borderRadius: "8px" }}
                  title="Resume Preview"
                />
              </div>

              {/* RIGHT: AI CRITIQUE & BREAKDOWN */}
              <div style={styles.analysisContainer}>
                <h4 style={styles.panelTitle}>🧠 AI Evaluation Breakdown</h4>
                
                {/* Match Score */}
                <div style={{...styles.statCard, marginBottom: "20px", background: "#1e293b"}}>
                  <p style={{margin: 0, fontSize: "12px"}}>Overall ATS Match</p>
                  <h1 style={{margin: 0, color: "#10b981"}}>{selectedUser.score}%</h1>
                </div>

                {/* We reuse the Breakdown Bars logic here */}
                <div style={styles.breakdownGrid}>
                  {selectedUser.breakdown && Object.entries(selectedUser.breakdown).map(([key, val]) => (
                    <div key={key} style={styles.miniBarRow}>
                      <div style={{display: "flex", justifyContent: "space-between", fontSize: "12px"}}>
                        <span>{key.replace("_", " ")}</span>
                        <span>{val}%</span>
                      </div>
                      <div style={styles.barBg}><div style={{...styles.barFill, width: `${val}%`}}></div></div>
                    </div>
                  ))}
                </div>

                {/* Tips List */}
                <h4 style={{marginTop: "20px", fontSize: "14px", color: "#818cf8"}}>💡 Key AI Tips</h4>
                <div style={{maxHeight: "200px", overflowY: "auto"}}>
                   {selectedUser.tips?.map((tip, i) => (
                     <p key={i} style={{fontSize: "12px", color: tip.type === 'good' ? '#4ade80' : '#fb7185', background: "rgba(255,255,255,0.05)", padding: "8px", borderRadius: "5px"}}>
                       {tip.type === 'good' ? '✔' : '✖'} {tip.msg}
                     </p>
                   ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// --- STYLES ---
const styles = {
  adminPage: { 
    padding: "40px", 
    background: "#020617", 
    minHeight: "100vh", 
    color: "white",
    fontFamily: "Inter, sans-serif"
  },
  statsRow: { display: "flex", gap: "20px", marginBottom: "30px" },
  statCard: { 
    flex: 1, 
    background: "#0f172a", 
    padding: "20px", 
    borderRadius: "12px", 
    border: "1px solid #1e293b",
    borderLeft: "4px solid #6366f1"
  },
  statLabel: { margin: 0, color: "#94a3b8", fontSize: "12px", textTransform: "uppercase" },
  statValue: { margin: "5px 0 0 0", fontSize: "28px" },
  chartGrid: { 
    display: "grid", 
    gridTemplateColumns: "1fr 1fr 1fr", 
    gap: "20px", 
    marginBottom: "30px" 
  },
  chartCard: { 
    background: "#0f172a", 
    padding: "20px", 
    borderRadius: "12px", 
    border: "1px solid #1e293b" 
  },
  chartTitle: { margin: "0 0 15px 0", fontSize: "14px", fontWeight: "600", color: "#818cf8" },
  tableContainer: { 
    background: "#0f172a", 
    borderRadius: "12px", 
    overflow: "hidden", 
    border: "1px solid #1e293b" 
  },
  table: { width: "100%", borderCollapse: "collapse", textAlign: "left" },
  th: { padding: "15px", fontSize: "13px", color: "#94a3b8", fontWeight: "600" },
  td: { padding: "15px", fontSize: "14px" },
  modalOverlay: { position: "fixed", top: 0, left: 0, width: "100%", height: "100%", background: "rgba(0,0,0,0.85)", display: "flex", justifyContent: "center", alignItems: "center", zIndex: 1000 },
  modalContent: { width: "90%", height: "90%", background: "#0f172a", borderRadius: "15px", display: "flex", flexDirection: "column", padding: "20px", border: "1px solid #334155" },
  modalHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid #334155", paddingBottom: "15px" },
  closeBtn: { background: "#ef4444", color: "white", border: "none", padding: "8px 15px", borderRadius: "5px", cursor: "pointer" },
  splitScreen: { display: "flex", flex: 1, gap: "20px", marginTop: "20px", overflow: "hidden" },
  pdfContainer: { flex: 1.2, background: "#1e293b", borderRadius: "10px", padding: "10px", display: "flex", flexDirection: "column" },
  analysisContainer: { flex: 1, padding: "10px", overflowY: "auto" },
  panelTitle: { color: "#94a3b8", textTransform: "uppercase", fontSize: "12px", letterSpacing: "1px", marginBottom: "15px" },
  barBg: { height: "6px", background: "#334155", borderRadius: "3px", marginTop: "4px" },
  barFill: { height: "100%", background: "#6366f1", borderRadius: "3px" },
  miniBarRow: { marginBottom: "12px" }
};

export default Admin;