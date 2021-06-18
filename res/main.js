
numberOfValues = 100;

const game = new GameContainer(1000,0); // start game with $1000

const context = $("#chart")[0].getContext("2d");
const currentValueElement = $("#currentValue");
const chartContainer = new ChartContainer(context);
const dataContainer = new DataContainer(numberOfValues);


function updateMoney() {
  $("#yourUSD").text(game.USD);
  $("#yourNACL").text(game.NACL);
}

function buyAll() {
  price = dataContainer.getLatestValue().toFixed(2)
  game.buy(price, 1);
  updateMoney();
}

function sellAll() {
  price = dataContainer.getLatestValue().toFixed(2)
  game.sell(price, 1);
  updateMoney;
}




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

updateMoney();

tickInterval = 1000; //1 second

tick();
window.setInterval(() => tick(), tickInterval);