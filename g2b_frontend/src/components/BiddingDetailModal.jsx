import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Divider,
  Grid,
  Chip,
  Link,
} from "@mui/material";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";

function BiddingDetailModal({ open, onClose, bidding, formatAmount }) {
  if (!bidding) return null;

  const InfoRow = ({ label, value, highlight = false }) => (
    <Grid container spacing={2} sx={{ py: 1 }}>
      <Grid item xs={4}>
        <Typography variant="body2" color="text.secondary" fontWeight="bold">
          {label}
        </Typography>
      </Grid>
      <Grid item xs={8}>
        <Typography
          variant="body2"
          fontWeight={highlight ? "bold" : "normal"}
          color={highlight ? "primary" : "text.primary"}
        >
          {value || "-"}
        </Typography>
      </Grid>
    </Grid>
  );

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        <Box
          display="flex"
          justifyContent="space-between"
          alignItems="start"
          gap={2}
        >
          <Typography variant="h6" sx={{ flex: 1 }}>
            {bidding.title}
          </Typography>
          <Chip
            label={bidding.notice_type}
            color={
              bidding.notice_type === "공사"
                ? "error"
                : bidding.notice_type === "용역"
                ? "primary"
                : "success"
            }
          />
        </Box>
      </DialogTitle>
      <DialogContent>
        <Box sx={{ mt: 2 }}>
          {/* 기본 정보 */}
          <Typography
            variant="subtitle1"
            fontWeight="bold"
            color="primary"
            gutterBottom
          >
            📋 기본 정보
          </Typography>
          <InfoRow label="공고번호" value={bidding.notice_number} />
          <InfoRow label="유형" value={bidding.notice_type} />
          <InfoRow label="발주기관" value={bidding.ordering_agency} highlight />
          <InfoRow label="수요기관" value={bidding.demanding_agency} />
          <Divider sx={{ my: 2 }} />

          {/* 금액 정보 */}
          <Typography
            variant="subtitle1"
            fontWeight="bold"
            color="primary"
            gutterBottom
          >
            💰 금액 정보
          </Typography>
          <InfoRow
            label="예산금액"
            value={
              bidding.budget_amount ? formatAmount(bidding.budget_amount) : "-"
            }
          />
          <InfoRow
            label="추정가격"
            value={
              bidding.estimated_price
                ? formatAmount(bidding.estimated_price)
                : "-"
            }
            highlight
          />
          <Divider sx={{ my: 2 }} />

          {/* 입찰 정보 */}
          <Typography
            variant="subtitle1"
            fontWeight="bold"
            color="primary"
            gutterBottom
          >
            📄 입찰 정보
          </Typography>
          <InfoRow label="입찰방식" value={bidding.bidding_method} />
          <InfoRow label="계약방법" value={bidding.contract_method} />
          <Divider sx={{ my: 2 }} />

          {/* 일정 정보 */}
          <Typography
            variant="subtitle1"
            fontWeight="bold"
            color="primary"
            gutterBottom
          >
            📅 일정 정보
          </Typography>
          <InfoRow
            label="공고일시"
            value={
              bidding.notice_date
                ? new Date(bidding.notice_date).toLocaleString("ko-KR")
                : "-"
            }
          />
          <InfoRow
            label="입찰마감"
            value={
              bidding.bid_close_date
                ? new Date(bidding.bid_close_date).toLocaleString("ko-KR")
                : "-"
            }
            highlight
          />
          <Divider sx={{ my: 2 }} />

          {/* 상세 링크 */}
          <Typography
            variant="subtitle1"
            fontWeight="bold"
            color="primary"
            gutterBottom
          >
            🔗 상세 정보
          </Typography>
          {bidding.bidding_url && (
            <Link
              href={bidding.bidding_url}
              target="_blank"
              rel="noopener noreferrer"
              sx={{
                display: "inline-flex",
                alignItems: "center",
                gap: 1,
                mt: 1,
                p: 2,
                bgcolor: "#f5f5f5",
                borderRadius: 1,
                textDecoration: "none",
                "&:hover": {
                  bgcolor: "#e0e0e0",
                },
              }}
            >
              <OpenInNewIcon fontSize="small" />
              <Typography variant="body2">
                나라장터에서 상세 정보 보기
              </Typography>
            </Link>
          )}

          {/* 안내 */}
          <Box sx={{ mt: 3, p: 2, bgcolor: "#fff3cd", borderRadius: 1 }}>
            <Typography variant="body2" color="text.secondary">
              💡 더 자세한 정보는 나라장터 링크를 통해 확인하실 수 있습니다.
            </Typography>
          </Box>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} variant="contained">
          닫기
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default BiddingDetailModal;
