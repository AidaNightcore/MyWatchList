// src/pages/User/ModeratorDashboard.jsx
import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Paper,
  Stack,
  CircularProgress,
  Alert,
  Link as MuiLink,
} from "@mui/material";
import { Link } from "react-router-dom";
import api from "../../services/api";

export default function ModeratorDashboard() {
  const [reports, setReports] = useState([]);
  const [details, setDetails] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState();

  // Fetch all reports at mount
  useEffect(() => {
    setLoading(true);
    api
      .get("/api/social/reports")
      .then((res) => setReports(res.data))
      .catch(() => setError("Failed to fetch reports."))
      .finally(() => setLoading(false));
  }, []);

  // Pentru fiecare raport, fetch reply details & user details
  useEffect(() => {
    async function fetchDetails() {
      let newDetails = {};
      for (const report of reports) {
        // Fetch reply details
        let reply = null,
          topic = null;
        if (report.reply_id) {
          try {
            // Poți folosi direct /api/social/topics/<topic_id>/replies
            const replyRes = await api.get(
              `/api/social/replies/${report.reply_id}`
            );
            reply = replyRes.data;
            // Extrage topicul (presupunând că reply conține topicID)
            if (reply.topicID) {
              try {
                const topicRes = await api.get(
                  `/api/social/topics/${reply.topicID}`
                );
                topic = topicRes.data;
              } catch {
                topic = null;
              }
            }
          } catch {
            reply = null;
          }
        }
        // Fetch usernames
        let reporter = null,
          reported = null;
        try {
          if (report.reporter_id)
            reporter = (await api.get(`/api/users/${report.reporter_id}`)).data;
        } catch {}
        try {
          if (report.reported_user_id)
            reported = (await api.get(`/api/users/${report.reported_user_id}`))
              .data;
        } catch {}

        newDetails[report.id] = { reply, topic, reporter, reported };
      }
      setDetails(newDetails);
    }
    if (reports.length > 0) fetchDetails();
  }, [reports]);

  return (
    <Box sx={{ maxWidth: 900, mx: "auto", py: 4 }}>
      <Typography variant="h4" fontWeight={700} sx={{ mb: 3 }}>
        Moderator Dashboard
      </Typography>
      {loading && <CircularProgress />}
      {error && <Alert severity="error">{error}</Alert>}
      {!loading && !error && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" fontWeight={600} sx={{ mb: 2 }}>
            Reported Messages
          </Typography>
          {reports.length === 0 && (
            <Typography color="text.secondary">No reports found.</Typography>
          )}
          <Stack spacing={3}>
            {reports.map((report) => {
              const det = details[report.id] || {};
              return (
                <Paper
                  key={report.id}
                  sx={{
                    p: 2,
                    borderLeft: "4px solid #f44336",
                    bgcolor: "#fff8f7",
                  }}
                  variant="outlined"
                >
                  <Typography fontWeight={600}>
                    Message:{" "}
                    <span style={{ color: "#f44336" }}>
                      {det.reply?.message || <i>Deleted or unavailable</i>}
                    </span>
                  </Typography>
                  <Typography>
                    Topic:{" "}
                    {det.reply?.topicID ? (
                      <MuiLink
                        component={Link}
                        to={`/forum/${det.reply.topicID}`}
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {det.topic?.title || `Topic #${det.reply.topicID}`}
                      </MuiLink>
                    ) : (
                      <i>Unknown</i>
                    )}
                  </Typography>
                  <Typography>
                    Reporter:{" "}
                    <b>{det.reporter?.username || report.reporter_id}</b> |
                    Reported user:{" "}
                    <b>{det.reported?.username || report.reported_user_id}</b>
                  </Typography>
                  {report.created_at && (
                    <Typography variant="caption" color="text.secondary">
                      Reported at:{" "}
                      {new Date(report.created_at).toLocaleString()}
                    </Typography>
                  )}
                </Paper>
              );
            })}
          </Stack>
        </Paper>
      )}
    </Box>
  );
}
