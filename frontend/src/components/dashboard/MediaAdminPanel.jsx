import React, { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Tabs,
  Tab,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Button,
  TextField,
  MenuItem,
  Stack,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import api from "../../services/api";

const MEDIA_TYPES = [
  { value: "Book", label: "Book" },
  { value: "Movie", label: "Movie" },
  { value: "Show", label: "Show" },
];

const INITIAL_FORM = {
  title: "",
  description: "",
  publisherID: "",
  franchiseID: "",
  imgURL: "",
  publishDate: "",
  author: "",
  pages: "",
  duration: "",
  director: "",
};

export default function MediaAdminPanel() {
  const [type, setType] = useState("Book");
  const [media, setMedia] = useState([]);
  const [editId, setEditId] = useState(null);
  const [form, setForm] = useState(INITIAL_FORM);
  const [publishers, setPublishers] = useState([]);
  const [franchises, setFranchises] = useState([]);

  useEffect(() => {
    loadMedia();
    loadPublishers();
    loadFranchises();
    setEditId(null);
    setForm(INITIAL_FORM);
  }, [type]);

  const loadMedia = async () => {
    const { data } = await api.get(`/api/media/${type.toLowerCase()}s`);
    setMedia(data);
  };
  const loadPublishers = async () => {
    const { data } = await api.get(`/api/media/publishers?sort=name`);
    setPublishers(data);
  };
  const loadFranchises = async () => {
    const { data } = await api.get(`/api/media/franchises?sort=title`);
    setFranchises(data);
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this item?")) return;
    await api.delete(`/api/media/${type.toLowerCase()}s/${id}`);
    setMedia((lst) => lst.filter((m) => m.id !== id));
  };

  const handleEdit = (item) => {
    setEditId(item.id);
    setForm({
      ...INITIAL_FORM,
      ...item,
      publisherID: item.publisherID || "",
      franchiseID: item.franchiseID || "",
      publishDate: item.publishDate ? item.publishDate.slice(0, 10) : "",
    });
  };

  const handleSave = async () => {
    await api.put(`/api/media/${type.toLowerCase()}s/${editId}`, {
      ...form,
      pages: form.pages ? Number(form.pages) : null,
      duration: form.duration ? Number(form.duration) : null,
    });
    setEditId(null);
    setForm(INITIAL_FORM);
    loadMedia();
  };

  const handleCreate = async () => {
    await api.post(`/api/media/${type.toLowerCase()}s`, {
      ...form,
      pages: form.pages ? Number(form.pages) : null,
      duration: form.duration ? Number(form.duration) : null,
    });
    setForm(INITIAL_FORM);
    loadMedia();
  };

  const handleFranchise = async (mediaId, franchiseId) => {
    if (!franchiseId) return;
    // Implement asocieri dacă ai rută dedicată; altfel folosește edit.
    await api.put(`/api/media/${type.toLowerCase()}s/${mediaId}`, {
      ...media.find((m) => m.id === mediaId),
      franchiseID: franchiseId,
    });
    loadMedia();
  };

  // Form fields adaptive
  const renderFields = () => (
    <Stack
      direction="row"
      spacing={2}
      alignItems="center"
      sx={{ mb: 2, flexWrap: "wrap" }}
    >
      <TextField
        label="Title"
        value={form.title}
        required
        onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
        InputLabelProps={{ style: { color: "#111" } }}
        sx={{ minWidth: 170 }}
      />
      <TextField
        label="Description"
        value={form.description}
        onChange={(e) =>
          setForm((f) => ({ ...f, description: e.target.value }))
        }
        InputLabelProps={{ style: { color: "#111" } }}
        sx={{ minWidth: 170 }}
      />
      <TextField
        select
        label="Publisher"
        value={form.publisherID}
        onChange={(e) =>
          setForm((f) => ({ ...f, publisherID: e.target.value }))
        }
        sx={{ minWidth: 140 }}
        InputLabelProps={{ style: { color: "#111" } }}
      >
        <MenuItem value="">—</MenuItem>
        {publishers.map((p) => (
          <MenuItem key={p.id} value={p.id}>
            {p.name}
          </MenuItem>
        ))}
      </TextField>
      <TextField
        select
        label="Franchise"
        value={form.franchiseID}
        onChange={(e) =>
          setForm((f) => ({ ...f, franchiseID: e.target.value }))
        }
        sx={{ minWidth: 140 }}
        InputLabelProps={{ style: { color: "#111" } }}
      >
        <MenuItem value="">—</MenuItem>
        {franchises.map((f) => (
          <MenuItem key={f.id} value={f.id}>
            {f.title || f.name}
          </MenuItem>
        ))}
      </TextField>
      <TextField
        label="Image URL"
        value={form.imgURL}
        onChange={(e) => setForm((f) => ({ ...f, imgURL: e.target.value }))}
        InputLabelProps={{ style: { color: "#111" } }}
        sx={{ minWidth: 180 }}
      />
      <TextField
        label="Publish Date"
        type="date"
        value={form.publishDate}
        onChange={(e) =>
          setForm((f) => ({ ...f, publishDate: e.target.value }))
        }
        InputLabelProps={{ shrink: true, style: { color: "#111" } }}
        sx={{ minWidth: 160 }}
      />
      {type === "Book" && (
        <>
          <TextField
            label="Author"
            value={form.author}
            onChange={(e) => setForm((f) => ({ ...f, author: e.target.value }))}
            InputLabelProps={{ style: { color: "#111" } }}
            sx={{ minWidth: 150 }}
          />
          <TextField
            label="Pages"
            type="number"
            value={form.pages}
            onChange={(e) => setForm((f) => ({ ...f, pages: e.target.value }))}
            InputLabelProps={{ style: { color: "#111" } }}
            sx={{ minWidth: 120 }}
          />
        </>
      )}
      {type === "Movie" && (
        <>
          <TextField
            label="Director"
            value={form.director}
            onChange={(e) =>
              setForm((f) => ({ ...f, director: e.target.value }))
            }
            InputLabelProps={{ style: { color: "#111" } }}
            sx={{ minWidth: 150 }}
          />
          <TextField
            label="Duration (min)"
            type="number"
            value={form.duration}
            onChange={(e) =>
              setForm((f) => ({ ...f, duration: e.target.value }))
            }
            InputLabelProps={{ style: { color: "#111" } }}
            sx={{ minWidth: 130 }}
          />
        </>
      )}
      {type === "Show" && (
        <>
          <TextField
            label="Director"
            value={form.director}
            onChange={(e) =>
              setForm((f) => ({ ...f, director: e.target.value }))
            }
            InputLabelProps={{ style: { color: "#111" } }}
            sx={{ minWidth: 150 }}
          />
          <TextField
            label="Duration (min/ep)"
            type="number"
            value={form.duration}
            onChange={(e) =>
              setForm((f) => ({ ...f, duration: e.target.value }))
            }
            InputLabelProps={{ style: { color: "#111" } }}
            sx={{ minWidth: 130 }}
          />
        </>
      )}
    </Stack>
  );

  return (
    <Box sx={{ bgcolor: "#fafbfc", minHeight: "100vh", p: 2 }}>
      <Typography
        variant="h5"
        sx={{ mb: 2, color: "#1a2233", fontWeight: 600 }}
      >
        Media Management
      </Typography>
      <Tabs
        value={MEDIA_TYPES.findIndex((t) => t.value === type)}
        onChange={(_, t) => setType(MEDIA_TYPES[t].value)}
        sx={{ mb: 2 }}
        textColor="primary"
        indicatorColor="primary"
      >
        {MEDIA_TYPES.map((mt) => (
          <Tab
            label={mt.label}
            key={mt.value}
            sx={{ color: "#1a2233", fontWeight: 500 }}
          />
        ))}
      </Tabs>
      {/* Add/Edit Form */}
      <Box sx={{ mb: 2 }}>
        {renderFields()}
        <Button
          variant="contained"
          onClick={editId ? handleSave : handleCreate}
          color="primary"
          sx={{ fontWeight: 600 }}
        >
          {editId ? "Save" : "Add"}
        </Button>
        {editId && (
          <Button
            onClick={() => {
              setEditId(null);
              setForm(INITIAL_FORM);
            }}
            sx={{ ml: 2, color: "#222" }}
          >
            Cancel
          </Button>
        )}
      </Box>
      {/* Media List */}
      <List>
        {media.map((m) => (
          <ListItem
            key={m.id}
            sx={{
              bgcolor: "#fff",
              borderRadius: 2,
              boxShadow: 1,
              mb: 1,
              border: "1px solid #ececec",
            }}
            secondaryAction={
              <Stack direction="row" spacing={1}>
                <IconButton onClick={() => handleEdit(m)} color="primary">
                  <EditIcon />
                </IconButton>
                <IconButton onClick={() => handleDelete(m.id)} color="error">
                  <DeleteIcon />
                </IconButton>
                <TextField
                  select
                  label="Franchise"
                  value={m.franchiseID || ""}
                  onChange={(e) => handleFranchise(m.id, e.target.value)}
                  sx={{ minWidth: 120, ml: 2 }}
                  InputLabelProps={{ style: { color: "#111" } }}
                >
                  <MenuItem value="">None</MenuItem>
                  {franchises.map((f) => (
                    <MenuItem key={f.id} value={f.id}>
                      {f.title || f.name}
                    </MenuItem>
                  ))}
                </TextField>
              </Stack>
            }
          >
            <ListItemText
              primary={
                <span style={{ color: "#1a2233", fontWeight: 600 }}>
                  {`${m.title}${m.author ? ` — ${m.author}` : ""}`}
                </span>
              }
              secondary={
                <span style={{ color: "#2e3c55" }}>
                  {`ID: ${m.id}${
                    m.publisher ? `, Publisher: ${m.publisher}` : ""
                  }${m.franchise ? `, Franchise: ${m.franchise}` : ""}${
                    m.publishDate ? `, Published: ${m.publishDate}` : ""
                  }`}
                </span>
              }
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );
}
