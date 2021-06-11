const gridColor = "#33ccff";
const tickColor = "#66ff99";
const tickFontSize = 18;
const lineColor = "#fa8072";

class ChartContainer {
    config = {
        type: "scatter",
        data: {
            datasets: [
                {
                    borderColor: lineColor,
                    backgroundColor: lineColor,
                    showLine: true,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            animation: {
                duration: 0
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: false,
                }
            },
            scales: {
                y: {
                    grid: {
                        color: gridColor
                    },
                    ticks: {
                        color: tickColor,
                        callback: x => `$${x}`,
                        font: {
                            size: tickFontSize
                        }
                    }
                },
                x: {
                    grid: {
                        color: gridColor
                    },
                    ticks: {
                        color: tickColor,
                        display: false
                    }
                }
            }
        },
    }

    constructor(context) {
        this.chart = new Chart(context, this.config);
    }

    setData(data) {
        this.chart.data.datasets[0].data = data;
        this.chart.update();
    }
}