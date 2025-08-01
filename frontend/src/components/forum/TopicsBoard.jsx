import { Box } from "@mui/material";
import TopicsList from "./TopicsLists";

export default function TopicsBoard({ topicsByType }) {
  return (
    <Box
      sx={{
        width: "100%",
        py: 0,
        display: "flex",
        flexDirection: "row",
        gap: 4,
        alignItems: "flex-start",
        "flex-wrap": "wrap",
      }}
    >
      {["Book", "Show", "Movie"].map((type) => (
        <Box key={type} sx={{ flex: 1, minWidth: "30vw" }}>
          <TopicsList
            sectionTitle={type + "s"}
            topics={topicsByType[type] || []}
          />
        </Box>
      ))}
    </Box>
  );
}
