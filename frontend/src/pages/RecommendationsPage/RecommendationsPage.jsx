import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Button,
  TextField,
  Stack,
  CircularProgress,
  Divider,
} from "@mui/material";
import { useAuth } from "../../contexts/AuthContext";
import api from "../../services/api";

export default function RecommendationsPage() {
  const { isAuthenticated, user } = useAuth();
  const [loading, setLoading] = useState(false);
  const [userRecs, setUserRecs] = useState({});
  const [searchTitle, setSearchTitle] = useState("");
  const [searchType, setSearchType] = useState("show");
  const [searchResults, setSearchResults] = useState(null);
  const [error, setError] = useState(null);

  // Fetch recs for logged-in user (last 5 completed)
  useEffect(() => {
    if (!isAuthenticated || !user) return;
    setLoading(true);
    api
      .get(`/api/media/${user.id}/dashboard/recommendations`)
      .then((res) => setUserRecs(res.data || {}))
      .catch(() => setUserRecs({}))
      .finally(() => setLoading(false));
  }, [isAuthenticated, user]);

  // Handler for manual recommendation search
  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSearchResults(null);
    if (!searchTitle.trim()) {
      setError("Enter a title");
      setLoading(false);
      return;
    }
    try {
      const { data } = await api.get("/api/media/recommendations", {
        params: { title: searchTitle.trim(), type: searchType, limit: 10 },
      });
      setSearchResults(data);
    } catch (err) {
      setError("No recommendations found.");
    }
    setLoading(false);
  };

  function renderTasteDiveRecs(recs) {
    if (!recs?.Similar?.Results?.length)
      return (
        <Typography color="text.secondary">No recommendations.</Typography>
      );
    return (
      <Stack spacing={1} sx={{ mt: 1 }}>
        {recs.Similar.Results.map((r, idx) => (
          <Paper key={r.Name + idx} variant="outlined" sx={{ p: 1 }}>
            <Typography fontWeight={600}>{r.Name}</Typography>
            {r.Type && (
              <Typography variant="caption" color="text.secondary">
                {r.Type}
              </Typography>
            )}
            {r.wTeaser && (
              <Typography variant="body2" sx={{ mt: 0.5 }}>
                {r.wTeaser}
              </Typography>
            )}
            {r.wUrl && (
              <Button
                href={r.wUrl}
                target="_blank"
                rel="noopener noreferrer"
                size="small"
                sx={{ mt: 1 }}
              >
                More info
              </Button>
            )}
          </Paper>
        ))}
      </Stack>
    );
  }

  return (
    <Box sx={{ maxWidth: 950, mx: "auto", py: 5, px: { xs: 1, md: 4 } }}>
      <Typography variant="h3" fontWeight={700} align="center" sx={{ mb: 3 }}>
        Recommendations
      </Typography>

      {/* User personalized recs */}
      {isAuthenticated && (
        <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
          <Typography variant="h5" fontWeight={600} sx={{ mb: 2 }}>
            Personalized recommendations
          </Typography>
          {loading ? (
            <CircularProgress />
          ) : Object.keys(userRecs).length > 0 ? (
            <Stack spacing={3}>
              {Object.entries(userRecs).map(([title, rec]) => (
                <Box key={title}>
                  <Typography variant="subtitle1" fontWeight={500}>
                    Based on <b>{title}</b>
                  </Typography>
                  {rec.error ? (
                    <Typography color="error">{rec.error}</Typography>
                  ) : (
                    renderTasteDiveRecs(rec)
                  )}
                </Box>
              ))}
            </Stack>
          ) : (
            <Typography color="text.secondary">
              No completed items found for recommendations.
            </Typography>
          )}
        </Paper>
      )}

      {/* Divider */}
      <Divider sx={{ mb: 4 }}>or</Divider>

      {/* Manual search */}
      <Paper elevation={2} sx={{ p: 3, mb: 2 }}>
        <Typography variant="h5" fontWeight={600} sx={{ mb: 2 }}>
          Search recommendations by title
        </Typography>
        <form onSubmit={handleSearch}>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={2} mb={2}>
            <TextField
              label="Title"
              value={searchTitle || ""}
              onChange={(e) => setSearchTitle(e.target.value)}
              required
              sx={{ flex: 2 }}
            />
            <TextField
              label="Type"
              select
              value={searchType}
              onChange={(e) => setSearchType(e.target.value)}
              SelectProps={{ native: true }}
              sx={{ flex: 1, minWidth: 100 }}
            >
              <option value="show">Show</option>
              <option value="movie">Movie</option>
              <option value="book">Book</option>
              <option value="music">Music</option>
              <option value="author">Author</option>
              <option value="game">Game</option>
            </TextField>
            <Button
              variant="contained"
              type="submit"
              sx={{ px: 4, fontWeight: 600 }}
              disabled={loading}
            >
              Search
            </Button>
          </Stack>
        </form>
        {error && <Typography color="error">{error}</Typography>}
        {loading && !userRecs && <CircularProgress />}
        {searchResults && (
          <Box sx={{ mt: 2 }}>{renderTasteDiveRecs(searchResults)}</Box>
        )}
      </Paper>
    </Box>
  );
}
