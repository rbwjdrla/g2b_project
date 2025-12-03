import axios from 'axios';

// API 기본 URL
const API_BASE_URL = 'http://43.201.32.63:8000/api';

// axios 인스턴스 생성
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 입찰공고 목록 조회
export const getBiddings = async (params = {}) => {
  try {
    const response = await api.get('/biddings', { params });
    return response.data;
  } catch (error) {
    console.error('입찰공고 조회 에러:', error);
    throw error;
  }
};

// 입찰공고 상세 조회
export const getBiddingDetail = async (noticeNumber) => {
  try {
    const response = await api.get(`/biddings/${noticeNumber}`);
    return response.data;
  } catch (error) {
    console.error('입찰공고 상세 조회 에러:', error);
    throw error;
  }
};

// 낙찰정보 목록 조회
export const getAwards = async (params = {}) => {
  try {
    const response = await api.get('/awards', { params });
    return response.data;
  } catch (error) {
    console.error('낙찰정보 조회 에러:', error);
    throw error;
  }
};

// 발주계획 목록 조회
export const getOrderPlans = async (params = {}) => {
  try {
    const response = await api.get('/order-plans', { params });
    return response.data;
  } catch (error) {
    console.error('발주계획 조회 에러:', error);
    throw error;
  }
};

export default api;
