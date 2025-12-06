import { useState, useEffect } from "react";
import { Box, Grid, Paper, CircularProgress, Button } from "@mui/material";
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
import dayjs from "dayjs";

// API
import {
  getBiddings,
  getStatisticsSummary,
  getDailyStatistics,
  getTopAgencies,
  getStatisticsByType,
} from "../services/api";

// Components
import DateRangeFilter from "../components/filters/DateRangeFilter";
import TypeFilter from "../components/filters/TypeFilter";
import SearchBar from "../components/filters/SearchBar";
import DailyChart from "../components/charts/DailyChart";
import TypeChart from "../components/charts/TypeChart";
import AgencyChart from "../components/charts/AgencyChart";
import TopAgenciesTable from "../components/tables/TopAgenciesTable";
import BiddingsList from "../components/tables/BiddingsList";

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
  // 금액 포맷
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

  // State
  const [loading, setLoading] = useState(true);
  const [recentBiddings, setRecentBiddings] = useState([]);
  const [topAgencies, setTopAgencies] = useState([]);
  const [dailyStats, setDailyStats] = useState([]);
  const [typeStats, setTypeStats] = useState([]);

  // 필터 State
  const [startDate, setStartDate] = useState(dayjs().subtract(30, "day"));
  const [endDate, setEndDate] = useState(dayjs());
  const [noticeType, setNoticeType] = useState("");
  const [searchText, setSearchText] = useState("");

  // 데이터 로드
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      // 최근 입찰공고
      const biddingsData = await getBiddings({
        limit: 20,
        skip: 0,
      });
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

  // 필터 적용
  const handleFilter = async () => {
    try {
      setLoading(true);
      const params = {
        limit: 20,
        skip: 0,
        notice_type: noticeType || undefined,
        search: searchText || undefined,
      };

      console.log("검색 파라미터:", params);

      const biddingsData = await getBiddings(params);
      console.log("검색 결과:", biddingsData);

      if (biddingsData.items) {
        setRecentBiddings(biddingsData.items);
      }
    } catch (error) {
      console.error("필터 에러:", error);
    } finally {
      setLoading(false);
    }
  };

  // 필터 초기화
  const handleReset = () => {
    setStartDate(dayjs().subtract(30, "day"));
    setEndDate(dayjs());
    setNoticeType("");
    setSearchText("");
    loadData();
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
    <Box sx={{ width: "100%", minHeight: "100vh", bgcolor: "#f5f5f5", p: 3 }}>
      {/* 필터 */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box display="flex" gap={2} flexWrap="wrap" alignItems="center">
          <DateRangeFilter
            startDate={startDate}
            endDate={endDate}
            onStartDateChange={setStartDate}
            onEndDateChange={setEndDate}
          />
          <TypeFilter
            value={noticeType}
            onChange={(e) => setNoticeType(e.target.value)}
          />
          <SearchBar
            value={searchText}
            onChange={setSearchText}
            placeholder="공고명, 기관명 검색"
          />
          <Box sx={{ ml: "auto", display: "flex", gap: 1 }}>
            <Button variant="contained" onClick={handleFilter}>
              검색
            </Button>
            <Button variant="outlined" onClick={handleReset}>
              초기화
            </Button>
          </Box>
        </Box>
      </Paper>

      {/* 차트 */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3, height: 400 }}>
            <DailyChart data={dailyStats} />
          </Paper>
        </Grid>
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 3, height: 400 }}>
            <TypeChart data={typeStats} />
          </Paper>
        </Grid>
      </Grid>

      {/* TOP 기관 바 차트 */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3, height: 500 }}>
            <AgencyChart data={topAgencies} />
          </Paper>
        </Grid>
      </Grid>

      {/* TOP 5 기관 테이블 */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12}>
          <TopAgenciesTable
            agencies={topAgencies}
            formatAmount={formatAmount}
          />
        </Grid>
      </Grid>

      {/* 최근 입찰공고 */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <BiddingsList biddings={recentBiddings} formatAmount={formatAmount} />
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;
