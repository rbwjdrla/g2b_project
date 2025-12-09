import React from "react";
import { Box, TextField, Typography } from "@mui/material";

const BudgetFilter = ({ minBudget, maxBudget, onMinChange, onMaxChange }) => {
  const formatNumber = (value) => {
    if (!value) return "";
    return value.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  };

  const parseNumber = (value) => {
    return value.replace(/,/g, "");
  };

  const handleMinChange = (e) => {
    const value = parseNumber(e.target.value);
    if (value === "" || /^\d+$/.test(value)) {
      onMinChange(value);
    }
  };

  const handleMaxChange = (e) => {
    const value = parseNumber(e.target.value);
    if (value === "" || /^\d+$/.test(value)) {
      onMaxChange(value);
    }
  };

  return (
    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
      <Typography variant="body2" sx={{ minWidth: 60 }}>
        예산 범위
      </Typography>
      <TextField
        size="small"
        placeholder="최소 (원)"
        value={formatNumber(minBudget)}
        onChange={handleMinChange}
        sx={{ width: 150 }}
      />
      <Typography variant="body2">~</Typography>
      <TextField
        size="small"
        placeholder="최대 (원)"
        value={formatNumber(maxBudget)}
        onChange={handleMaxChange}
        sx={{ width: 150 }}
      />
    </Box>
  );
};

export default BudgetFilter;
