function drawBar(id, data, label, monthly) {
    var ctx = document.getElementById(id);
    var myDate = new Date();
    var year = myDate.getFullYear();
    var month = myDate.getMonth();
    var day = myDate.getDate();
    var labels = [];
    var values = [];
    var i = 1;
    var upbound = 0;
    if (monthly) upbound = month + 1;
    else upbound = day;
    while (i <= upbound){
        labels.push(i);
        values.push(0);
        i++;
    }
    for (var j = 0; j < data.length - 1; j++){
        values[parseInt(data[j]['x']) - 1] = data[j]['y'];
    }
    labels.push(data[data.length - 1]['x']);
    values.push(data[data.length - 1]['y']);
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: values,
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
function drawLine(id, data) {
    var ctx = document.getElementById(id);
    var labels = [];
    var values = [];
    var i = 1;
    while (i < 32 && i <= parseInt(data[data.length - 1]['x'])){
        labels.push(i);
        values.push(0);
        i++;
    }
    for (var j = 0; j < data.length; j++){
        values[parseInt(data[j]['x']) - 1] = data[j]['y'];
    }
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            label: labels,
            datasets: [{
                data: values,
                backgroundColor: "rgba(14,72,100,1)",
                strokeColor: "black",
                borderWidth: 1
            }],
            options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
        }
    });

}