import {
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";

function TopAgenciesTable({ agencies, formatAmount }) {
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        발주 TOP 5 기관
      </Typography>
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>순위</TableCell>
              <TableCell>기관명</TableCell>
              <TableCell align="right">공고 건수</TableCell>
              <TableCell align="right">총 예산</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {agencies.slice(0, 5).map((agency, index) => (
              <TableRow key={index}>
                <TableCell>{index + 1}</TableCell>
                <TableCell>{agency.agency}</TableCell>
                <TableCell align="right">
                  {agency.count.toLocaleString()}건
                </TableCell>
                <TableCell align="right">
                  {formatAmount(agency.total_budget)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}

export default TopAgenciesTable;
