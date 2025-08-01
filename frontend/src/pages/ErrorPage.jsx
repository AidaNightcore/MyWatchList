import React from "react";
import { Link, useLocation } from "react-router-dom";
import { Box, Button, Container, Typography } from "@mui/material";
import HomeIcon from "@mui/icons-material/Home";

export default function ErrorPage() {
  // Dacă ai transmis un mesaj de eroare cu navigate("/error", { state: { status, message } })
  const location = useLocation();
  const status = location.state?.status || "Error";
  const message =
    location.state?.message ||
    "Something went wrong or the page was not found.";

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "100vh",
          textAlign: "center",
          p: 3,
        }}
      >
        <Typography
          variant="h1"
          sx={{ fontSize: "5rem", fontWeight: 700, mb: 2 }}
        >
          {status}
        </Typography>

        <Typography variant="h4" sx={{ mb: 2 }}>
          {status === 404 ? "Oops! Page not found." : "Something went wrong!"}
        </Typography>

        <Typography variant="body1" sx={{ mb: 3 }}>
          {message}
        </Typography>

        <Button
          component={Link}
          to="/"
          variant="contained"
          startIcon={<HomeIcon />}
          size="large"
        >
          Go to Home
        </Button>
      </Box>
    </Container>
  );
}
