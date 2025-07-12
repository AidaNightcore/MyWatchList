import { Card, CardMedia, CardContent, Typography } from "@mui/material";
import StarIcon from "@mui/icons-material/Star";
import { Link } from "react-router-dom";

const POSTER_RATIO = 1.5; // 2:3 (w:h) poster ratio, adică height = width * 1.5

const MediaCard = ({ media }) => {
  // Extrage anul din publishDate
  const year = media.publishDate
    ? new Date(media.publishDate).getFullYear()
    : "";

  return (
    <Card
      sx={{
        width: {
          xs: 130, // telefoane
          sm: 150, // tablete mici
          md: 180, // desktop mic
          lg: 220, // desktop mare
        },
        display: "flex",
        flexDirection: "column",
        borderRadius: 2,
        overflow: "hidden",
        boxShadow: 2,
        background: "#fff",
        height: {
          xs: 130 * POSTER_RATIO + 100,
          sm: 150 * POSTER_RATIO + 110,
          md: 180 * POSTER_RATIO + 120,
          lg: 220 * POSTER_RATIO + 130,
        },
      }}
    >
      <CardMedia
        component="img"
        image={media.image_url || media.image || "/placeholder.jpg"}
        alt={media.title}
        sx={{
          width: "100%",
          height: {
            xs: 130 * POSTER_RATIO,
            sm: 150 * POSTER_RATIO,
            md: 180 * POSTER_RATIO,
            lg: 220 * POSTER_RATIO,
          },
          objectFit: "cover",
          backgroundColor: "#ddd",
        }}
      />
      <CardContent
        sx={{
          flex: 1,
          p: 1.5,
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-start",
          background: "#fff",
        }}
      >
        <Typography
          variant="subtitle1"
          sx={{
            fontWeight: "bold",
            mb: 0.5,
            color: "#181818",
            lineHeight: 1.15,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
          component={Link}
          to={`/media/${media.id}`}
          style={{ textDecoration: "none" }}
        >
          {media.title}
        </Typography>
        <Typography sx={{ fontSize: 14, color: "#222", mb: 0.2 }}>
          {media.type}
          {media.score !== undefined && (
            <>
              &nbsp;
              <StarIcon
                sx={{
                  fontSize: 16,
                  verticalAlign: "middle",
                  color: "#f5c518",
                  ml: 0.5,
                  mb: "2px",
                }}
              />
              {parseFloat(media.score).toFixed(1)}
            </>
          )}
        </Typography>
        <Typography sx={{ fontSize: 13, color: "#222" }}>{year}</Typography>
      </CardContent>
    </Card>
  );
};

export default MediaCard;
