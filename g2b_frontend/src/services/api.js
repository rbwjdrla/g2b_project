// src/services/api.js
import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getBiddings = async (params = {}) => {
  try {
    const response = await api.get('/biddings', { params });
    return response.data;
  } catch (error) {
    console.error('입찰공고 조회 에러:', error);
    throw error;
  }
};

export const getBiddingDetail = async (noticeNumber) => {
  try {
    const response = await api.get(`/biddings/${noticeNumber}`);
    return response.data;
  } catch (error) {
    console.error('입찰공고 상세 조회 에러:', error);
    throw error;
  }
};

export const getAwards = async (params = {}) => {
  try {
    const response = await api.get('/awards', { params });
    return response.data;
  } catch (error) {
    console.error('낙찰정보 조회 에러:', error);
    throw error;
  }
};

export const getOrderPlans = async (params = {}) => {
  try {
    const response = await api.get('/orderplans', { params });
    return response.data;
  } catch (error) {
    console.error('발주계획 조회 에러:', error);
    throw error;
  }
};

export const getStatisticsSummary = async () => {
  try {
    const response = await api.get('/statistics/summary');
    return response.data;
  } catch (error) {
    console.error('통계 요약 조회 에러:', error);
    throw error;
  }
};

export const getDailyStatistics = async (days = 30) => {
  try {
    const response = await api.get('/statistics/daily', { params: { days } });
    return response.data;
  } catch (error) {
    console.error('일별 통계 조회 에러:', error);
    throw error;
  }
};

export const getTopAgencies = async (limit = 10) => {
  try {
    const response = await api.get('/statistics/top-agencies', { params: { limit } });
    return response.data;
  } catch (error) {
    console.error('TOP 기관 조회 에러:', error);
    throw error;
  }
};

export const getStatisticsByType = async () => {
  try {
    const response = await api.get('/statistics/by-type');
    return response.data;
  } catch (error) {
    console.error('유형별 통계 조회 에러:', error);
    throw error;
  }
};

export default api;