import { useState, useEffect } from 'react';
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
  TableRow
} from '@mui/material';
import { 
  Assessment as AssessmentIcon,
  Gavel as GavelIcon,
  Description as DescriptionIcon,
  TrendingUp as TrendingUpIcon
} from '@mui/icons-material';
import { 
  getBiddings, 
  getStatisticsSummary,
  getDailyStatistics,
  getTopAgencies 
} from '../services/api';

function Dashboard() {
  const formatAmount = (amount) => {
    if (!amount && amount !== 0) return '-';
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
    totalBudget: 0
  });
  const [recentBiddings, setRecentBiddings] = useState([]);
  const [topAgencies, setTopAgencies] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // 통계 데이터
      const statsData = await getStatisticsSummary();
      console.log('통계 데이터:', statsData);
      
      setStats({
        totalBiddings: statsData.total_biddings || 0,
        totalAwards: statsData.total_awards || 0,
        totalOrderPlans: statsData.total_order_plans || 0,
        totalBudget: statsData.total_budget || 0
      });
      
      // 최근 입찰공고
      const biddingsData = await getBiddings({ limit: 10 });
      console.log('입찰공고 데이터:', biddingsData);
      
      if (biddingsData.items) {
        setRecentBiddings(biddingsData.items);
      }
      
      // TOP 기관
      const agenciesData = await getTopAgencies(5);
      console.log('TOP 기관:', agenciesData);
      setTopAgencies(agenciesData);
      
    } catch (error) {
      console.error('데이터 로딩 에러:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, icon: Icon, color, suffix = '건' }) => (
    <Card sx={{ height: '100%', bgcolor: color }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography color="white" variant="h6" gutterBottom>
              {title}
            </Typography>
            <Typography color="white" variant="h4">
              {typeof value === 'number' ? value.toLocaleString() : value}{suffix}
            </Typography>
          </Box>
          <Icon sx={{ fontSize: 48, color: 'white', opacity: 0.7 }} />
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
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

      {/* TOP 5 기관 */}
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
              {topAgencies.map((agency, index) => (
                <TableRow key={index}>
                  <TableCell>{index + 1}</TableCell>
                  <TableCell>{agency.agency}</TableCell>
                  <TableCell align="right">{agency.count.toLocaleString()}건</TableCell>
                  <TableCell align="right">{formatAmount(agency.total_budget)}</TableCell>
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
                  borderBottom: index < recentBiddings.length - 1 ? '1px solid #eee' : 'none' 
                }}
              >
                <Typography variant="subtitle1" fontWeight="bold">
                  {bidding.title}
                </Typography>
                <Box display="flex" gap={2} mt={1}>
                  <Typography variant="body2" color="text.secondary">
                    {bidding.notice_type || '-'}
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