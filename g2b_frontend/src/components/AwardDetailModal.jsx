// src/components/AwardDetailModal.jsx
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

function AwardDetailModal({ open, onClose, award, formatAmount }) {
  if (!award) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box display="flex" alignItems="center" gap={2}>
            <Typography variant="h6">낙찰정보 상세</Typography>
            <Chip
              label={award.notice_type || "용역"}
              size="small"
              color="primary"
            />
          </Box>
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>

      <DialogContent dividers>
        <Box sx={{ py: 2 }}>
          <Typography
            variant="h6"
            gutterBottom
            sx={{ mb: 3, fontWeight: "bold" }}
          >
            {award.title || award.notice_name || "제목 없음"}
          </Typography>

          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                공고번호
              </Typography>
              <Typography variant="body1" sx={{ fontWeight: 500 }}>
                {award.notice_number || "-"}
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                낙찰업체
              </Typography>
              <Typography
                variant="body1"
                color="primary"
                sx={{ fontWeight: "bold" }}
              >
                {award.contractor_name || award.award_company_name || "-"}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                낙찰금액
              </Typography>
              <Typography
                variant="h6"
                color="primary"
                sx={{ fontWeight: "bold" }}
              >
                {formatAmount(award.contract_amount || award.award_amount)}
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                낙찰률
              </Typography>
              <Typography variant="body1">
                {award.winning_rate ? `${award.winning_rate}%` : "-"}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                낙찰일자
              </Typography>
              <Typography variant="body1">
                {award.contract_date || award.award_date
                  ? new Date(
                      award.contract_date || award.award_date
                    ).toLocaleDateString("ko-KR")
                  : "-"}
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                발주기관
              </Typography>
              <Typography variant="body1">
                {award.ordering_agency || "-"}
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

export default AwardDetailModal;
