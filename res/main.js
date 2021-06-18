
numberOfValues = 100;


const context = $("#chart")[0].getContext("2d");
const currentValueElement = $("#currentValue");
const chartContainer = new ChartContainer(context);
const dataContainer = new DataContainer(numberOfValues);

function tick() {  
  $.ajax({
    url:'100_values',
    dataType: 'json',
    success: function(ajaxResponse) {

      // Begin async
      const data = dataContainer.replace(ajaxResponse);
      chartContainer.setData( dataContainer.getDataForChart() );
      const currentValue = dataContainer.getLatestValue().toFixed(2);
      currentValueElement.text(currentValue);
      // End async

    }
  });
}

tickInterval = 1000; //1 second

tick();
window.setInterval(() => tick(), tickInterval);