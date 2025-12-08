// src/components/OrderPlanDetailModal.jsx
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Divider,
  Chip,
  Grid,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import IconButton from "@mui/material/IconButton";

function OrderPlanDetailModal({ open, onClose, plan, formatAmount }) {
  if (!plan) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box display="flex" alignItems="center" gap={2}>
            <Typography variant="h6">발주계획 상세</Typography>
            <Chip
              label={plan.prcrmnt_methd || "미분류"}
              size="small"
              color="warning"
            />
          </Box>
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>

      <DialogContent dividers>
        <Box sx={{ py: 2 }}>
          <Typography variant="h6" gutterBottom sx={{ mb: 3, fontWeight: "bold" }}>
            {plan.biz_nm || '사업명 없음'}
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                발주계획번호
              </Typography>
              <Typography variant="body1" sx={{ fontWeight: 500 }}>
                {plan.order_plan_unty_no || '-'}
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                발주년월
              </Typography>
              <Typography variant="body1">
                {plan.order_year}년 {plan.order_mnth}월
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                발주기관
              </Typography>
              <Typography variant="body1">
                {plan.order_instt_nm || '-'}
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                발주예정금액
              </Typography>
              <Typography variant="h6" color="primary" sx={{ fontWeight: "bold" }}>
                {formatAmount(plan.sum_order_amt)}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                조달방법
              </Typography>
              <Typography variant="body1">
                {plan.prcrmnt_methd || '-'}
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                공고일자
              </Typography>
              <Typography variant="body1">
                {plan.ntice_dt?.substring(0, 10) || '-'}
              </Typography>
            </Grid>
          </Grid>
        </Box>
      </DialogContent>

      <DialogActions sx={{ px: 3, py: 2 }}>
        <Button onClick={onClose} variant="contained" size="large">
          닫기
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default OrderPlanDetailModal;
