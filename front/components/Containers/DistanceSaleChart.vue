<template>
  <div class="container">
    <line-chart
      :chart-data="barChartData"
      :options="barChartOptions"
      :height="200"
    />
  </div>
</template>

<script>
    const chartColors = {
        red: "rgb(255, 99, 132)",
        orange: "rgb(255, 159, 64)",
        yellow: "rgb(255, 205, 86)",
        green: "rgb(75, 192, 192)",
        blue: "rgb(54, 162, 235)",
        purple: "rgb(153, 102, 255)",
        grey: "rgb(201, 203, 207)",
    }

    export default {
        data() {
            return {
                barChartData: {
                    labels: ["Jan", "Feb", "Mar"],
                    datasets: [
                        {
                            label: "Income",
                            // backgroundColor: ["red", "orange", "yellow"],
                            backgroundColor: [
                                chartColors.red,
                                chartColors.orange,
                                chartColors.yellow,
                            ],
                            data: [10, 15, 20],
                        },
                    ],
                },
                barChartOptions: {
                    responsive: true,
                    legend: {
                        display: false,
                    },
                    title: {
                        display: true,
                        text: "Monthly Income",
                    },
                    scales: {
                        yAxes: [
                            {
                                ticks: {
                                    beginAtZero: true,
                                },
                            },
                        ],
                    },
                },
            }
        },
    }
</script>
