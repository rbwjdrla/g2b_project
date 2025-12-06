import { Card, CardContent, Box, Typography } from "@mui/material";

function StatCard({ title, value, icon: Icon, color, suffix = "건" }) {
  return (
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
}

export default StatCard;
