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

export default function FranchiseAdminPanel() {
  const [franchises, setFranchises] = useState([]);
  const [form, setForm] = useState({ title: "" }); 

  const loadFranchises = async () => {
    const { data } = await api.get(`/api/media/franchises?sort=title`);
    setFranchises(data);
  };

  useEffect(() => {
    loadFranchises();
  }, []);

  const handleAdd = async () => {
    await api.post(`/api/admin/franchises`, form); 
    setForm({ title: "" });
    loadFranchises();
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this franchise?")) return;
    await api.delete(`/api/admin/franchises/${id}`); 
    setFranchises((lst) => lst.filter((p) => p.id !== id));
  };

  return (
    <Box>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Franchises
      </Typography>
      <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
        <TextField
          label="Franchise name"
          value={form.title}
          onChange={(e) => setForm({ title: e.target.value })}
        />
        <Button variant="contained" onClick={handleAdd}>
          Add
        </Button>
      </Stack>
      <List>
        {franchises.map((f) => (
          <ListItem
            key={f.id}
            secondaryAction={
              <IconButton onClick={() => handleDelete(f.id)} color="error">
                <DeleteIcon />
              </IconButton>
            }
          >
            <ListItemText primary={f.title} secondary={`ID: ${f.id}`} />
          </ListItem>
        ))}
      </List>
    </Box>
  );
}
