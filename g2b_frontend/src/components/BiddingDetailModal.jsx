import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Divider,
  Grid
} from '@mui/material';

function BiddingDetailModal({ open, onClose, bidding, formatAmount }) {
  if (!bidding) return null;

  const InfoRow = ({ label, value }) => (
    <Grid container spacing={2} sx={{ py: 1 }}>
      <Grid item xs={4}>
        <Typography variant="body2" color="text.secondary" fontWeight="bold">
          {label}
        </Typography>
      </Grid>
      <Grid item xs={8}>
        <Typography variant="body2">{value || '-'}</Typography>
      </Grid>
    </Grid>
  );

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Typography variant="h6">{bidding.title}</Typography>
      </DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 2 }}>
          <InfoRow label="공고번호" value={bidding.notice_number} />
          <InfoRow label="유형" value={bidding.notice_type} />
          <InfoRow label="발주기관" value={bidding.ordering_agency} />
          <InfoRow label="수요기관" value={bidding.demand_agency} />
          <Divider sx={{ my: 2 }} />
          
          <InfoRow label="예산금액" value={formatAmount(bidding.budget_amount)} />
          <InfoRow label="기초금액" value={formatAmount(bidding.basic_amount)} />
          <Divider sx={{ my: 2 }} />
          
          <InfoRow label="입찰방식" value={bidding.bidding_method} />
          <InfoRow label="계약방법" value={bidding.contract_method} />
          <InfoRow label="공동수급" value={bidding.joint_delivery} />
          <Divider sx={{ my: 2 }} />
          
          <InfoRow label="공고일시" value={bidding.notice_datetime} />
          <InfoRow label="입찰마감" value={bidding.bid_close_datetime} />
          <InfoRow label="개찰일시" value={bidding.bid_open_datetime} />
          <Divider sx={{ my: 2 }} />
          
          <Typography variant="body2" color="text.secondary" fontWeight="bold" gutterBottom>
            사업내용
          </Typography>
          <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', mt: 1 }}>
            {bidding.project_description || '내용 없음'}
          </Typography>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>닫기</Button>
      </DialogActions>
    </Dialog>
  );
}

export default BiddingDetailModal;
