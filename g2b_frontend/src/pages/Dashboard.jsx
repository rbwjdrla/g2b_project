// src/pages/Dashboard.jsx
import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  Box,
  Tabs,
  Tab,
  Pagination,
  CircularProgress,
  Button,
  Grid,
  Paper,
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
  Filler,
} from "chart.js";
import dayjs from "dayjs";
import { getBiddings, getAwards, getOrderPlans } from "../services/api";
import DateRangeFilter from "../components/filters/DateRangeFilter";
import TypeFilter from "../components/filters/TypeFilter";
import SearchBar from "../components/filters/SearchBar";
import BudgetFilter from "../components/filters/BudgetFilter";
import CategoryFilter from "../components/filters/CategoryFilter";
import BiddingsList from "../components/tables/BiddingsList";
import AwardsList from "../components/tables/AwardsList";
import OrderPlansList from "../components/tables/OrderPlansList";
import BiddingDetailModal from "../components/BiddingDetailModal";
import AwardDetailModal from "../components/AwardDetailModal";
import OrderPlanDetailModal from "../components/OrderPlanDetailModal";
import DailyChart from "../components/charts/DailyChart";
import TypeChart from "../components/charts/TypeChart";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const Dashboard = () => {
  const [currentTab, setCurrentTab] = useState(0);
  const [loading, setLoading] = useState(false);

  const [biddings, setBiddings] = useState([]);
  const [biddingsTotal, setBiddingsTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);

  const [awards, setAwards] = useState([]);
  const [awardsTotal, setAwardsTotal] = useState(0);
  const [awardsPage, setAwardsPage] = useState(1);
  const [awardsTotalPages, setAwardsTotalPages] = useState(0);

  const [orderPlans, setOrderPlans] = useState([]);
  const [plansTotal, setPlansTotal] = useState(0);
  const [plansPage, setPlansPage] = useState(1);
  const [plansTotalPages, setPlansTotalPages] = useState(0);

  const [dailyData, setDailyData] = useState([]);
  const [typeData, setTypeData] = useState([]);

  const [filters, setFilters] = useState({
    startDate: dayjs().subtract(30, "day"),
    endDate: dayjs(),
    noticeType: "",
    search: "",
    minBudget: "",
    maxBudget: "",
    aiCategory: "",
  });

  const [selectedItem, setSelectedItem] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

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

  useEffect(() => {
    loadData();
    loadStatistics();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      await Promise.all([loadBiddings(1), loadAwards(1), loadOrderPlans(1)]);
    } catch (error) {
      console.error("데이터 로드 실패:", error);
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async () => {
    try {
      const [dailyRes, typeRes] = await Promise.all([
        fetch("/api/statistics/daily")
          .then((r) => r.json())
          .catch(() => []),
        fetch("/api/statistics/by-type")
          .then((r) => r.json())
          .catch(() => []),
      ]);

      setDailyData(dailyRes);
      setTypeData(typeRes);
    } catch (error) {
      console.error("통계 로드 실패:", error);
      setDailyData([]);
      setTypeData([]);
    }
  };

  const buildParams = (pageNum) => {
    const params = {
      page: pageNum,
      page_size: 20,
    };

    if (filters.startDate) {
      params.start_date = filters.startDate.format("YYYY-MM-DD");
    }
    if (filters.endDate) {
      params.end_date = filters.endDate.format("YYYY-MM-DD");
    }
    if (filters.noticeType) {
      params.notice_type = filters.noticeType;
    }
    if (filters.search) {
    if (filters.minBudget) {
      params.min_budget = filters.minBudget;
    }
    if (filters.maxBudget) {
      params.max_budget = filters.maxBudget;
    }
    if (filters.aiCategory) {
      params.ai_category = filters.aiCategory;
    }
      params.search = filters.search;
    }

    console.log("API 요청 params:", params);
    return params;
  };

  const loadBiddings = async (pageNum) => {
    try {
      const response = await getBiddings(buildParams(pageNum));
      setBiddings(response.items || []);
      setBiddingsTotal(response.total || 0);
      setTotalPages(Math.ceil((response.total || 0) / 20));
    } catch (error) {
      console.error("입찰공고 로드 실패:", error);
      setBiddings([]);
      setBiddingsTotal(0);
    }
  };

  const loadAwards = async (pageNum) => {
    try {
      const response = await getAwards(buildParams(pageNum));
      setAwards(response.items || []);
      setAwardsTotal(response.total || 0);
      setAwardsTotalPages(Math.ceil((response.total || 0) / 20));
    } catch (error) {
      console.error("낙찰정보 로드 실패:", error);
      setAwards([]);
      setAwardsTotal(0);
    }
  };

  const loadOrderPlans = async (pageNum) => {
    try {
      const response = await getOrderPlans(buildParams(pageNum));
      setOrderPlans(response.items || []);
      setPlansTotal(response.total || 0);
      setPlansTotalPages(Math.ceil((response.total || 0) / 20));
    } catch (error) {
      console.error("발주계획 로드 실패:", error);
      setOrderPlans([]);
      setPlansTotal(0);
    }
  };

  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  const handlePageChange = (event, value) => {
    setPage(value);
    loadBiddings(value);
  };

  const handleAwardsPageChange = (event, value) => {
    setAwardsPage(value);
    loadAwards(value);
  };

  const handlePlansPageChange = (event, value) => {
    setPlansPage(value);
    loadOrderPlans(value);
  };

  const handleFilter = () => {
    console.log("=== 필터 조건 ===");
    console.log("startDate:", filters.startDate?.format("YYYY-MM-DD"));
    console.log("endDate:", filters.endDate?.format("YYYY-MM-DD"));
    console.log("noticeType:", filters.noticeType);
    console.log("search:", filters.search);

    if (currentTab === 0) {
      setPage(1);
      loadBiddings(1);
    } else if (currentTab === 1) {
      setAwardsPage(1);
      loadAwards(1);
    } else if (currentTab === 2) {
      setPlansPage(1);
      loadOrderPlans(1);
    }
  };

  const handleReset = () => {
    setFilters({
      startDate: dayjs().subtract(30, "day"),
      endDate: dayjs(),
      noticeType: "",
      search: "",
      minBudget: "",
      maxBudget: "",
      aiCategory: "",
    });
    setPage(1);
    setAwardsPage(1);
    setPlansPage(1);
    loadData();
  };

  const handleItemClick = (item) => {
    setSelectedItem(item);
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setSelectedItem(null);
  };

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        G2B 입찰 정보 대시보드
      </Typography>

      {/* 필터 */}
      <Box sx={{ mb: 3 }}>
        <Box
          sx={{
            display: "flex",
            gap: 2,
            flexWrap: "wrap",
            alignItems: "center",
            mb: 2,
          }}
        >
          <DateRangeFilter
            startDate={filters.startDate}
            endDate={filters.endDate}
            onStartDateChange={(date) =>
              setFilters({ ...filters, startDate: date })
            }
            onEndDateChange={(date) =>
              setFilters({ ...filters, endDate: date })
            }
          />
          <TypeFilter
            value={filters.noticeType}
            onChange={(type) => setFilters({ ...filters, noticeType: type })}
          />
          <SearchBar
            value={filters.search}
            onChange={(search) => setFilters({ ...filters, search })}
            onSearch={handleFilter}
          />
        </Box>
        <Box
          sx={{
            display: "flex",
            gap: 2,
            flexWrap: "wrap",
            alignItems: "center",
          }}
        >
          <BudgetFilter
            minBudget={filters.minBudget}
            maxBudget={filters.maxBudget}
            onMinChange={(value) => setFilters({ ...filters, minBudget: value })}
            onMaxChange={(value) => setFilters({ ...filters, maxBudget: value })}
          />
          <CategoryFilter
            value={filters.aiCategory}
            onChange={(value) => setFilters({ ...filters, aiCategory: value })}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleFilter}
            sx={{ height: 40 }}
          >
            검색
          </Button>
          <Button variant="outlined" onClick={handleReset} sx={{ height: 40 }}>
            초기화
          </Button>
        </Box>
      </Box>

      {/* Grid 레이아웃: 왼쪽 메인 + 오른쪽 통계 */}
      <Grid container spacing={3}>
        {/* 왼쪽: 메인 콘텐츠 */}
        <Grid item xs={12} lg={8}>
          {/* 탭 */}
          <Box sx={{ borderBottom: 1, borderColor: "divider", mb: 2 }}>
            <Tabs value={currentTab} onChange={handleTabChange}>
              <Tab label="입찰공고" />
              <Tab label="낙찰정보" />
              <Tab label="발주계획" />
            </Tabs>
          </Box>

          {/* 탭 패널 */}
          {currentTab === 0 && (
            <>
              <BiddingsList
                biddings={biddings}
                formatAmount={formatAmount}
                total={biddingsTotal}
                page={page}
                limit={20}
                onPageChange={handlePageChange}
                onItemClick={handleItemClick}
              />
              <Box sx={{ display: "flex", justifyContent: "center", mt: 3 }}>
                <Pagination
                  count={totalPages}
                  page={page}
                  onChange={handlePageChange}
                  color="primary"
                />
              </Box>
            </>
          )}

          {currentTab === 1 && (
            <>
              <AwardsList
                awards={awards}
                formatAmount={formatAmount}
                total={awardsTotal}
                page={awardsPage}
                limit={20}
                onPageChange={handleAwardsPageChange}
                onItemClick={handleItemClick}
              />
              <Box sx={{ display: "flex", justifyContent: "center", mt: 3 }}>
                <Pagination
                  count={awardsTotalPages}
                  page={awardsPage}
                  onChange={handleAwardsPageChange}
                  color="primary"
                />
              </Box>
            </>
          )}

          {currentTab === 2 && (
            <>
              <OrderPlansList
                plans={orderPlans}
                formatAmount={formatAmount}
                total={plansTotal}
                page={plansPage}
                limit={20}
                onPageChange={handlePlansPageChange}
                onItemClick={handleItemClick}
              />
              <Box sx={{ display: "flex", justifyContent: "center", mt: 3 }}>
                <Pagination
                  count={plansTotalPages}
                  page={plansPage}
                  onChange={handlePlansPageChange}
                  color="primary"
                />
              </Box>
            </>
          )}
        </Grid>

        {/* 오른쪽: 통계 패널 */}
        <Grid item xs={12} lg={4}>
          <Box sx={{ position: "sticky", top: 20 }}>
            {dailyData.length > 0 && (
              <Paper sx={{ p: 2, mb: 3, height: 350 }}>
                <DailyChart data={dailyData} />
              </Paper>
            )}

            {typeData.length > 0 && (
              <Paper sx={{ p: 2, mb: 3, height: 350 }}>
                <TypeChart data={typeData} />
              </Paper>
            )}
          </Box>
        </Grid>
      </Grid>

      {/* 모달 */}
      {currentTab === 0 && (
        <BiddingDetailModal
          open={modalOpen}
          onClose={handleCloseModal}
          bidding={selectedItem}
          formatAmount={formatAmount}
        />
      )}

      {currentTab === 1 && (
        <AwardDetailModal
          open={modalOpen}
          onClose={handleCloseModal}
          award={selectedItem}
          formatAmount={formatAmount}
        />
      )}

      {currentTab === 2 && (
        <OrderPlanDetailModal
          open={modalOpen}
          onClose={handleCloseModal}
          plan={selectedItem}
          formatAmount={formatAmount}
        />
      )}
    </Container>
  );
};

export default Dashboard;
