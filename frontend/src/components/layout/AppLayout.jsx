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
    <Box
      sx={{
        display: "flex",
        minHeight: "100vh",
        flexDirection: "column",
        width: "100vw", // Full viewport width
        overflowX: "hidden", // Prevent scrollbars if needed
      }}
    >
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
          width: "100vw", // Ensure main takes full viewport width
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Toolbar />
        <Box
          sx={{
            flexGrow: 1,
            p: { xs: 2, sm: 3 },
            width: "100vw", // Ensure inner container is also full width
            maxWidth: "100vw", // Prevent accidental maxWidth restriction
            boxSizing: "border-box",
          }}
        >
          <Outlet />
        </Box>
      </Box>
      <Footer />
    </Box>
  );
};

export default AppLayout;
