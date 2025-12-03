import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Box, AppBar, Toolbar, Typography, Container } from '@mui/material';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <Router>
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        {/* 헤더 */}
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div">
              G2B 입찰공고 조회 시스템
            </Typography>
          </Toolbar>
        </AppBar>

        {/* 메인 컨텐츠 */}
        <Box component="main" sx={{ flexGrow: 1, bgcolor: '#f5f5f5' }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
          </Routes>
        </Box>

        {/* 푸터 */}
        <Box component="footer" sx={{ py: 3, px: 2, mt: 'auto', bgcolor: '#1976d2', color: 'white' }}>
          <Container maxWidth="sm">
            <Typography variant="body2" align="center">
              © 2025 G2B 입찰공고 조회 시스템
            </Typography>
          </Container>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
