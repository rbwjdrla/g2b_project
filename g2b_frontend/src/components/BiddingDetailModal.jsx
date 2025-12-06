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
} from "@mui/material";

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
    <Dialog open={open} onClose={onClose} maxWidth="lg" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6" sx={{ flex: 1, pr: 2 }}>
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
          <InfoRow label="공고명" value={bidding.title} />
          <InfoRow label="유형" value={bidding.notice_type} />
          <InfoRow label="발주기관" value={bidding.ordering_agency} highlight />
          <InfoRow label="수요기관" value={bidding.demand_agency} />
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
            value={formatAmount(bidding.budget_amount)}
            highlight
          />
          <InfoRow
            label="기초금액"
            value={formatAmount(bidding.basic_amount)}
          />
          <Divider sx={{ my: 2 }} />

          {/* 계약 정보 */}
          <Typography
            variant="subtitle1"
            fontWeight="bold"
            color="primary"
            gutterBottom
          >
            📄 계약 정보
          </Typography>
          <InfoRow label="입찰방식" value={bidding.bidding_method} />
          <InfoRow label="계약방법" value={bidding.contract_method} />
          <InfoRow label="공동수급" value={bidding.joint_delivery} />
          <InfoRow label="참가자격" value={bidding.qualification} />
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
          <InfoRow label="공고일시" value={bidding.notice_datetime} />
          <InfoRow
            label="입찰마감"
            value={bidding.bid_close_datetime}
            highlight
          />
          <InfoRow label="개찰일시" value={bidding.bid_open_datetime} />
          <InfoRow label="입찰서류" value={bidding.bid_document_datetime} />
          <InfoRow label="투찰서류" value={bidding.submission_datetime} />
          <Divider sx={{ my: 2 }} />

          {/* 추가 정보 */}
          <Typography
            variant="subtitle1"
            fontWeight="bold"
            color="primary"
            gutterBottom
          >
            ℹ️ 추가 정보
          </Typography>
          <InfoRow label="제한/경쟁" value={bidding.restriction_type} />
          <InfoRow label="입찰참가지역" value={bidding.bidding_region} />
          <InfoRow label="공고기관" value={bidding.notice_agency} />
          <InfoRow label="담당자" value={bidding.contact_person} />
          <InfoRow label="전화번호" value={bidding.contact_phone} />
          <Divider sx={{ my: 2 }} />

          {/* 사업 내용 */}
          <Typography
            variant="subtitle1"
            fontWeight="bold"
            color="primary"
            gutterBottom
          >
            📝 사업 내용
          </Typography>
          <Box
            sx={{
              mt: 1,
              p: 2,
              bgcolor: "#f5f5f5",
              borderRadius: 1,
              maxHeight: 300,
              overflow: "auto",
            }}
          >
            <Typography variant="body2" sx={{ whiteSpace: "pre-wrap" }}>
              {bidding.project_description ||
                bidding.business_description ||
                "내용 없음"}
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
