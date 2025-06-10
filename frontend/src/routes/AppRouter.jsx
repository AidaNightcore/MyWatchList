import React from "react";
import { Routes, Route, Navigate, Outlet } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import AuthLayout from "../components/layout/AuthLayout";
import { useAuth } from "../contexts/AuthContext";

// Pages
import HomePage from "../pages/HomePage/HomePage";
import LoginPage from "../pages/Auth/LoginPage";
import RegisterPage from "../pages/Auth/RegisterPage";
import MediaListPage from "../pages/Media/MediaListPage";
import MediaDetailPage from "../pages/Media/MediaDetailPage";
import WatchlistPage from "../pages/User/WatchlistPage";
import ProfilePage from "../pages/User/ProfilePage";
import SearchPage from "../pages/SearchPage/SearchPage";
import ErrorPage from "../pages/ErrorPage";

// Protected route component
const ProtectedRoute = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};

// Main router component
const AppRouter = () => {
  return (
    <Routes>
      {/* Auth layout routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>

      {/* Main app layout */}
      <Route element={<AppLayout />}>
        {/* Public routes */}
        <Route index element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />

        {/* Media routes */}
        <Route path="/media">
          <Route index element={<MediaListPage />} />
          <Route path=":id" element={<MediaDetailPage />} />
        </Route>

        {/* Protected routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/watchlist" element={<WatchlistPage />} />
          <Route path="/profile/:username" element={<ProfilePage />} />
        </Route>

        {/* 404 route */}
        <Route path="*" element={<ErrorPage />} />
      </Route>
    </Routes>
  );
};

export default AppRouter;
