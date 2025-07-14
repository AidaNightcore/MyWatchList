import { Card, CardContent, Typography } from "@mui/material";
import { Link } from "react-router-dom";

function FranchiseCard({ franchise }) {
  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Typography
          variant="h6"
          component={Link}
          to={`/franchise/${franchise.id}`}
          sx={{
            textDecoration: "none",
            color: "primary.main",
            "&:hover": { textDecoration: "underline" },
          }}
        >
          {franchise.name}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Books: {franchise.books.length} &nbsp;|&nbsp; Movies:{" "}
          {franchise.movies.length} &nbsp;|&nbsp; Shows:{" "}
          {franchise.shows.length}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default FranchiseCard;
