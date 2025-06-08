import { Card, CardMedia, CardContent, Typography, Chip } from "@mui/material";
import { Link } from "react-router-dom";

const MediaCard = ({ media }) => {
  return (
    <Card
      sx={{
        maxWidth: 300,
        height: "100%",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <CardMedia
        component="img"
        height="140"
        image={media.image || "/placeholder.jpg"}
        alt={media.title}
      />
      <CardContent sx={{ flexGrow: 1 }}>
        <Typography gutterBottom variant="h6" component="div">
          <Link to={`/media/${media.id}`}>{media.title}</Link>
        </Typography>

        <div
          style={{
            display: "flex",
            gap: "8px",
            flexWrap: "wrap",
            marginBottom: "8px",
          }}
        >
          <Chip label={media.type} size="small" />
          <Chip label={`${media.releaseYear}`} size="small" />
        </div>

        <Typography variant="body2" color="text.secondary">
          {media.synopsis?.slice(0, 100)}...
        </Typography>
      </CardContent>
    </Card>
  );
};

export default MediaCard;
