import React, { useState, useEffect } from 'react';
    import { Routes, Route, useNavigate } from 'react-router-dom';
    import axios from 'axios';
    import Login from './components/Login';
    import Dashboard from './components/Dashboard';

    const API_BASE_URL = 'https://localhost/Api/V8';

    function App() {
      const [token, setToken] = useState(localStorage.getItem('token') || null);
      const navigate = useNavigate();

      useEffect(() => {
        if (token) {
          localStorage.setItem('token', token);
        } else {
          localStorage.removeItem('token');
        }
      }, [token]);


      const handleLogin = async (username, password) => {
        try {
          const response = await axios.post(`${API_BASE_URL}/login`, { username, password });
          setToken(response.data.token);
          navigate('/dashboard');
        } catch (error) {
          console.error('Login failed:', error);
          alert('Login failed. Please check your credentials.');
        }
      };

      const handleLogout = () => {
        setToken(null);
        navigate('/');
      };

      const authAxios = axios.create({
        baseURL: API_BASE_URL,
        headers: {
          Authorization: token ? `Bearer ${token}` : '',
        },
      });

      return (
        <div className="App">
          <Routes>
            <Route path="/" element={<Login onLogin={handleLogin} />} />
            <Route
              path="/dashboard"
              element={
                token ? (
                  <Dashboard authAxios={authAxios} onLogout={handleLogout} />
                ) : (
                  <Login onLogin={handleLogin} />
                )
              }
            />
          </Routes>
        </div>
      );
    }

    export default App;
