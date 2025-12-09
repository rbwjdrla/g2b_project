import React from "react";
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";

const CompetitionFilter = ({ value, onChange }) => {
  const levels = [
    { value: "", label: "전체" },
    { value: "저", label: "저 (경쟁 낮음)" },
    { value: "중", label: "중 (보통)" },
    { value: "고", label: "고 (경쟁 치열)" },
  ];

  return (
    <FormControl size="small" sx={{ minWidth: 150 }}>
      <InputLabel>경쟁 강도</InputLabel>
      <Select
        value={value}
        label="경쟁 강도"
        onChange={(e) => onChange(e.target.value)}
      >
        {levels.map((level) => (
          <MenuItem key={level.value} value={level.value}>
            {level.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default CompetitionFilter;
