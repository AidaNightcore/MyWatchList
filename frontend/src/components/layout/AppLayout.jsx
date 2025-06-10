import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import {
  Box,
  CssBaseline,
  Toolbar,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import Navbar from "./Navbar";
import Footer from "./Footer";

const drawerWidth = 240;

const AppLayout = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", flexDirection: "column" }}>
      <CssBaseline />
      <Navbar
        drawerWidth={drawerWidth}
        handleDrawerToggle={handleDrawerToggle}
      />

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Toolbar /> {/* Spacer for fixed navbar */}
        {/* Page content */}
        <Box
          sx={{
            flexGrow: 1,
            p: { xs: 2, sm: 3 },
            maxWidth: "1400px",
            width: "100%",
            margin: "0 auto",
          }}
        >
          <Outlet /> {/* This renders the child routes */}
        </Box>
      </Box>
      <Footer />
    </Box>
  );
};

export default AppLayout;
