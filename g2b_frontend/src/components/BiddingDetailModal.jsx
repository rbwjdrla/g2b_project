import { useState, useEffect } from "react";
import {
  Box,
  Grid,
  Paper,
  CircularProgress,
  Button,
  Typography,
  Tabs,
  Tab,
} from "@mui/material";
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
  getAwards,
  getOrderPlans,
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
import AwardsList from "../components/tables/AwardsList";
import OrderPlansList from "../components/tables/OrderPlansList";
import BiddingDetailModal from "../components/BiddingDetailModal";
import TabPanel from "../components/TabPanel";

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
  const [topAgencies, setTopAgencies] = useState([]);
  const [dailyStats, setDailyStats] = useState([]);
  const [typeStats, setTypeStats] = useState([]);

  // 탭 State
  const [currentTab, setCurrentTab] = useState(0);

  // 필터 State
  const [startDate, setStartDate] = useState(dayjs().subtract(30, "day"));
  const [endDate, setEndDate] = useState(dayjs());
  const [noticeType, setNoticeType] = useState("");
  const [searchText, setSearchText] = useState("");
  const [limit] = useState(20);

  // 입찰공고 State
  const [recentBiddings, setRecentBiddings] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  // 낙찰정보 State
  const [awards, setAwards] = useState([]);
  const [awardsPage, setAwardsPage] = useState(1);
  const [awardsTotal, setAwardsTotal] = useState(0);

  // 발주계획 State
  const [orderPlans, setOrderPlans] = useState([]);
  const [plansPage, setPlansPage] = useState(1);
  const [plansTotal, setPlansTotal] = useState(0);

  // 상세 모달 State
  const [selectedBidding, setSelectedBidding] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  // 데이터 로드
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);

      // 입찰공고
      const biddingsData = await getBiddings({
        limit: limit,
        skip: (page - 1) * limit,
      });
      if (biddingsData) {
        setRecentBiddings(biddingsData.items || []);
        setTotal(biddingsData.total || 0);
      }

      // 낙찰정보
      const awardsData = await getAwards({
        limit: limit,
        skip: (awardsPage - 1) * limit,
      });
      if (awardsData) {
        setAwards(awardsData.items || []);
        setAwardsTotal(awardsData.total || 0);
      }

      // 발주계획
      const plansData = await getOrderPlans({
        limit: limit,
        skip: (plansPage - 1) * limit,
      });
      if (plansData) {
        setOrderPlans(plansData.items || []);
        setPlansTotal(plansData.total || 0);
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

  // 탭 변경
  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  // 필터 적용
  const handleFilter = async () => {
    setPage(1);
    setAwardsPage(1);
    setPlansPage(1);

    try {
      setLoading(true);
      const params = {
        limit: limit,
        skip: 0,
        notice_type: noticeType || undefined,
        search: searchText || undefined,
      };

      // 현재 탭에 따라 데이터 로드
      if (currentTab === 0) {
        const biddingsData = await getBiddings(params);
        if (biddingsData) {
          setRecentBiddings(biddingsData.items || []);
          setTotal(biddingsData.total || 0);
        }
      } else if (currentTab === 1) {
        const awardsData = await getAwards(params);
        if (awardsData) {
          setAwards(awardsData.items || []);
          setAwardsTotal(awardsData.total || 0);
        }
      } else if (currentTab === 2) {
        const plansData = await getOrderPlans({
          limit: limit,
          skip: 0,
          search: searchText || undefined,
        });
        if (plansData) {
          setOrderPlans(plansData.items || []);
          setPlansTotal(plansData.total || 0);
        }
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
    setPage(1);
    setAwardsPage(1);
    setPlansPage(1);
    loadData();
  };

  // 입찰공고 페이지 변경
  const handlePageChange = async (newPage) => {
    setPage(newPage);
    window.scrollTo({ top: 0, behavior: "smooth" });

    try {
      setLoading(true);
      const params = {
        limit: limit,
        skip: (newPage - 1) * limit,
        notice_type: noticeType || undefined,
        search: searchText || undefined,
      };

      const biddingsData = await getBiddings(params);
      if (biddingsData) {
        setRecentBiddings(biddingsData.items || []);
        setTotal(biddingsData.total || 0);
      }
    } catch (error) {
      console.error("페이지 변경 에러:", error);
    } finally {
      setLoading(false);
    }
  };

  // 낙찰정보 페이지 변경
  const handleAwardsPageChange = async (newPage) => {
    setAwardsPage(newPage);
    window.scrollTo({ top: 0, behavior: "smooth" });

    try {
      setLoading(true);
      const awardsData = await getAwards({
        limit: limit,
        skip: (newPage - 1) * limit,
        notice_type: noticeType || undefined,
        search: searchText || undefined,
      });
      if (awardsData) {
        setAwards(awardsData.items || []);
        setAwardsTotal(awardsData.total || 0);
      }
    } catch (error) {
      console.error("페이지 변경 에러:", error);
    } finally {
      setLoading(false);
    }
  };

  // 발주계획 페이지 변경
  const handlePlansPageChange = async (newPage) => {
    setPlansPage(newPage);
    window.scrollTo({ top: 0, behavior: "smooth" });

    try {
      setLoading(true);
      const plansData = await getOrderPlans({
        limit: limit,
        skip: (newPage - 1) * limit,
        search: searchText || undefined,
      });
      if (plansData) {
        setOrderPlans(plansData.items || []);
        setPlansTotal(plansData.total || 0);
      }
    } catch (error) {
      console.error("페이지 변경 에러:", error);
    } finally {
      setLoading(false);
    }
  };

  // 상세 모달
  const handleItemClick = (item) => {
    setSelectedBidding(item);
    setModalOpen(true);
  };

  const handleModalClose = () => {
    setModalOpen(false);
    setSelectedBidding(null);
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
            placeholder="공고명, 기관명, 업체명 검색"
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

      {/* 탭 */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={currentTab} onChange={handleTabChange}>
          <Tab label="입찰공고" />
          <Tab label="낙찰정보" />
          <Tab label="발주계획" />
        </Tabs>
      </Paper>

      {/* 메인 레이아웃: 왼쪽 목록, 오른쪽 통계 */}
      <Grid container spacing={3}>
        {/* 왼쪽: 탭별 목록 */}
        <Grid item xs={12} lg={7}>
          <TabPanel value={currentTab} index={0}>
            <BiddingsList
              biddings={recentBiddings}
              formatAmount={formatAmount}
              total={total}
              page={page}
              limit={limit}
              onPageChange={handlePageChange}
              onItemClick={handleItemClick}
            />
          </TabPanel>

          <TabPanel value={currentTab} index={1}>
            <AwardsList
              awards={awards}
              formatAmount={formatAmount}
              total={awardsTotal}
              page={awardsPage}
              limit={limit}
              onPageChange={handleAwardsPageChange}
              onItemClick={handleItemClick}
            />
          </TabPanel>

          <TabPanel value={currentTab} index={2}>
            <OrderPlansList
              plans={orderPlans}
              formatAmount={formatAmount}
              total={plansTotal}
              page={plansPage}
              limit={limit}
              onPageChange={handlePlansPageChange}
              onItemClick={handleItemClick}
            />
          </TabPanel>
        </Grid>

        {/* 오른쪽: 통계 */}
        <Grid item xs={12} lg={5}>
          <Box sx={{ display: "flex", flexDirection: "column", gap: 3 }}>
            {/* 일별 추이 차트 */}
            <Paper sx={{ p: 3, height: 400 }}>
              <DailyChart data={dailyStats} />
            </Paper>

            {/* 유형별 차트 */}
            <Paper sx={{ p: 3, height: 400 }}>
              <TypeChart data={typeStats} />
            </Paper>

            {/* TOP 5 기관 테이블 */}
            <TopAgenciesTable
              agencies={topAgencies}
              formatAmount={formatAmount}
            />

            {/* TOP 기관 바 차트 */}
            <Paper sx={{ p: 3, height: 500 }}>
              <AgencyChart data={topAgencies} />
            </Paper>
          </Box>
        </Grid>
      </Grid>

      {/* 상세 모달 */}
      <BiddingDetailModal
        open={modalOpen}
        onClose={handleModalClose}
        bidding={selectedBidding}
        formatAmount={formatAmount}
      />
    </Box>
  );
}

export default Dashboard;
