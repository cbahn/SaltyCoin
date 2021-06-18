
class DataContainer {
    walker;
    data;
    dataLength;

    constructor(dataLength) {
        this.dataLength = dataLength;
        this.data = new Array(this.dataLength).fill(0);
    }

    replace(newData) {
        this.data = newData;
    }

    getLatestValue() {
        return this.data.slice(-1)[0];
    }

    /**
     * Return the data formatted in the form that the chart want
     * example return: [{x:3452,y:0},{x:5239,y:1},{x:9032,y:2}]
     */
    getDataForChart() {
        return this.data.map((item, index) => {
            return {
                x: index,
                y: item
            };
        });
    }

}