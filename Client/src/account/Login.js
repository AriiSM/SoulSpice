import { useState } from "react";
import { loginUser } from "../api/api";
import { useContext } from "react";
import { UserContext } from "../UserContext";
import { useNavigate } from 'react-router-dom';
import "./Auth.css";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { setUserId } = useContext(UserContext);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const data = await loginUser({ username, password });
      // console.log("Login successful, user_id:", data.user_id);
      setUserId(data.user_id);
      navigate('/dashboard');
    } catch (err) {
      setError("Invalid username or password!");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1 className="auth-title">Login to SoulSpice</h1>
        <p className="auth-subtitle">Please enter your username and password.</p>

        <form onSubmit={handleLogin} className="auth-form">
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
            Login
          </button>
        </form>

        {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}

        <a href="/register" className="auth-link">
          Don't have an account? Register
        </a>
      </div>
    </div>
  );
}
