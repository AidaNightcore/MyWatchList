import {
  Card,
  CardContent,
  Typography,
  Divider,
  Avatar,
  Box,
} from "@mui/material";
import { Link as RouterLink, useNavigate } from "react-router-dom";

export default function TopicCard({
  id, // id-ul topicului
  title,
  imgURL,
  firstReply,
  mediaId, // id-ul media asociat
}) {
  const navigate = useNavigate();

  const handleCardClick = (e) => {
    // Dacă s-a dat click pe linkul de titlu, nu naviga la topic (lasă să meargă către media)
    if (
      e.target.tagName === "A" &&
      e.target.getAttribute("data-mediatitlelink") === "1"
    ) {
      return;
    }
    navigate(`/forum/${id}`);
  };

  return (
    <Card
      variant="outlined"
      sx={{
        display: "flex",
        p: 2,
        gap: 2,
        cursor: "pointer",
        transition: "box-shadow 0.2s",
        "&:hover": { boxShadow: 4, background: "#f9f9f9" },
      }}
      onClick={handleCardClick}
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          handleCardClick(e);
        }
      }}
    >
      <Avatar
        variant="rounded"
        src={imgURL}
        alt={title}
        sx={{ width: 100, height: 140, mr: 2 }}
      />
      <CardContent sx={{ flex: 1 }}>
        <Typography variant="h6">
          <RouterLink
            to={`/media/${mediaId}`}
            data-mediatitlelink="1"
            style={{
              textDecoration: "none",
              color: "inherit",
              transition: "color 0.2s",
            }}
            onMouseOver={(e) => (e.target.style.color = "#1976d2")}
            onMouseOut={(e) => (e.target.style.color = "inherit")}
            onClick={(e) => e.stopPropagation()} // NU declanșa click pe card
          >
            {title}
          </RouterLink>
        </Typography>
        <Divider sx={{ my: 1 }} />
        <Typography variant="subtitle2" sx={{ color: "primary.main" }}>
          What do you think about it?
        </Typography>
        {firstReply && (
          <Box sx={{ mt: 1, bgcolor: "#f5f5f5", p: 1, borderRadius: 2 }}>
            <Typography variant="body2">{firstReply}</Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}
