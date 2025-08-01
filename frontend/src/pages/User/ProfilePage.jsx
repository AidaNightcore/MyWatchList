import React, { useEffect, useState } from "react";
import { Box, Grid, CircularProgress } from "@mui/material";
import { useParams } from "react-router-dom"; // <-- esențial

import api from "../../services/api";
import ProfileHeader from "../../components/user/ProfileHeader";
import ProfileCharts from "../../components/user/ProfileCharts";
import ProfileRecents from "../../components/user/ProfileRecents";
import StatsOverview from "../../components/user/ProfileStats";
import FriendsList from "../../components/user/FriendsList";

export default function ProfilePage() {
  const { id } = useParams(); // <-- esențial, extrage "id" din url
  const userId = Number(id); // <-- folosește int dacă backend-ul tău cere int

  const [user, setUser] = useState(null);
  const [summary, setSummary] = useState(null);
  const [activity, setActivity] = useState([]);
  const [friends, setFriends] = useState([]);

  useEffect(() => {
    if (!userId) return; // protecție pentru cazuri fără id valid
    api.get(`/api/users/${userId}`).then((res) => setUser(res.data));
    api
      .get(`/api/users/profile-summary/${userId}`)
      .then((res) => setSummary(res.data));
    api
      .get(`/api/users/activity-history/${userId}`)
      .then((res) => setActivity(res.data));
    api
      .get(`/api/users/${userId}/relationships?type=friend`)
      .then((res) => setFriends(res.data));
  }, [userId]);

  if (!user || !summary) return <CircularProgress />;

  return (
    <Box p={3}>
      <ProfileHeader user={user} />
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={4}>
          <StatsOverview summary={summary} />
          <FriendsList friends={friends} />
        </Grid>
        <Grid item xs={12} md={8}>
          <ProfileCharts summary={summary} />
          <ProfileRecents activity={activity} />
        </Grid>
      </Grid>
    </Box>
  );
}
