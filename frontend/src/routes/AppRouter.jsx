import { BrowserRouter, Routes, Route } from "react-router-dom";
import AppLayout from "../components/layout/AppLayout";
import HomePage from "../pages/HomePage/HomePage";
import MediaListPage from "../pages/Media/MediaListPage";
import MediaDetailPage from "../pages/Media/MediaDetailPage";
import LoginPage from "../pages/Auth/LoginPage";
import WatchlistPage from "../pages/User/WatchlistPage";
import ProfilePage from "../pages/User/ProfilePage";

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<HomePage />} />

          {/* Media routes */}
          <Route path="media" element={<MediaListPage />} />
          <Route path="media/:id" element={<MediaDetailPage />} />

          {/* User routes */}
          <Route path="user/:username" element={<ProfilePage />} />
          <Route path="watchlist" element={<WatchlistPage />} />

          {/* Auth routes */}
          <Route path="login" element={<LoginPage />} />

          {/* Error route */}
          <Route path="*" element={<div>Page Not Found</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default AppRouter;
