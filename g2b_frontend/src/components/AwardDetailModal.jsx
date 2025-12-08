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
            {award.award_company_name || "업체명 없음"}
          </Typography>

          <Grid container spacing={3}>
            {/* 공고번호 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                공고번호
              </Typography>
              <Typography variant="body1" sx={{ fontWeight: 500 }}>
                {award.bid_ntce_no || "-"}
              </Typography>
            </Grid>

            {/* 낙찰업체 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                낙찰업체
              </Typography>
              <Typography
                variant="body1"
                color="primary"
                sx={{ fontWeight: "bold" }}
              >
                {award.award_company_name || "-"}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            {/* 낙찰금액 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                낙찰금액
              </Typography>
              <Typography
                variant="h6"
                color="primary"
                sx={{ fontWeight: "bold" }}
              >
                {formatAmount(award.award_amount)}
              </Typography>
            </Grid>

            {/* 낙찰률 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                낙찰률
              </Typography>
              <Typography variant="body1">
                {award.award_rate ? `${award.award_rate}%` : "-"}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            {/* 대표자명 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                대표자명
              </Typography>
              <Typography variant="body1">
                {award.award_ceo_name || "-"}
              </Typography>
            </Grid>

            {/* 사업자번호 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                사업자번호
              </Typography>
              <Typography variant="body1">
                {award.award_business_no || "-"}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            {/* 발주기관코드 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                발주기관코드
              </Typography>
              <Typography variant="body1">
                {award.ntce_instt_cd || "-"}
              </Typography>
            </Grid>

            {/* 수요기관코드 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                수요기관코드
              </Typography>
              <Typography variant="body1">{award.dminstt_cd || "-"}</Typography>
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
