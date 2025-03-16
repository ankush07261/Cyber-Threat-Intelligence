import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../css/login.css"; // Import CSS file

const Login = ({ setAuth }) => {
  const [credentials, setCredentials] = useState({
    username: "",
    password: "",
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(
        "http://localhost:8000/api/login",
        credentials
      );
      localStorage.setItem("token", response.data.token);
      setAuth(true);
      navigate("/dashboard");
    } catch (error) {
      setShowModal(true); // Show modal on wrong credentials
    }
  };

  return (
    <div className="login-container">
      <h1>Cyber Threat Intelligence</h1>
      <h2>Login</h2>
      <form onSubmit={handleLogin} className="login-form">
        <label>Username</label>
        <input
          type="text"
          value={credentials.username}
          onChange={(e) =>
            setCredentials({ ...credentials, username: e.target.value })
          }
          required
        />

        <label>Password</label>
        <div className="password-container">
          <input
            type={showPassword ? "text" : "password"}
            value={credentials.password}
            onChange={(e) =>
              setCredentials({ ...credentials, password: e.target.value })
            }
            required
          />
          <button
            className="toggle-password"
            type="button"
            onClick={() => setShowPassword(!showPassword)}
          >
            {showPassword ? "👁️" : "🙈"}
          </button>
        </div>

        <button type="submit" className="login-button">
          Login
        </button>
      </form>

      <p>
        Don't have an account? <a href="/register">Register</a>
      </p>

      {/* Error Modal */}
      {showModal && (
        <div className="error-modal">
          <p>❌ Invalid Credentials</p>
          <button onClick={() => setShowModal(false)}>OK</button>
        </div>
      )}
    </div>
  );
};

export default Login;
