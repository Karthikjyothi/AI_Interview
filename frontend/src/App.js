import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

import Interview from "./pages/Interview";
import ResumeAnalyzer from "./pages/ResumeAnalyzer";
import Admin from "./pages/Admin";

// 🔥 Sidebar Item Component
const NavItem = ({ to, label }) => (
  <Link
    to={to}
    style={{
      display: "block",
      padding: "12px",
      borderRadius: "10px",
      marginBottom: "10px",
      color: "#cbd5f5",
      textDecoration: "none",
      transition: "0.3s"
    }}
    onMouseEnter={(e) => (e.target.style.background = "#1e293b")}
    onMouseLeave={(e) => (e.target.style.background = "transparent")}
  >
    {label}
  </Link>
);

// 🔥 Sidebar Style
const sidebarStyle = {
  width: "230px",
  background: "#020617",
  padding: "20px",
  borderRight: "1px solid #1e293b"
};

function App() {
  return (
    <Router>
      <div
        style={{
          display: "flex",
          height: "100vh",
          background: "#020617",
          color: "white"
        }}
      >

        {/* SIDEBAR */}
        <div style={sidebarStyle}>
          <h2 style={{ marginBottom: "30px" }}>🚀 AI Career</h2>

          <NavItem to="/" label="🎤 Interview" />
          <NavItem to="/resume" label="📄 Resume Analyzer" />
          <NavItem to="/admin" label="📊 Admin Panel" />
        </div>

        {/* MAIN CONTENT */}
        <div style={{ flex: 1, overflow: "auto" }}>
          <Routes>
            <Route path="/" element={<Interview />} />
            <Route path="/resume" element={<ResumeAnalyzer />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </div>

      </div>
    </Router>
  );
}

export default App;