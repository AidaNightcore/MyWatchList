import React, { useState } from "react";
import { Box, Tabs, Tab, Paper } from "@mui/material";
import MediaAdminPanel from "../../components/dashboard/MediaAdminPanel";
import PublisherAdminPanel from "../../components/dashboard/PublisherAdminPanel";
import FranchiseAdminPanel from "../../components/dashboard/FranchiseAdminPanel";
import UserAdminPanel from "../../components/dashboard/UserAdminpanel";

export default function AdminDashboard() {
  const [tab, setTab] = useState(0);

  return (
    <Box sx={{ maxWidth: 1200, mx: "auto", py: 4 }}>
      <Paper sx={{ p: 2, mb: 3 }}>
        <Tabs value={tab} onChange={(_, t) => setTab(t)}>
          <Tab label="Users" />
          <Tab label="Media" />
          <Tab label="Publishers" />
          <Tab label="Franchises" />
        </Tabs>
      </Paper>
      {tab === 0 && <UserAdminPanel />}
      {tab === 1 && <MediaAdminPanel />}
      {tab === 2 && <PublisherAdminPanel />}
      {tab === 3 && <FranchiseAdminPanel />}
    </Box>
  );
}
