import React, { useEffect, useState, useRef } from "react";
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  Avatar,
  Stack,
  Divider,
  CircularProgress,
  Alert,
} from "@mui/material";
import api from "../../services/api";
import { useAuth } from "../../contexts/AuthContext";

export default function SettingsPage() {
  const { user, logout } = useAuth();
  const [profile, setProfile] = useState({});
  const [loading, setLoading] = useState(true);
  const [edit, setEdit] = useState({});
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState({});
  const fileInputRef = useRef();

  useEffect(() => {
    if (!user) return;
    api.get(`/api/users/${user.id}`).then((res) => {
      setProfile(res.data);
      setEdit({
        name: res.data.name || "",
        email: res.data.email || "",
        username: res.data.username || "",
      });
      setLoading(false);
    });
  }, [user]);

  // Poza de profil
  const handleProfilePicUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setErrors({});
    setSuccess({});
    const formData = new FormData();
    formData.append("file", file);
    try {
      await api.put(`/api/users/${user.id}/profile-picture`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSuccess((s) => ({ ...s, picture: "Profile picture updated" }));
      // Refresh fără reload, doar imaginea:
      setProfile((p) => ({ ...p, profilePicture: Date.now() }));
    } catch {
      setErrors((e) => ({ ...e, picture: "Failed to upload picture" }));
    }
  };

  // Update generic (nume, email, username, parola)
  const handleFieldUpdate = async (field, value, endpoint, payload = {}) => {
    setErrors({});
    setSuccess({});
    try {
      await api.put(`/api/users/${user.id}/${endpoint}`, {
        [field]: value,
        ...payload,
      });
      setSuccess((s) => ({ ...s, [field]: "Updated" }));
      setProfile((p) => ({ ...p, [field]: value }));
    } catch (err) {
      setErrors((e) => ({
        ...e,
        [field]:
          err?.response?.data?.error ||
          err?.response?.data?.errors?.[0] ||
          "Failed",
      }));
    }
  };

  // Stergere cont
  const handleDeleteAccount = async () => {
    if (
      !window.confirm(
        "Are you sure you want to permanently delete your account? This cannot be undone."
      )
    )
      return;
    setLoading(true);
    try {
      await api.delete(`/api/users/${user.id}`);
      logout(); // logout context
      window.location.href = "/";
    } catch {
      setErrors((e) => ({ ...e, delete: "Failed to delete account" }));
    }
    setLoading(false);
  };

  if (loading)
    return <CircularProgress sx={{ mt: 6, mx: "auto", display: "block" }} />;

  return (
    <Box sx={{ maxWidth: 600, mx: "auto", py: 4 }}>
      <Typography variant="h4" fontWeight={700} sx={{ mb: 3 }}>
        Account Settings
      </Typography>

      {/* Profile picture */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Stack direction="row" spacing={3} alignItems="center">
          <Avatar
            sx={{ width: 90, height: 90 }}
            src={
              profile.profilePicture
                ? `/api/users/${user.id}/profile-picture?${profile.profilePicture}`
                : undefined
            }
          />
          <Button
            variant="outlined"
            onClick={() => fileInputRef.current.click()}
          >
            Change Picture
          </Button>
          <input
            type="file"
            accept="image/*"
            hidden
            ref={fileInputRef}
            onChange={handleProfilePicUpload}
          />
        </Stack>
        {success.picture && <Alert severity="success">{success.picture}</Alert>}
        {errors.picture && <Alert severity="error">{errors.picture}</Alert>}
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography fontWeight={600} sx={{ mb: 1 }}>
          Change name
        </Typography>
        <Stack direction="row" spacing={2}>
          <TextField
            label="Name"
            value={edit.name}
            onChange={(e) => setEdit((s) => ({ ...s, name: e.target.value }))}
            sx={{ flex: 1 }}
          />
          <Button
            variant="contained"
            onClick={() => handleFieldUpdate("name", edit.name, "name")}
          >
            Update
          </Button>
        </Stack>
        {success.name && <Alert severity="success">{success.name}</Alert>}
        {errors.name && <Alert severity="error">{errors.name}</Alert>}
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography fontWeight={600} sx={{ mb: 1 }}>
          Change username
        </Typography>
        <Stack direction="row" spacing={2}>
          <TextField
            label="Username"
            value={edit.username}
            onChange={(e) =>
              setEdit((s) => ({ ...s, username: e.target.value }))
            }
            sx={{ flex: 1 }}
          />
          <Button
            variant="contained"
            onClick={() =>
              handleFieldUpdate("username", edit.username, "username")
            }
          >
            Update
          </Button>
        </Stack>
        {success.username && (
          <Alert severity="success">{success.username}</Alert>
        )}
        {errors.username && <Alert severity="error">{errors.username}</Alert>}
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography fontWeight={600} sx={{ mb: 1 }}>
          Change email
        </Typography>
        <Stack direction="row" spacing={2}>
          <TextField
            label="Email"
            type="email"
            value={edit.email}
            onChange={(e) => setEdit((s) => ({ ...s, email: e.target.value }))}
            sx={{ flex: 1 }}
          />
          <Button
            variant="contained"
            onClick={() => handleFieldUpdate("email", edit.email, "email")}
          >
            Update
          </Button>
        </Stack>
        {success.email && <Alert severity="success">{success.email}</Alert>}
        {errors.email && <Alert severity="error">{errors.email}</Alert>}
      </Paper>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography fontWeight={600} sx={{ mb: 1 }}>
          Change password
        </Typography>
        <Stack direction="row" spacing={2}>
          <TextField
            label="New password"
            type="password"
            value={edit.password || ""}
            onChange={(e) =>
              setEdit((s) => ({ ...s, password: e.target.value }))
            }
            sx={{ flex: 1 }}
          />
          <Button
            variant="contained"
            onClick={() =>
              handleFieldUpdate("password", edit.password, "password")
            }
          >
            Update
          </Button>
        </Stack>
        {success.password && (
          <Alert severity="success">{success.password}</Alert>
        )}
        {errors.password && <Alert severity="error">{errors.password}</Alert>}
      </Paper>

      <Divider sx={{ my: 4 }} />

      <Paper sx={{ p: 3, bgcolor: "#ffebee" }}>
        <Typography color="error" fontWeight={700} sx={{ mb: 1 }}>
          Danger Zone
        </Typography>
        <Button
          variant="outlined"
          color="error"
          onClick={handleDeleteAccount}
          disabled={loading}
        >
          Delete account
        </Button>
        {errors.delete && <Alert severity="error">{errors.delete}</Alert>}
      </Paper>
    </Box>
  );
}
