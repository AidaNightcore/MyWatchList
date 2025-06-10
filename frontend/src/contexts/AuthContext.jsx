import React, { createContext, useContext, useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import api from "../services/api";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  // Initialize authentication state
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        setIsLoading(true);
        const accessToken = localStorage.getItem("access_token");

        if (!accessToken) {
          setIsLoading(false);
          return;
        }

        // Verify token validity
        const response = await api.get("/auth/me");
        setUser(response.data);
        setIsAuthenticated(true);
      } catch (err) {
        console.error("Authentication check failed", err);
        handleLogout();
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();
  }, []);

  // Handle login
  const login = async (credentials) => {
    try {
      setIsLoading(true);
      setError(null);

      const response = await api.post("/auth/login", credentials);
      const { access_token, refresh_token, user } = response.data;

      // Store tokens
      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);

      // Update state
      setUser(user);
      setIsAuthenticated(true);

      // Redirect to requested page or home
      const origin = location.state?.from?.pathname || "/";
      navigate(origin);

      return { success: true };
    } catch (err) {
      console.error("Login failed", err);
      setError(err.response?.data?.error || "Login failed. Please try again.");
      return { success: false, error: err.response?.data?.error };
    } finally {
      setIsLoading(false);
    }
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    setIsAuthenticated(false);
    navigate("/login");
  };

  // Value to provide to consumers
  const value = {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout: handleLogout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
