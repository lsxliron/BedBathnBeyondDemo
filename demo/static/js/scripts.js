(function(){
  // Activate Parallax
  $('.parallax').parallax();

  $('#lineChartBtn').on('click', function(){
    $.ajax({
      url:'/randomizeLineChart/',
      type: 'POST',
      datatype: "json",
      data:{csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(), aspect:$('#aspect').val()},
      success: function(data){
        $("#lineChartDiv").html(data.svg)
      }
    })
  })

  $('#scatterPlotBtn').on('click', function(){
    $.ajax({
      url:'/randomizeScatterPlot/',
      type: 'POST',
      datatype: "json",
      data:{csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(), aspect:$('#aspect').val()},
      success: function(data){
        $("#scatterPlotDiv").html(data.svg)
      }
    })
  })
  
})()