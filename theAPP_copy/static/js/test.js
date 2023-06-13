
 $('.spiderChart').highcharts({

    chart: {
        polar: true,
        type: 'line',
        style: {
          fontFamily: "Georgia, serif", // default font
          fontSize: '12px'
        }
    },

    colors: ['#0067ac', '#a02842', '#007680'],

    pane: {
        size: '80%'
    },

    xAxis: {
        categories: ["Time", "Cost Saving", "Productivity", "Reduction in Errors", "ROI", "Revenue Increase", "Payback Period"],
        tickmarkPlacement: 'on',
        lineWidth: 0
    },

    yAxis: {
        gridLineInterpolation: 'polygon',
        lineWidth: 0,
        min: 0,
        max: 60,
        tickInterval: 5
    },

    tooltip: {
        shared: true,
        pointFormat: '<span style="color:{series.color}"> <b>{point.y:,.0f}%</b><br/>'
    },

    legend: {
        enabled: false
    },

    series: [{    
        data: [55, 20, 43, 39, 18, 15, 5],
        pointPlacement: 'on'
    }]
});


