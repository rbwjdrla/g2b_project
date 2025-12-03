import { useState, useEffect } from "react";
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
} from "@mui/material";
import {
  Assessment as AssessmentIcon,
  Gavel as GavelIcon,
  Description as DescriptionIcon,
  TrendingUp as TrendingUpIcon,
} from "@mui/icons-material";
import { getBiddings } from "../services/api";

function Dashboard() {
  const formatAmount = (amount) => {
    if (!amount && amount !== 0) return "-";
    if (amount >= 1000000000000) {
      return `${(amount / 1000000000000).toFixed(1)}조원`;
    } else if (amount >= 100000000) {
      return `${(amount / 100000000).toFixed(1)}억원`;
    } else if (amount >= 10000) {
      return `${(amount / 10000).toFixed(0)}만원`;
    } else {
      return `${amount.toLocaleString()}원`;
    }
  };

  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalBiddings: 0,
    totalAwards: 0,
    totalOrderPlans: 0,
    todayBiddings: 0,
  });
  const [recentBiddings, setRecentBiddings] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      // 입찰공고만 가져오기
      const response = await getBiddings({ limit: 10 });
      console.log("API 응답:", response);

      const items = Array.isArray(response) ? response : [];

      setStats({
        totalBiddings: items.length,
        totalAwards: 0,
        totalOrderPlans: 0,
        todayBiddings: items.length,
      });

      setRecentBiddings(items);
    } catch (error) {
      console.error("데이터 로딩 에러:", error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon: Icon, color }) => (
    <Card sx={{ height: "100%", bgcolor: color }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography color="white" variant="h6" gutterBottom>
              {title}
            </Typography>
            <Typography color="white" variant="h4">
              {value}건
            </Typography>
          </Box>
          <Icon sx={{ fontSize: 48, color: "white", opacity: 0.7 }} />
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="80vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="총 입찰공고"
            value={stats.totalBiddings}
            icon={DescriptionIcon}
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="총 낙찰정보"
            value={stats.totalAwards}
            icon={GavelIcon}
            color="#2e7d32"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="총 발주계획"
            value={stats.totalOrderPlans}
            icon={AssessmentIcon}
            color="#ed6c02"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="최근 공고"
            value={stats.todayBiddings}
            icon={TrendingUpIcon}
            color="#9c27b0"
          />
        </Grid>
      </Grid>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          최근 입찰공고
        </Typography>
        <Box>
          {recentBiddings.length === 0 ? (
            <Typography color="text.secondary">데이터가 없습니다.</Typography>
          ) : (
            recentBiddings.map((bidding, index) => (
              <Box
                key={index}
                sx={{
                  py: 2,
                  borderBottom:
                    index < recentBiddings.length - 1
                      ? "1px solid #eee"
                      : "none",
                }}
              >
                <Typography variant="subtitle1" fontWeight="bold">
                  {bidding.title}
                </Typography>
                <Box display="flex" gap={2} mt={1}>
                  <Typography variant="body2" color="text.secondary">
                    {bidding.notice_type || "-"}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {bidding.ordering_agency}
                  </Typography>
                  <Typography variant="body2" color="primary">
                    {formatAmount(bidding.budget_amount)}
                  </Typography>
                </Box>
              </Box>
            ))
          )}
        </Box>
      </Paper>
    </Container>
  );
}

export default Dashboard;
