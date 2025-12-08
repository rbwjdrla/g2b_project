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
} from "@mui/material";
import { getBiddings, getAwards, getOrderPlans } from "../services/api";
import DateRangeFilter from "../components/filters/DateRangeFilter";
import TypeFilter from "../components/filters/TypeFilter";
import SearchBar from "../components/filters/SearchBar";
import BiddingsList from "../components/tables/BiddingsList";
import AwardsList from "../components/tables/AwardsList";
import OrderPlansList from "../components/tables/OrderPlansList";
import BiddingDetailModal from "../components/BiddingDetailModal";
import AwardDetailModal from "../components/AwardDetailModal";
import OrderPlanDetailModal from "../components/OrderPlanDetailModal";
import DailyChart from "../components/charts/DailyChart";
import TypeChart from "../components/charts/TypeChart";
import AgencyChart from "../components/charts/AgencyChart";
import TopAgenciesTable from "../components/tables/TopAgenciesTable";

const Dashboard = () => {
  const [currentTab, setCurrentTab] = useState(0);
  const [loading, setLoading] = useState(false);

  // 입찰공고 상태
  const [biddings, setBiddings] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);

  // 낙찰정보 상태
  const [awards, setAwards] = useState([]);
  const [awardsPage, setAwardsPage] = useState(1);
  const [awardsTotalPages, setAwardsTotalPages] = useState(0);

  // 발주계획 상태
  const [orderPlans, setOrderPlans] = useState([]);
  const [plansPage, setPlansPage] = useState(1);
  const [plansTotalPages, setPlansTotalPages] = useState(0);

  // 통계 데이터 상태
  const [dailyData, setDailyData] = useState([]);
  const [typeData, setTypeData] = useState([]);
  const [agencyData, setAgencyData] = useState([]);

  // 필터 상태
  const [filters, setFilters] = useState({
    startDate: null,
    endDate: null,
    noticeType: "",
    search: "",
  });

  // 모달 상태
  const [selectedItem, setSelectedItem] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

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

  // 초기 데이터 로드
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

  // 통계 데이터 로드
  const loadStatistics = async () => {
    try {
      const [dailyRes, typeRes, agencyRes] = await Promise.all([
        fetch("/api/statistics/daily")
          .then((r) => r.json())
          .catch(() => []),
        fetch("/api/statistics/by-type")
          .then((r) => r.json())
          .catch(() => []),
        fetch("/api/statistics/top-agencies")
          .then((r) => r.json())
          .catch(() => []),
      ]);

      setDailyData(dailyRes);
      setTypeData(typeRes);
      setAgencyData(agencyRes);
    } catch (error) {
      console.error("통계 로드 실패:", error);
      setDailyData([]);
      setTypeData([]);
      setAgencyData([]);
    }
  };

  const buildParams = (pageNum) => {
    const params = {
      page: pageNum,
      page_size: 20,
    };

    if (filters.startDate) params.start_date = filters.startDate;
    if (filters.endDate) params.end_date = filters.endDate;
    if (filters.noticeType) params.notice_type = filters.noticeType;
    if (filters.search) params.search = filters.search;

    return params;
  };

  const loadBiddings = async (pageNum) => {
    try {
      const response = await getBiddings(buildParams(pageNum));
      setBiddings(response.items || []);
      setTotalPages(Math.ceil((response.total || 0) / 20));
    } catch (error) {
      console.error("입찰공고 로드 실패:", error);
      setBiddings([]);
    }
  };

  const loadAwards = async (pageNum) => {
    try {
      const response = await getAwards(buildParams(pageNum));
      setAwards(response.items || []);
      setAwardsTotalPages(Math.ceil((response.total || 0) / 20));
    } catch (error) {
      console.error("낙찰정보 로드 실패:", error);
      setAwards([]);
    }
  };

  const loadOrderPlans = async (pageNum) => {
    try {
      const response = await getOrderPlans(buildParams(pageNum));
      setOrderPlans(response.items || []);
      setPlansTotalPages(Math.ceil((response.total || 0) / 20));
    } catch (error) {
      console.error("발주계획 로드 실패:", error);
      setOrderPlans([]);
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
      <Box sx={{ mb: 3, display: "flex", gap: 2, flexWrap: "wrap" }}>
        <DateRangeFilter
          startDate={filters.startDate}
          endDate={filters.endDate}
          onStartDateChange={(date) =>
            setFilters({ ...filters, startDate: date })
          }
          onEndDateChange={(date) => setFilters({ ...filters, endDate: date })}
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

      {/* 통계 차트 */}
      {(dailyData.length > 0 ||
        typeData.length > 0 ||
        agencyData.length > 0) && (
        <Box sx={{ mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            통계
          </Typography>
          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
              gap: 2,
              mb: 2,
            }}
          >
            {dailyData.length > 0 && <DailyChart data={dailyData} />}
            {typeData.length > 0 && <TypeChart data={typeData} />}
          </Box>
          <Box
            sx={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(400px, 1fr))",
              gap: 2,
            }}
          >
            {agencyData.length > 0 && <AgencyChart data={agencyData} />}
            {agencyData.length > 0 && (
              <TopAgenciesTable data={agencyData} formatAmount={formatAmount} />
            )}
          </Box>
        </Box>
      )}

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
            total={biddings.length}
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
            total={awards.length}
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
            total={orderPlans.length}
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

      {/* 상세보기 모달 - 탭별로 다른 모달 */}
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
