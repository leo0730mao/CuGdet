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
                    //'rgba(255, 99, 132, 1)',
                    '#D95749',
                    '#563D94',
                    '#D9C349',
                    '#37A44F',
                    '#EC9E96',
                    '#9B88CA',
                    '#A29652',
                    '#69D180',
                    '#8D7B18',
                    '#8D2318'
                ],
                borderColor: [
                    '#D95749',
                    '#563D94',
                    '#D9C349',
                    '#37A44F',
                    '#EC9E96',
                    '#9B88CA',
                    '#A29652',
                    '#69D180',
                    '#8D7B18',
                    '#8D2318'
                ],
                strokeColor: "black",
                borderWidth: 1,
                data : values
            }]
        }
    });
}