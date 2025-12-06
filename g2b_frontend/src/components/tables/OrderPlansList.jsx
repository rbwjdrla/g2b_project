import { Paper, Typography, Box, Pagination, Chip } from '@mui/material';

function OrderPlansList({ plans, formatAmount, total, page, limit, onPageChange, onItemClick }) {
  const totalPages = Math.ceil(total / limit);

  return (
    <Paper sx={{ p: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h5">
          발주계획 목록
        </Typography>
        <Typography variant="body2" color="text.secondary">
          총 {total.toLocaleString()}건
        </Typography>
      </Box>
      
      <Box>
        {plans.length === 0 ? (
          <Typography color="text.secondary" textAlign="center" py={4}>
            검색 결과가 없습니다.
          </Typography>
        ) : (
          <>
            {plans.map((plan, index) => (
              <Box
                key={index}
                sx={{
                  py: 2,
                  px: 2,
                  borderBottom: index < plans.length - 1 ? '1px solid #eee' : 'none',
                  cursor: 'pointer',
                  '&:hover': {
                    bgcolor: '#f5f5f5',
                  },
                  transition: 'background-color 0.2s',
                }}
                onClick={() => onItemClick(plan)}
              >
                <Box display="flex" justifyContent="space-between" alignItems="start" mb={1}>
                  <Typography variant="subtitle1" fontWeight="bold" sx={{ flex: 1 }}>
                    {plan.biz_nm || '사업명 없음'}
                  </Typography>
                  <Chip 
                    label={plan.prcrmnt_methd || '미분류'} 
                    size="small" 
                    color="warning"
                    sx={{ ml: 2 }}
                  />
                </Box>
                <Box display="flex" gap={3} flexWrap="wrap">
                  <Typography variant="body2" color="text.secondary">
                    📍 {plan.order_instt_nm || '-'}
                  </Typography>
                  <Typography variant="body2" color="primary" fontWeight="bold">
                    💰 {formatAmount(plan.sum_order_amt)}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    📅 {plan.order_year}년 {plan.order_mnth}월
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

export default OrderPlansList;
