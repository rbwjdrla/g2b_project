import { Paper, Typography, Box } from "@mui/material";

function BiddingsList({ biddings, formatAmount }) {
  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        최근 입찰공고
      </Typography>
      <Box>
        {biddings.length === 0 ? (
          <Typography color="text.secondary">데이터가 없습니다.</Typography>
        ) : (
          biddings.map((bidding, index) => (
            <Box
              key={index}
              sx={{
                py: 2,
                borderBottom:
                  index < biddings.length - 1 ? "1px solid #eee" : "none",
              }}
            >
              <Typography variant="subtitle1" fontWeight="bold">
                {bidding.title}
              </Typography>
              <Box display="flex" gap={2} mt={1}>
                <Typography variant="body2" color="text.secondary">
                  {bidding.notice_type || "-"}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {bidding.ordering_agency}
                </Typography>
                <Typography variant="body2" color="primary">
                  {formatAmount(bidding.budget_amount)}
                </Typography>
              </Box>
            </Box>
          ))
        )}
      </Box>
    </Paper>
  );
}

export default BiddingsList;
