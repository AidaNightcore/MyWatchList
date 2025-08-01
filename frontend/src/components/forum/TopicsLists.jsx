import { Stack, Typography, Box } from "@mui/material";
import TopicCard from "./TopicCard";

export default function TopicsList({ sectionTitle, topics }) {
  return (
    <Box sx={{ mb: 6 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        {sectionTitle}
      </Typography>
      <Stack spacing={3}>
        {topics.map((topic) => (
          <TopicCard
            key={topic.id}
            id={topic.id}
            title={topic.title}
            imgURL={topic.imgURL}
            firstReply={topic.firstReply}
            mediaId={topic.mediaId}
          />
        ))}
      </Stack>
    </Box>
  );
}
