import { Box, TextField } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import dayjs from "dayjs";

function DateRangeFilter({
  startDate,
  endDate,
  onStartDateChange,
  onEndDateChange,
}) {
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Box display="flex" gap={2}>
        <DatePicker
          label="시작일"
          value={startDate}
          onChange={onStartDateChange}
          format="YYYY-MM-DD"
          slotProps={{ textField: { size: "small" } }}
        />
        <DatePicker
          label="종료일"
          value={endDate}
          onChange={onEndDateChange}
          format="YYYY-MM-DD"
          slotProps={{ textField: { size: "small" } }}
        />
      </Box>
    </LocalizationProvider>
  );
}

export default DateRangeFilter;
