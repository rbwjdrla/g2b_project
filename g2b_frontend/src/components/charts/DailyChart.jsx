import { Line } from "react-chartjs-2";

function DailyChart({ data }) {
  const chartData = {
    labels: data.map((d) => d.date.substring(5)), // MM-DD
    datasets: [
      {
        label: "입찰공고 건수",
        data: data.map((d) => d.count),
        borderColor: "rgb(25, 118, 210)",
        backgroundColor: "rgba(25, 118, 210, 0.5)",
        tension: 0.3,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "최근 30일 입찰공고 추이",
        font: { size: 16 },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return <Line data={chartData} options={options} />;
}

export default DailyChart;
