import { Paper, Typography, Box, Pagination, Chip } from '@mui/material';

function BiddingsList({ biddings, formatAmount, total, page, limit, onPageChange, onItemClick }) {
  const totalPages = Math.ceil(total / limit);

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
                  <Chip 
                    label={bidding.notice_type} 
                    size="small" 
                    color={
                      bidding.notice_type === '공사' ? 'error' :
                      bidding.notice_type === '용역' ? 'primary' : 'success'
                    }
                    sx={{ ml: 2 }}
                  />
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

            {/* 페이징 */}
            <Box display="flex" justifyContent="center" mt={3}>
              <Pagination 
                count={totalPages} 
                page={page} 
                onChange={(e, value) => onPageChange(value)}
                color="primary"
                showFirstButton
                showLastButton
              />
            </Box>
          </>
        )}
      </Box>
    </Paper>
  );
}

export default BiddingsList;
