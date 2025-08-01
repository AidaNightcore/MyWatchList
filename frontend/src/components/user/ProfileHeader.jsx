import React, { useState } from "react";
import {
  Card,
  CardContent,
  Avatar,
  Typography,
  Stack,
  Chip,
} from "@mui/material";
import { Button } from "primereact/button";

export default function ProfileHeader({ user }) {
  const [avatarSrc, setAvatarSrc] = useState(
    `/api/users/${user.id}/profile-picture`
  );
  return (
    <Card elevation={3}>
      <CardContent>
        <Stack direction="row" spacing={3} alignItems="center">
          <Avatar
            src={avatarSrc}
            onError={() => setAvatarSrc(null)}
            sx={{ width: 96, height: 96 }}
          >
            {/* fallback la prima literă din username sau un icon */}
            {user.username && user.username[0]?.toUpperCase()}
          </Avatar>
          <Stack>
            <Typography variant="h4">{user.name}</Typography>
            <Typography variant="subtitle1" color="text.secondary">
              @{user.username}
            </Typography>
            <Stack direction="row" spacing={1} mt={1}>
              {user.isAdmin && <Chip label="Admin" color="primary" />}
              {user.isModerator && <Chip label="Moderator" color="secondary" />}
            </Stack>
          </Stack>
          <Button
            label="Add Friend"
            icon="pi pi-user-plus"
            className="p-button-sm p-button-outlined"
          />
        </Stack>
      </CardContent>
    </Card>
  );
}
