import React from "react";
import GenreAutocomplete from "../Autocomplete/GenreAutocomplete";
import PublisherAutocomplete from "../Autocomplete/PublisherAutocomplete";
import FranchiseAutocomplete from "../Autocomplete/FranchiseAutocomplete";
import { Dropdown } from "primereact/dropdown";
import Box from "@mui/material/Box";

const typeOptions = [
  { label: "All", value: "" },
  { label: "Book", value: "Book" },
  { label: "Movie", value: "Movie" },
  { label: "Show", value: "Show" },
];

export default function MediaFilterBar({
  genre,
  setGenre,
  publisher,
  setPublisher,
  mediaType,
  setMediaType,
  franchise,
  setFranchise,
}) {
  return (
    <Box
      sx={{
        display: "flex",
        flexWrap: "wrap",
        gap: 2,
        mb: 3,
        alignItems: "center",
        justifyContent: { xs: "center", sm: "flex-start" },
      }}
    >
      <GenreAutocomplete value={genre} onChange={setGenre} />
      <PublisherAutocomplete value={publisher} onChange={setPublisher} />
      <FranchiseAutocomplete value={franchise} onChange={setFranchise} />
      <Dropdown
        value={mediaType}
        options={typeOptions}
        onChange={(e) => setMediaType(e.value)}
        placeholder="Type"
        style={{ minWidth: 160 }}
        showClear
      />
    </Box>
  );
}
