import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  IconButton,
  TextField,
  Button,
  Stack,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import api from "../../services/api";

export default function PublisherAdminPanel() {
  const [publishers, setPublishers] = useState([]);
  const [form, setForm] = useState({ name: "" });

  const loadPublishers = async () => {
    const { data } = await api.get(`/api/media/publishers?sort=name`);
    setPublishers(data);
  };

  useEffect(() => {
    loadPublishers();
  }, []);

  const handleAdd = async () => {
    await api.post(`/api/media/publishers`, form);
    setForm({ name: "" });
    loadPublishers();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this publisher?")) return;
    await api.delete(`/api/media/publishers/${id}`);
    setPublishers((lst) => lst.filter((p) => p.id !== id));
  };

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Publishers
      </Typography>
      <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
        <TextField
          label="Publisher name"
          value={form.name}
          onChange={(e) => setForm({ name: e.target.value })}
        />
        <Button variant="contained" onClick={handleAdd}>
          Add
        </Button>
      </Stack>
      <List>
        {publishers.map((p) => (
          <ListItem
            key={p.id}
            secondaryAction={
              <IconButton onClick={() => handleDelete(p.id)} color="error">
                <DeleteIcon />
              </IconButton>
            }
          >
            <ListItemText primary={p.name} secondary={`ID: ${p.id}`} />
          </ListItem>
        ))}
      </List>
    </Box>
  );
}
