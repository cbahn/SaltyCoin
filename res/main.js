const context = document.getElementById("chart").getContext("2d");
const upElement = document.getElementById("up");
const downElement = document.getElementById("down");
const currentValueElement = document.getElementById("currentValue");
const chartContainer = new ChartContainer(context);
const dataContainer = new DataContainer();

function tick() {  
  $.ajax({
    url:'100_values',
    dataType: 'json',
    success: function(ajaxResponse) {
      // Begin async


      const data = dataContainer.replace(ajaxResponse);
      chartContainer.setData(dataContainer.replace(ajaxResponse));
      const currentValue = data[data.length-1].y.toFixed(2);
      const previousValue = data[data.length-2].y.toFixed(2);
      currentValueElement.textContent = currentValue;
      if (currentValue > previousValue) {
          upElement.style.display = null;
          downElement.style.display = "none";
      }
      else {
          upElement.style.display = "none";
          downElement.style.display = null;
      }

      // End async
    }
  });
}

tickInterval = 1000;

tick();
window.setInterval(() => tick(), tickInterval);