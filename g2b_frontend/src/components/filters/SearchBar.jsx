// src/components/filters/SearchBar.jsx
import { TextField, InputAdornment } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

function SearchBar({ value, onChange, onSearch, placeholder = "검색..." }) {
  const handleKeyPress = (e) => {
    if (e.key === "Enter" && onSearch) {
      onSearch();
    }
  };

  return (
    <TextField
      size="small"
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      onKeyPress={handleKeyPress}
      InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <SearchIcon />
          </InputAdornment>
        ),
      }}
      sx={{ minWidth: 300 }}
    />
  );
}

export default SearchBar;
