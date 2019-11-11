function drawBar(id, data) {
    var ctx = document.getElementById(id);
    var labels = [];
    for (var i = 0; i < data.length; i++){
        labels.push(data[i]['x']);
    }
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: "rgba(14,72,100,1)",
                strokeColor: "black",
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}
function drawPie(id, data) {
    var ctx = document.getElementById(id);
    var labels = [];
    for (var i = 0; i < data.length - 1; i++){
        labels.push(data[i]['x']);
    }
    var values = [];
    for (var j = 0; j < data.length - 1; j++){
        values.push(data[j]['y']);
    }
    var myLineChart = new Chart(ctx, {
        type: 'polarArea',
        data: {
            labels: labels,
            datasets: [{
                backgroundColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                strokeColor: "black",
                borderWidth: 1,
                data : values
            }]
        }
    });
}