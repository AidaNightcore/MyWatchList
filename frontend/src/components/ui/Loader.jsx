import React from "react";
import { Box, CircularProgress } from "@mui/material";

const Loader = ({ fullScreen = false }) => {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: fullScreen ? "100vh" : "100%",
        width: fullScreen ? "100vw" : "100%",
        position: fullScreen ? "fixed" : "relative",
        top: 0,
        left: 0,
        zIndex: 1300,
        backgroundColor: fullScreen
          ? "rgba(255, 255, 255, 0.7)"
          : "transparent",
      }}
    >
      <CircularProgress size={fullScreen ? 80 : 40} />
    </Box>
  );
};

export default Loader;
