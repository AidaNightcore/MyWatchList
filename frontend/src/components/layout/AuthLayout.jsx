import React from "react";
import { Outlet } from "react-router-dom";
import { Box, Container, CssBaseline } from "@mui/material";
import { styled } from "@mui/material/styles";

const AuthLayoutContainer = styled(Box)({
  display: "flex",
  minHeight: "100vh",
  alignItems: "center",
  justifyContent: "center",
  backgroundColor: "#f5f7fa",
});

const AuthCard = styled(Box)(({ theme }) => ({
  width: "100%",
  maxWidth: 450,
  padding: theme.spacing(4),
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.background.paper,
  boxShadow: theme.shadows[3],
}));

const AuthLayout = () => {
  return (
    <AuthLayoutContainer>
      <CssBaseline />
      <Container maxWidth="sm">
        <AuthCard>
          <Outlet />{" "}
          {/* This renders the child routes (LoginPage, RegisterPage) */}
        </AuthCard>
      </Container>
    </AuthLayoutContainer>
  );
};

export default AuthLayout;
