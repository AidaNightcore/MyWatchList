import React, { useEffect, useState } from "react";
import { Container, Typography, CircularProgress } from "@mui/material";
import TopicsBoard from "../../components/forum/TopicsBoard";

import axios from "axios";

export default function ForumPage() {
  const [topicsByType, setTopicsByType] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("/api/social/topics/board").then((res) => {
      setTopicsByType(res.data); // structurează backend-ul să trimită { Book: [...], Movie: [...], Show: [...] }
      setLoading(false);
    });
  }, []);

  return (
    <Container maxWidth="md" sx={{ py: 6 }}>
      <Typography variant="h3" align="center" gutterBottom>
        Forum
      </Typography>
      <Typography
        variant="body1"
        align="center"
        color="text.secondary"
        sx={{ mb: 4 }}
      >
        Discuții organizate pe cărți, filme și seriale.
      </Typography>
      {loading ? (
        <CircularProgress sx={{ display: "block", mx: "auto", my: 10 }} />
      ) : (
        <TopicsBoard topicsByType={topicsByType} />
      )}
    </Container>
  );
}
