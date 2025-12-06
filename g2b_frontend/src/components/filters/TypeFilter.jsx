import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";

function TypeFilter({ value, onChange }) {
  return (
    <FormControl size="small" sx={{ minWidth: 120 }}>
      <InputLabel>유형</InputLabel>
      <Select value={value} onChange={onChange} label="유형">
        <MenuItem value="">전체</MenuItem>
        <MenuItem value="공사">공사</MenuItem>
        <MenuItem value="용역">용역</MenuItem>
        <MenuItem value="물품">물품</MenuItem>
      </Select>
    </FormControl>
  );
}

export default TypeFilter;
