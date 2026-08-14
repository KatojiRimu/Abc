import React, { useState } from 'react';
import './Register.css';

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitted, setIsSubmitted] = useState(false);

  const registeruser = async (e) => {
    e.preventDefault();

    setErrorMessage("");
    const register_url = window.location.origin + "/djangoapp/register";

    try {
      const res = await fetch(register_url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          "username": userName,
          "password": password,
          "first_name": firstName,
          "last_name": lastName,
          "email": email
        }),
      });

      const json = await res.json();
      if (json.status === "Authenticated" || json.userName) {
        sessionStorage.setItem('username', json.userName);
        setIsSubmitted(true);
        window.location.href = "/";
      } else if (json.error === "Already Registered") {
        setErrorMessage("User already exists. Please choose a different username.");
      } else {
        setErrorMessage(json.message || "Registration failed. Please check your inputs.");
      }
    } catch (err) {
      setErrorMessage("Network error connecting to backend API.");
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h2 className="register-title">Create Account</h2>
        <p className="register-subtitle">Register to submit dealership reviews and rate vehicles.</p>

        {errorMessage && (
          <div className="alert-danger">
            {errorMessage}
          </div>
        )}

        {isSubmitted ? (
          <div className="alert-success">
            Registration successful! Redirecting to home...
          </div>
        ) : (
          <form onSubmit={registeruser} className="register-form">
            <div className="form-group">
              <label className="form-label">Username</label>
              <input
                type="text"
                name="username"
                placeholder="Enter username"
                className="form-input"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">First Name</label>
                <input
                  type="text"
                  name="first_name"
                  placeholder="Enter first name"
                  className="form-input"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Last Name</label>
                <input
                  type="text"
                  name="last_name"
                  placeholder="Enter last name"
                  className="form-input"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Email Address</label>
              <input
                type="email"
                name="email"
                placeholder="name@example.com"
                className="form-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Password</label>
              <input
                type="password"
                name="password"
                placeholder="••••••••"
                className="form-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="btn-submit">
              Register Account
            </button>
          </form>
        )}

        <div className="register-footer">
          Already have an account? <a href="/login/" className="link-highlight">Login here</a>
        </div>
      </div>
    </div>
  );
};

export default Register;
