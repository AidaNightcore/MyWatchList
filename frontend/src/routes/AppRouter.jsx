import React from "react";
import { Routes, Route, Navigate, Outlet } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import AuthLayout from "../components/layout/AuthLayout";
import { useAuth } from "../contexts/AuthContext";
import AdminRoute from "./AdminRoute";
import ModeratorRoute from "./ModeratorRoute";

// Pages
import HomePage from "../pages/HomePage/HomePage";
import LoginPage from "../pages/Auth/LoginPage";
import RegisterPage from "../pages/Auth/RegisterPage";
import MediaListPage from "../pages/Media/MediaListPage";
import MediaDetailPage from "../pages/Media/MediaDetailPage";
import WatchlistPage from "../pages/User/WatchlistPage";
import ProfilePage from "../pages/User/ProfilePage";
import RecommendationsPage from "../pages/RecommendationsPage/RecommendationsPage";
import ErrorPage from "../pages/ErrorPage";
import AdminDashboard from "../pages/User/AdminDashboard";
import ModeratorDashboard from "../pages/User/ModeratorDashboard";
import ForumPage from "../pages/Social/ForumPage";
import TopicPage from "../pages/Social/TopicPage";
import FranchisePage from "../pages/Media/FranchisePage";
import PublisherPage from "../pages/Media/PublisherPage";
import SettingsPage from "../pages/User/SettingsPage";
import ProposeMediaFormPage from "../pages/Media/ProposeMediaFormPage";
import { MediaProvider } from "../contexts/MediaContext";
import { WatchlistProvider } from "../contexts/WatchlistContext";
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
      {/* Layout de autentificare */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>

      {/* Layout principal */}

      <Route element={<AppLayout />}>
        {/* Public */}
        <Route index element={<HomePage />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
        <Route
          element={
            <WatchlistProvider>
              <Outlet />
            </WatchlistProvider>
          }
        >
          <Route
            path="/media"
            element={
              <MediaProvider>
                <WatchlistProvider>
                  <Outlet />
                </WatchlistProvider>
              </MediaProvider>
            }
          >
            <Route index element={<MediaListPage />} />
            <Route path=":titleId" element={<MediaDetailPage />} />
          </Route>
          <Route path="/watchlist" element={<WatchlistPage />} />
        </Route>
        <Route path="/franchise" element={<FranchisePage />} />
        <Route path="/publisher" element={<PublisherPage />} />
        {/* Forum */}
        <Route path="/forum">
          <Route index element={<ForumPage />} />
          <Route path=":topicId" element={<TopicPage />} />
        </Route>
        {/* Profil public – vizibil oricui */}
        <Route path="/profile/:username" element={<ProfilePage />} />

        {/* Propunere media (doar user logat) */}
        <Route element={<ProtectedRoute />}>
          <Route path="/propose-media" element={<ProposeMediaFormPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>

        {/* Admin/moderator */}
        <Route element={<AdminRoute />}>
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
        </Route>
        {/* Admin/moderator */}
        <Route element={<ModeratorRoute />}>
          <Route path="/moderator/dashboard" element={<ModeratorDashboard />} />
        </Route>

        <Route path="*" element={<ErrorPage />} />
      </Route>
    </Routes>
  );
};

export default AppRouter;
