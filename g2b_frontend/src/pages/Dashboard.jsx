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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import {
  Assessment as AssessmentIcon,
  Gavel as GavelIcon,
  Description as DescriptionIcon,
  TrendingUp as TrendingUpIcon,
} from "@mui/icons-material";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line, Bar, Pie } from "react-chartjs-2";
import {
  getBiddings,
  getStatisticsSummary,
  getDailyStatistics,
  getTopAgencies,
  getStatisticsByType,
} from "../services/api";

// Chart.js 등록
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

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
    totalBudget: 0,
  });
  const [recentBiddings, setRecentBiddings] = useState([]);
  const [topAgencies, setTopAgencies] = useState([]);
  const [dailyStats, setDailyStats] = useState([]);
  const [typeStats, setTypeStats] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      // 통계 데이터
      const statsData = await getStatisticsSummary();
      setStats({
        totalBiddings: statsData.total_biddings || 0,
        totalAwards: statsData.total_awards || 0,
        totalOrderPlans: statsData.total_order_plans || 0,
        totalBudget: statsData.total_budget || 0,
      });

      // 최근 입찰공고
      const biddingsData = await getBiddings({ limit: 10 });
      if (biddingsData.items) {
        setRecentBiddings(biddingsData.items);
      }

      // TOP 기관
      const agenciesData = await getTopAgencies(10);
      setTopAgencies(agenciesData);

      // 일별 통계
      const dailyData = await getDailyStatistics(30);
      setDailyStats(dailyData);

      // 유형별 통계
      const typeData = await getStatisticsByType();
      setTypeStats(typeData);
    } catch (error) {
      console.error("데이터 로딩 에러:", error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon: Icon, color, suffix = "건" }) => (
    <Card sx={{ height: "100%", bgcolor: color }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography color="white" variant="h6" gutterBottom>
              {title}
            </Typography>
            <Typography color="white" variant="h4">
              {typeof value === "number" ? value.toLocaleString() : value}
              {suffix}
            </Typography>
          </Box>
          <Icon sx={{ fontSize: 48, color: "white", opacity: 0.7 }} />
        </Box>
      </CardContent>
    </Card>
  );

  // 일별 차트 데이터
  const dailyChartData = {
    labels: dailyStats.map((d) => d.date.substring(5)), // MM-DD
    datasets: [
      {
        label: "입찰공고 건수",
        data: dailyStats.map((d) => d.count),
        borderColor: "rgb(25, 118, 210)",
        backgroundColor: "rgba(25, 118, 210, 0.5)",
        tension: 0.3,
      },
    ],
  };

  const dailyChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "최근 30일 입찰공고 추이",
        font: { size: 16 },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  // 유형별 파이 차트 데이터
  const typeChartData = {
    labels: typeStats.map((t) => t.type || "미분류"),
    datasets: [
      {
        label: "건수",
        data: typeStats.map((t) => t.count),
        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
          "rgba(75, 192, 192, 0.6)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  const pieChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "right",
      },
      title: {
        display: true,
        text: "유형별 입찰공고 분포",
        font: { size: 16 },
      },
    },
  };

  // TOP 기관 바 차트
  const agencyChartData = {
    labels: topAgencies.map((a) => a.agency),
    datasets: [
      {
        label: "공고 건수",
        data: topAgencies.map((a) => a.count),
        backgroundColor: "rgba(25, 118, 210, 0.6)",
        borderColor: "rgba(25, 118, 210, 1)",
        borderWidth: 1,
      },
    ],
  };

  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: "y",
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: "TOP 10 발주기관",
        font: { size: 16 },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
      },
    },
  };

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
    <Container maxWidth={false} sx={{ px: 3, mt: 4, mb: 4 }}>
      {/* 통계 카드 */}
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
            title="총 예산"
            value={formatAmount(stats.totalBudget)}
            icon={TrendingUpIcon}
            color="#9c27b0"
            suffix=""
          />
        </Grid>
      </Grid>

      {/* 차트 행 */}
      <Grid container spacing={3} mb={4}>
        {/* 일별 라인 차트 */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Line data={dailyChartData} options={dailyChartOptions} />
          </Paper>
        </Grid>

        {/* 유형별 파이 차트 */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Pie data={typeChartData} options={pieChartOptions} />
          </Paper>
        </Grid>
      </Grid>

      {/* TOP 기관 바 차트 */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3, height: 500 }}>
            <Bar data={agencyChartData} options={barChartOptions} />
          </Paper>
        </Grid>
      </Grid>

      {/* TOP 5 기관 테이블 */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          발주 TOP 5 기관
        </Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>순위</TableCell>
                <TableCell>기관명</TableCell>
                <TableCell align="right">공고 건수</TableCell>
                <TableCell align="right">총 예산</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {topAgencies.slice(0, 5).map((agency, index) => (
                <TableRow key={index}>
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>{agency.agency}</TableCell>
                  <TableCell align="right">
                    {agency.count.toLocaleString()}건
                  </TableCell>
                  <TableCell align="right">
                    {formatAmount(agency.total_budget)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* 최근 입찰공고 */}
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
