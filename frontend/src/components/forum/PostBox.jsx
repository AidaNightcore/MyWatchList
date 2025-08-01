import { Box, Typography, Avatar, Divider, Stack } from "@mui/material";
import { useAuth } from "../../contexts/AuthContext";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import ReportIcon from "@mui/icons-material/Report";
import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";

export default function PostBox({
  post,
  index,
  isStarter,
  onEdit = () => {},
  onDelete = () => {},
  onReport = () => {},
}) {
  if (!post) return null;
  const { user, isAuthenticated } = useAuth();

  const isOwn = user && post.userID === user.id;

  return (
    <Box
      id={`reply-${post.id}`} // Acum fiecare reply are id unic pentru scroll
      sx={{
        bgcolor: "#242424",
        borderRadius: 1,
        mb: 2,
        boxShadow: 2,
        display: "flex",
        border: "1px solid #353535",
      }}
    >
      {/* User info (left column) */}
      <Box
        sx={{
          p: 2,
          minWidth: 160,
          bgcolor: "#1b1b1b",
          borderRight: "1px solid #353535",
        }}
      >
        <Avatar
          src={post.user?.profilePicture || undefined}
          alt={post.user?.username || "User"}
          sx={{ width: 64, height: 64, mb: 1, mx: "auto" }}
        />
        <Typography
          variant="subtitle1"
          align="center"
          fontWeight="bold"
          color="#6ad0fe"
        >
          {post.user?.username || "Anonymous"}
        </Typography>
        <Typography variant="body2" align="center" color="gray">
          {post.user?.lastLogin
            ? `Last online: ${formatDate(post.user.lastLogin)}`
            : "Last online: —"}
        </Typography>
        <Typography variant="body2" align="center" color="gray" sx={{ mt: 1 }}>
          Joined: {post.user?.joinedDate || "—"}
        </Typography>
        {/* <Typography variant="body2" align="center" color="gray">
          Posts: {post.user?.posts || "—"}
        </Typography> */}
      </Box>
      {/* Message (right column) */}
      <Box sx={{ flex: 1, p: 2 }}>
        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography variant="body2" color="gray">
            {formatDate(post.createdAt || post.date)}
          </Typography>
          <Typography variant="body2" color="gray">
            #{index}
          </Typography>
        </Stack>
        <Divider sx={{ my: 1, borderColor: "#353535" }} />
        <Typography
          variant="body1"
          sx={{ color: "#ddd", whiteSpace: "pre-line" }}
        >
          {post.message || post.question || ""}
        </Typography>
        {/* Optional imagine în post */}
        {post.image && (
          <Box sx={{ mt: 2 }}>
            <img
              src={post.image}
              alt="post attachment"
              style={{ maxWidth: 360, borderRadius: 4 }}
            />
          </Box>
        )}
        <Stack direction="row" spacing={3} sx={{ mt: 2 }} alignItems="center">
          {isAuthenticated && isOwn && (
            <>
              <Tooltip title="Edit">
                <IconButton
                  color="primary"
                  size="small"
                  onClick={() => onEdit(post)}
                >
                  <EditIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Delete">
                <IconButton
                  color="error"
                  size="small"
                  onClick={() => onDelete(post)}
                >
                  <DeleteIcon />
                </IconButton>
              </Tooltip>
            </>
          )}
          {isAuthenticated && !isOwn && (
            <Tooltip title="Report">
              <IconButton
                color="warning"
                size="small"
                onClick={() => onReport(post)}
              >
                <ReportIcon />
              </IconButton>
            </Tooltip>
          )}
        </Stack>
      </Box>
    </Box>
  );
}

function formatDate(date) {
  if (!date) return "";
  const d = new Date(date);
  return d.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
