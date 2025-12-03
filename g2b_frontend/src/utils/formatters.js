export const formatAmount = (amount) => {
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

// 날짜 포맷팅
export const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleDateString('ko-KR');
};

// 날짜+시간 포맷팅
export const formatDateTime = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return date.toLocaleString('ko-KR');
};

// 공고번호 포맷팅
export const formatNoticeNumber = (noticeNumber) => {
  if (!noticeNumber) return '-';
  return noticeNumber;
};
