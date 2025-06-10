import React, { useState } from "react";
import {
  TextField,
  InputAdornment,
  IconButton,
  Paper,
  Popper,
  List,
  ListItem,
  ListItemText,
  ClickAwayListener,
} from "@mui/material";
import { Search as SearchIcon, Close as CloseIcon } from "@mui/icons-material";

const SearchBar = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [anchorEl, setAnchorEl] = useState(null);
  const [results, setResults] = useState([]);

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearchTerm(value);

    // Mock search results
    if (value.length > 2) {
      setResults([
        { id: 1, title: "Inception", type: "movie" },
        { id: 2, title: "The Lord of the Rings", type: "book" },
        { id: 3, title: "Stranger Things", type: "show" },
      ]);
      setAnchorEl(e.currentTarget);
    } else {
      setResults([]);
      setAnchorEl(null);
    }
  };

  const handleClear = () => {
    setSearchTerm("");
    setResults([]);
    setAnchorEl(null);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl) && results.length > 0;

  return (
    <Box sx={{ position: "relative" }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Search movies, shows, books..."
        value={searchTerm}
        onChange={handleSearch}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
          endAdornment: searchTerm && (
            <InputAdornment position="end">
              <IconButton onClick={handleClear}>
                <CloseIcon fontSize="small" />
              </IconButton>
            </InputAdornment>
          ),
          sx: {
            borderRadius: 4,
            bgcolor: "background.paper",
            height: 40,
          },
        }}
      />

      <Popper
        open={open}
        anchorEl={anchorEl}
        placement="bottom-start"
        sx={{ zIndex: 1300, width: anchorEl?.clientWidth }}
      >
        <ClickAwayListener onClickAway={handleClose}>
          <Paper elevation={3} sx={{ mt: 1, width: "100%" }}>
            <List>
              {results.map((result) => (
                <ListItem
                  key={result.id}
                  button
                  component="a"
                  href={`/media/${result.id}`}
                  onClick={handleClose}
                >
                  <ListItemText
                    primary={result.title}
                    secondary={
                      result.type.charAt(0).toUpperCase() + result.type.slice(1)
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </ClickAwayListener>
      </Popper>
    </Box>
  );
};

export default SearchBar;
