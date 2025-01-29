import React, { useState } from 'react';

    function Login({ onLogin }) {
      const [username, setUsername] = useState('');
      const [password, setPassword] = useState('');

      const handleSubmit = (e) => {
        e.preventDefault();
        onLogin(username, password);
      };

      return (
        <div className="login-container">
          <h2>Login</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Password:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit">Login</button>
          </form>
        </div>
      );
    }

    export default Login;
