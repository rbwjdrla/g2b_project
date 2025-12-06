import { Paper, Typography, Box, Pagination, Chip } from '@mui/material';

function AwardsList({ awards, formatAmount, total, page, limit, onPageChange, onItemClick }) {
  const totalPages = Math.ceil(total / limit);

  return (
    <Paper sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">
          낙찰정보 목록
        </Typography>
        <Typography variant="body2" color="text.secondary">
          총 {total.toLocaleString()}건
        </Typography>
      </Box>
      
      <Box>
        {awards.length === 0 ? (
          <Typography color="text.secondary" textAlign="center" py={4}>
            검색 결과가 없습니다.
          </Typography>
        ) : (
          <>
            {awards.map((award, index) => (
              <Box
                key={index}
                sx={{
                  py: 2,
                  px: 2,
                  borderBottom: index < awards.length - 1 ? '1px solid #eee' : 'none',
                  cursor: 'pointer',
                  '&:hover': {
                    bgcolor: '#f5f5f5',
                  },
                  transition: 'background-color 0.2s',
                }}
                onClick={() => onItemClick(award)}
              >
                <Box display="flex" justifyContent="space-between" alignItems="start" mb={1}>
                  <Typography variant="subtitle1" fontWeight="bold" sx={{ flex: 1 }}>
                    {award.title}
                  </Typography>
                  <Chip 
                    label={award.notice_type} 
                    size="small" 
                    color={
                      award.notice_type === '공사' ? 'error' :
                      award.notice_type === '용역' ? 'primary' : 'success'
                    }
                    sx={{ ml: 2 }}
                  />
                </Box>
                <Box display="flex" gap={3} flexWrap="wrap">
                  <Typography variant="body2" color="text.secondary">
                    🏆 {award.contractor_name || '업체명 없음'}
                  </Typography>
                  <Typography variant="body2" color="primary" fontWeight="bold">
                    💰 {formatAmount(award.contract_amount)}
                  </Typography>
                  <Typography variant="body2" color="success.main">
                    📊 낙찰률: {award.winning_rate ? `${award.winning_rate}%` : '-'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    📅 {award.contract_date?.substring(0, 10)}
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

export default AwardsList;
