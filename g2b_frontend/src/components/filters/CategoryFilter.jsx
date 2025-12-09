import React from "react";
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";

const CategoryFilter = ({ value, onChange }) => {
  const categories = [
    { value: "", label: "전체 카테고리" },
    { value: "IT", label: "IT" },
    { value: "건설", label: "건설" },
    { value: "용역", label: "용역" },
    { value: "물품", label: "물품" },
    { value: "교육", label: "교육" },
    { value: "의료", label: "의료" },
    { value: "청소", label: "청소" },
    { value: "보안", label: "보안" },
    { value: "인쇄", label: "인쇄" },
    { value: "운송", label: "운송" },
    { value: "기타", label: "기타" },
  ];

  return (
    <FormControl size="small" sx={{ minWidth: 150 }}>
      <InputLabel>카테고리</InputLabel>
      <Select
        value={value}
        label="카테고리"
        onChange={(e) => onChange(e.target.value)}
      >
        {categories.map((cat) => (
          <MenuItem key={cat.value} value={cat.value}>
            {cat.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default CategoryFilter;
