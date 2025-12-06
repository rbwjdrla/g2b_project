import { Pie } from "react-chartjs-2";

function TypeChart({ data }) {
  const chartData = {
    labels: data.map((t) => t.type || "미분류"),
    datasets: [
      {
        label: "건수",
        data: data.map((t) => t.count),
        backgroundColor: [
          "rgba(255, 99, 132, 0.6)",
          "rgba(54, 162, 235, 0.6)",
          "rgba(255, 206, 86, 0.6)",
          "rgba(75, 192, 192, 0.6)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(75, 192, 192, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "right",
      },
      title: {
        display: true,
        text: "유형별 입찰공고 분포",
        font: { size: 16 },
      },
    },
  };

  return <Pie data={chartData} options={options} />;
}

export default TypeChart;
