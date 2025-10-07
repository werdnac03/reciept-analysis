import { useState } from "react";
import { loginUser, registerUser } from "../lib/api/auth";
import { useAuth } from "../lib/auth";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");

    try {
      if (isLogin) {
        const res = await loginUser(username, password);
        if (res.error) return setMessage(res.error);
        if (!res.token) return setMessage("No token received");

        login(res.token);
        navigate("/receipts");
      } else {
        if (!email) return setMessage("Email is required");
        const res = await registerUser(email, username, password);
        if (res.error) return setMessage(res.error);

        setMessage("Registration successful! Please log in.");
        setIsLogin(true);
      }
    } catch (err) {
      console.error(err);
      setMessage("Server error. Please try again.");
    }
  };

return (
    <div className="d-flex align-items-center justify-content-center vh-100 bg-light">
      <div className="card shadow p-4" style={{ width: "400px" }}>
        <h2 className="text-center mb-4">
          {isLogin ? "Login" : "Register"}
        </h2>

        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="mb-3">
              <label className="form-label">Email</label>
              <input
                type="email"
                className="form-control"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          )}

          <div className="mb-3">
            <label className="form-label">Username</label>
            <input
              type="text"
              className="form-control"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="mb-4">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary w-100 mb-3"
          >
            {isLogin ? "Login" : "Register"}
          </button>
        </form>

        {message && (
          <div className="alert alert-info text-center py-2" role="alert">
            {message}
          </div>
        )}

        <div className="text-center">
          <button
            type="button"
            onClick={() => {
              setIsLogin(!isLogin);
              setMessage("");
            }}
            className="btn btn-link text-decoration-none"
          >
            {isLogin
              ? "Need an account? Register here"
              : "Already have an account? Login here"}
          </button>
        </div>
      </div>
    </div>
  );
}
