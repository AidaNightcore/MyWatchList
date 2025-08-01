import React, { useState } from "react";
import { useAuth } from "../../contexts/AuthContext";
import { useAuthStore } from "../../store/authStore";
import { useNavigate } from "react-router-dom";
import {
  Container,
  TextField,
  Button,
  Box,
  Typography,
  CircularProgress,
} from "@mui/material";

const LoginPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login, isLoading, error } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    await login({ email, password });
    // Redirect dacă login-ul a reușit
    if (useAuthStore.getState().user) {
      navigate("/");
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          mt: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography variant="h4" component="h1" gutterBottom>
          Sign in to MediaTracker
        </Typography>

        {error && (
          <Typography color="error" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}

        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{ mt: 1, width: "100%" }}
        >
          <TextField
            margin="normal"
            required
            fullWidth
            label="Email Address"
            autoComplete="email"
            autoFocus
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <TextField
            margin="normal"
            required
            fullWidth
            label="Password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={isLoading}
            sx={{ mt: 3, mb: 2 }}
          >
            {isLoading ? <CircularProgress size={24} /> : "Sign In"}
          </Button>

          <Button
            fullWidth
            variant="outlined"
            onClick={() => navigate("/register")}
            sx={{ mt: 1 }}
          >
            Create new account
          </Button>
        </Box>
      </Box>
    </Container>
  );
};

export default LoginPage;
