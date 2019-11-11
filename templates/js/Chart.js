function drawLinegraph(id, data, title){
    var linechart;
    linechart = echarts.init(document.getElementById(id));
    var option = {
        title: {
            text: title,
            x: 'center'
        },
        legend: {
            orient: 'horizontal',
            x: 'left',
            y: 'bottom',
            data:data['legend']
        },
        xAxis: {
            type: 'category',
            data: data['x']
        },
        yAxis: {
            type: 'value'
        },
        series: data['y'],
        grid:{
            x:50
        }
    };
    linechart.setOption(option);
    window.onresize = function(){
        linechart.resize();
    }
}

function drawPiegraph(id, data) {
    var piechart = echarts.init(document.getElementById(id));
    var legend = [];
    for(var i = 0; i < data.length; i++){
        legend.push(data[i]['name']);
    }
    piechart.setOption({
        title: {
            text: title,
            x: 'center'
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            y: 'bottom',
            data:legend
        },
        series: {
            label: {
                show:false
            },
            type: 'pie',
            data: data
        },
        grid:{
            x:25
        }
    });
    window.onresize = function(){
        piechart.resize();
    }
}