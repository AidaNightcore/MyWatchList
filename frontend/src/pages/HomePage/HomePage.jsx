import React, { useEffect, useState } from "react";
import { Box, Typography, Button } from "@mui/material";
import { useAuth } from "../../contexts/AuthContext";
import api from "../../services/api";
import { useNavigate } from "react-router-dom";
import FeatureGrid from "../../components/homepage/FeatureGrid";
import MediaRow from "../../components/media/MediaRow";

export default function HomePage() {
  const { isAuthenticated, user } = useAuth();
  const navigate = useNavigate();

  const [userLists, setUserLists] = useState({
    movies: [],
    shows: [],
    books: [],
  });

  const [global, setGlobal] = useState({
    movies: [],
    shows: [],
    books: [],
    forumBoard: { Book: [], Movie: [], Show: [] },
  });

  useEffect(() => {
    let ignore = false;

    if (isAuthenticated && user) {
      api.get(`/api/watchlists/user/${user.id}`).then((res) => {
        if (ignore) return;
        // Flatten toate statusurile și tratează lipsă type!
        const allStatus = Object.values(res.data || {}).flat();
        // fallback dacă lipsește title sau type: NU crash-ui
        setUserLists({
          movies: allStatus.filter(
            (x) =>
              x.title && typeof x.title === "object" && x.title.type === "Movie"
          ),
          shows: allStatus.filter(
            (x) =>
              x.title && typeof x.title === "object" && x.title.type === "Show"
          ),
          books: allStatus.filter(
            (x) =>
              x.title && typeof x.title === "object" && x.title.type === "Book"
          ),
        });
      });
    }
    api.get("/api/social/topics/board").then((res) => {
      if (ignore) return;
      setGlobal((prev) => ({
        ...prev,
        forumBoard: res.data || { Book: [], Movie: [], Show: [] },
        movies: res.data.Movie || [],
        shows: res.data.Show || [],
        books: res.data.Book || [],
      }));
    });

    return () => {
      ignore = true;
    };
  }, [isAuthenticated, user]);

  return (
    <Box sx={{ bgcolor: "#f7f8fa", minHeight: "100vh", p: { xs: 0, md: 2 } }}>
      <Box sx={{ maxWidth: 1100, mx: "auto", pt: 4, pb: 6 }}>
        <Typography variant="h2" align="center" fontWeight={700} sx={{ mb: 1 }}>
          Track Your Favorite Movies, Shows and Books
        </Typography>
        <Typography variant="h5" align="center" sx={{ mb: 3, color: "#666" }}>
          Keep your lists in one place, see recommendations, synchronize, and
          join the community.
        </Typography>
        <Box sx={{ display: "flex", justifyContent: "center", mb: 3 }}>
          {!isAuthenticated && (
            <Button
              variant="contained"
              size="large"
              sx={{ borderRadius: 2, fontWeight: 600, px: 4 }}
              onClick={() => navigate("/signup")}
            >
              Create an Account
            </Button>
          )}
        </Box>
        {/* Media rows */}
        <Box sx={{ mb: 3 }}>
          <MediaRow
            title="Your movies"
            items={isAuthenticated ? userLists.movies : global.movies}
          />
          <MediaRow
            title="Your shows"
            items={isAuthenticated ? userLists.shows : global.shows}
          />
          <MediaRow
            title="Your books"
            items={isAuthenticated ? userLists.books : global.books}
          />
        </Box>
        {/* Feature grid & forum */}
        <FeatureGrid forumBoard={global.forumBoard} />
      </Box>
    </Box>
  );
}
