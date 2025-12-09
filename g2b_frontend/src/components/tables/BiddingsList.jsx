import { Paper, Typography, Box, Chip } from '@mui/material';

function BiddingsList({ biddings, formatAmount, total, onItemClick }) {

  return (
    <Paper sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">
          입찰공고 목록
        </Typography>
        <Typography variant="body2" color="text.secondary">
          총 {total.toLocaleString()}건
        </Typography>
      </Box>
      
      <Box>
        {biddings.length === 0 ? (
          <Typography color="text.secondary" textAlign="center" py={4}>
            검색 결과가 없습니다.
          </Typography>
        ) : (
          <>
            {biddings.map((bidding, index) => (
              <Box
                key={index}
                sx={{
                  py: 2,
                  px: 2,
                  borderBottom: index < biddings.length - 1 ? '1px solid #eee' : 'none',
                  cursor: 'pointer',
                  '&:hover': {
                    bgcolor: '#f5f5f5',
                  },
                  transition: 'background-color 0.2s',
                }}
                onClick={() => onItemClick(bidding)}
              >
                <Box display="flex" justifyContent="space-between" alignItems="start" mb={1}>
                  <Typography variant="subtitle1" fontWeight="bold" sx={{ flex: 1 }}>
                    {bidding.title}
                  </Typography>
                  <Box display="flex" gap={1} flexWrap="wrap">
                    <Chip
                      label={bidding.notice_type}
                      size="small"
                      color={
                        bidding.notice_type === '공사' ? 'error' :
                        bidding.notice_type === '용역' ? 'primary' : 'success'
                      }
                    />
                    {bidding.ai_category && (
                      <Chip
                        label={bidding.ai_category}
                        size="small"
                        variant="outlined"
                        color="info"
                      />
                    )}
                  </Box>
                </Box>
                <Box display="flex" gap={1} flexWrap="wrap" mb={1}>
                  {bidding.ai_tags && JSON.parse(bidding.ai_tags).map((tag, idx) => (
                    <Chip
                      key={idx}
                      label={tag}
                      size="small"
                      variant="filled"
                      sx={{
                        bgcolor: '#e3f2fd',
                        color: '#1976d2',
                        fontWeight: 'bold',
                        fontSize: '0.7rem'
                      }}
                    />
                  ))}
                </Box>
                <Box display="flex" gap={3} flexWrap="wrap">
                  <Typography variant="body2" color="text.secondary">
                    📍 {bidding.ordering_agency}
                  </Typography>
                  <Typography variant="body2" color="primary" fontWeight="bold">
                    💰 {formatAmount(bidding.budget_amount)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    📅 {bidding.notice_datetime?.substring(0, 10)}
                  </Typography>
                </Box>
              </Box>
            ))}
          </>
        )}
      </Box>
    </Paper>
  );
}

export default BiddingsList;
