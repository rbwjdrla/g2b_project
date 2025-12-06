import { Bar } from "react-chartjs-2";

function AgencyChart({ data }) {
  const chartData = {
    labels: data.map((a) => a.agency),
    datasets: [
      {
        label: "공고 건수",
        data: data.map((a) => a.count),
        backgroundColor: "rgba(25, 118, 210, 0.6)",
        borderColor: "rgba(25, 118, 210, 1)",
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: "y",
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: "TOP 10 발주기관",
        font: { size: 16 },
      },
    },
    scales: {
      x: {
        beginAtZero: true,
      },
    },
  };

  return <Bar data={chartData} options={options} />;
}

export default AgencyChart;
