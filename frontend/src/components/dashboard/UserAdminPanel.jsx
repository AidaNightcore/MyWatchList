import React, { useState } from "react";
import {
  Box,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Typography,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import api from "../../services/api";

export default function UserAdminPanel() {
  const [query, setQuery] = useState("");
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    try {
      const { data } = await api.get(
        `/api/users/search?q=${encodeURIComponent(query)}`
      );
      setUsers(data);
    } catch {
      setError("Failed to search users.");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this user?")) return;
    await api.delete(`/api/users/${id}`);
    setUsers((u) => u.filter((us) => us.id !== id));
  };

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2 }}>
        User Management
      </Typography>
      <Box sx={{ display: "flex", gap: 2, mb: 2 }}>
        <TextField
          label="Search by username"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button variant="contained" onClick={handleSearch}>
          Search
        </Button>
      </Box>
      <List>
        {users.map((u) => (
          <ListItem
            key={u.id}
            secondaryAction={
              <IconButton
                edge="end"
                onClick={() => handleDelete(u.id)}
                color="error"
              >
                <DeleteIcon />
              </IconButton>
            }
          >
            <ListItemText
              primary={`${u.username} (${u.name})`}
              secondary={`ID: ${u.id}`}
            />
          </ListItem>
        ))}
      </List>
      {error && <Typography color="error">{error}</Typography>}
    </Box>
  );
}
