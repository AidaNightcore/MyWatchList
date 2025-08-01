import { Card, CardContent, Typography } from "@mui/material";
import { Link } from "react-router-dom";

function PublisherCard({ publisher }) {
  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography
          variant="h6"
          component={Link}
          to={`/publisher/${publisher.id}`}
          sx={{
            textDecoration: "none",
            color: "primary.main",
            "&:hover": { textDecoration: "underline" },
          }}
        >
          {publisher.name}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Books: {publisher.books.length} &nbsp;|&nbsp; Movies:{" "}
          {publisher.movies.length} &nbsp;|&nbsp; Shows:{" "}
          {publisher.shows.length}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default PublisherCard;
