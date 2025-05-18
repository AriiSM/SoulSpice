import { useState } from "react";
import { registerUser } from "../api/api";
import "./Auth.css";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
      await registerUser({ username, password });
      setMessage("User created! You can now log in.");
    } catch (err) {
      setError(`Registration failed.`);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1 className="auth-title">Create an account</h1>
        <p className="auth-subtitle">Start your SoulSpice journey.</p>

        <form onSubmit={handleRegister} className="auth-form">
          <input
            type="text"
            className="auth-input"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            className="auth-input"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" className="auth-button">
            Register
          </button>
        </form>

        {message && <p style={{color: "green", textAlign: "center" }}>{message}</p>}
        {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
        <a href="/" className="auth-link">
          Already have an account? Login
        </a>
      </div>
    </div>
  );
}
