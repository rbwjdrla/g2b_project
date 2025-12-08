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

function BiddingDetailModal({ open, onClose, bidding, formatAmount }) {
  if (!bidding) return null;

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      {/* 헤더 */}
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box display="flex" alignItems="center" gap={2}>
            <Typography variant="h6">공고 상세정보</Typography>
            <Chip
              label={bidding.notice_type || "미분류"}
              size="small"
              color={
                bidding.notice_type === "공사"
                  ? "error"
                  : bidding.notice_type === "용역"
                  ? "primary"
                  : "success"
              }
            />
          </Box>
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>

      {/* 내용 */}
      <DialogContent dividers>
        <Box sx={{ py: 2 }}>
          {/* 공고명 */}
          <Typography
            variant="h6"
            gutterBottom
            sx={{ mb: 3, fontWeight: "bold" }}
          >
            {bidding.title}
          </Typography>

          <Grid container spacing={3}>
            {/* 공고번호 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                공고번호
              </Typography>
              <Typography variant="body1" sx={{ fontWeight: 500 }}>
                {bidding.notice_number}
              </Typography>
            </Grid>

            {/* 공고일시 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                공고일시
              </Typography>
              <Typography variant="body1">
                {bidding.notice_date
                  ? new Date(bidding.notice_date).toLocaleString("ko-KR")
                  : "-"}
              </Typography>
            </Grid>

            {/* 입찰마감일시 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                입찰마감일시
              </Typography>
              <Typography variant="body1" color="error">
                {bidding.bid_close_date
                  ? new Date(bidding.bid_close_date).toLocaleString("ko-KR")
                  : "-"}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            {/* 발주기관 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                발주기관
              </Typography>
              <Typography variant="body1">
                {bidding.ordering_agency || "-"}
              </Typography>
            </Grid>

            {/* 수요기관 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                수요기관
              </Typography>
              <Typography variant="body1">
                {bidding.demanding_agency || "-"}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            {/* 예산금액 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                예산금액
              </Typography>
              <Typography
                variant="h6"
                color="primary"
                sx={{ fontWeight: "bold" }}
              >
                {formatAmount(bidding.budget_amount)}
              </Typography>
            </Grid>

            {/* 추정가격 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                추정가격
              </Typography>
              <Typography variant="body1">
                {formatAmount(bidding.estimated_price)}
              </Typography>
            </Grid>

            <Grid item xs={12}>
              <Divider />
            </Grid>

            {/* 계약방법 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                계약방법
              </Typography>
              <Typography variant="body1">
                {bidding.contract_method || "-"}
              </Typography>
            </Grid>

            {/* 입찰방법 */}
            <Grid item xs={12} sm={6}>
              <Typography variant="caption" color="text.secondary">
                입찰방법
              </Typography>
              <Typography variant="body1">
                {bidding.bidding_method || "-"}
              </Typography>
            </Grid>

            {/* 나라장터 링크 */}
            {bidding.bidding_url && (
              <Grid item xs={12}>
                <Button
                  variant="outlined"
                  fullWidth
                  href={bidding.bidding_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  sx={{ mt: 2 }}
                >
                  나라장터에서 자세히 보기 →
                </Button>
              </Grid>
            )}
          </Grid>
        </Box>
      </DialogContent>

      {/* 하단 버튼 */}
      <DialogActions sx={{ px: 3, py: 2 }}>
        <Button onClick={onClose} variant="contained" size="large">
          닫기
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default BiddingDetailModal;
