import React from "react";
import { useRouteError, Link } from "react-router-dom";
import { Box, Button, Container, Typography } from "@mui/material";
import HomeIcon from "@mui/icons-material/Home";

const ErrorPage = () => {
  const error = useRouteError();
  console.error(error);

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
          {error.status || "Error"}
        </Typography>

        <Typography variant="h4" sx={{ mb: 2 }}>
          {error.status === 404
            ? "Oops! Page not found."
            : "Something went wrong!"}
        </Typography>

        <Typography variant="body1" sx={{ mb: 3 }}>
          {error.statusText || error.message}
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
};

export default ErrorPage;
