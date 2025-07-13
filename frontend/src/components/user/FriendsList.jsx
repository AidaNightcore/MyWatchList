import React from "react";
import { Card, CardContent, Typography, Avatar, Stack } from "@mui/material";
import { Link } from "react-router-dom";

export default function FriendsList({ friends }) {
  const friendsArr = Array.isArray(friends) ? friends : [];
  return (
    <Card elevation={2} sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h6">Prieteni ({friendsArr.length})</Typography>
        <Stack direction="row" spacing={2}>
          {friendsArr.map((friend) => (
            <Link to={`/profile/${friend.id}`} key={friend.id}>
              <Avatar
                src={`/api/users/${friend.id}/profile-picture`}
                alt={friend.username}
                sx={{ width: 48, height: 48 }}
              />
            </Link>
          ))}
        </Stack>
      </CardContent>
    </Card>
  );
}
