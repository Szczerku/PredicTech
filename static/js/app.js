$(document).ready(function () {
    const MAX_DATA_COUNT = 50;

    function configureChart(ctx, label, backgroundColor, borderColor) {
        return new Chart(ctx, {
            type: "line",
            data: {
                labels: [],
                datasets: [
                    {
                        label: label,
                        fill: true,
                        backgroundColor: backgroundColor,
                        borderColor: borderColor,
                        lineTension: 0,
                        data: []
                    }
                ]
            },
            options: {
                scales: {
                    x: {
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        }
                    }
                },
                responsive: true,
                maintainAspectRatio: false,
            },
        });
    }

    function addData(lineChart, label, data) {
        lineChart.data.labels.push(label);
        lineChart.data.datasets.forEach((dataset) => {
            dataset.data.push(data);
        });
        lineChart.update();
    }

    function removeFirstData(lineChart) {
        lineChart.data.labels.splice(0, 1);
        lineChart.data.datasets.forEach((dataset) => {
            dataset.data.shift();
        });
        lineChart.update();
    }

    function handleSocketData(lineChart, msg) {
        console.log(`Otrzymano dane z czujnika :: ${msg.date} :: ${msg.value}`);

        if (lineChart.data.labels.length > MAX_DATA_COUNT) {
            removeFirstData(lineChart);
        }
        addData(lineChart, msg.date, msg.value);
    }

    const ctx1 = document.getElementById("lineChart1").getContext("2d");
    const lineChart1 = configureChart(ctx1, "Voltage 1", "rgba(75,192,192,0.5)", "rgb(75, 192, 192)");

    const ctx2 = document.getElementById("lineChart2").getContext("2d");
    const lineChart2 = configureChart(ctx2, "Voltage 2", "rgba(255, 0, 255, 0.5)", "rgb(255,0 , 255)");

    const ctx3 = document.getElementById("lineChart3").getContext("2d");
    const lineChart3 = configureChart(ctx3, "Voltage 3", "rgba(31,53,235,0.5)", "rgb(31, 53, 235)");

    var socket = io.connect();

    socket.on("updateSensorData1", function (msg) {
        handleSocketData(lineChart1, msg);
    });

    socket.on("updateSensorData2", function (msg) {
        handleSocketData(lineChart2, msg);
    });

    socket.on("updateSensorData3", function (msg) {
        handleSocketData(lineChart3, msg);
    });
});
