import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import { PrimeReactProvider } from "primereact/api";
import { ThemeProvider } from "@mui/material/styles";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <PrimeReactProvider>
      <App />
    </PrimeReactProvider>
  </React.StrictMode>
);
