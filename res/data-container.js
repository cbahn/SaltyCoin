class RandomWalker {
    currentValue;
    upChance;
    changeDirectionPenalty;
    currentDirection;

    constructor() {
        this.currentValue = 0;
        this.upChance = 0.5;
        this.changeDirectionPenalty = 0;
        this.currentDirection = 1;
    }

    next() {
        const random = Math.random();
        const threshold = this.upChance + (this.currentDirection * this.changeDirectionPenalty);
        this.currentDirection = threshold > random ? 1 : -1;
        const magnitude = (Math.random() + Math.random()) * 0.01;
        this.currentValue = this.currentValue * (1 + (this.currentDirection * magnitude));
        return this.currentValue;
    }
}



dataLength = 100;

class DataContainer {
    walker;
    data;

    constructor() {
        const walker = new RandomWalker();
        walker.currentValue = 10;
        walker.upChance = 0.52;
        walker.changeDirectionPenalty = .25;


        this.data = new Array(dataLength).fill(3);

        // Fill the data array with the number 3
        //this.data = new Array(dataLength).fill(undefined).map(() => walker.next());
        //this.data = new Array(dataLength).fill(3);

        this.walker = walker;
    }

    next() {
        this.data.shift();
        this.data.push(this.walker.next());
        
        return this.data.map((item, index) => {
            return {
                x: index,
                y: item
            };
        });
    }

    replace(newData) {
        this.data = newData;

        return this.data.map((item, index) => {
            return {
                x: index,
                y: item
            };
        });

    }

}