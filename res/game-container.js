
class GameContainer {
    USD;
    NACL;

    constructor(startingUSD, startingNACL) {
        this.USD = startingUSD;
        this.NACL = startingNACL;
    }

    buy(price, amount) {
        this.trade(price,amount);
    }

    sell(price, amount) {
        this.trade(price, -amount);
    }

    trade(price, amount) {
        var newUSD = this.USD - price*amount;
        var newNACL = this.NACL + amount;

        if( newUSD < 0 ) {
            throw 'Not enough USD to complete trade';
        }
        if( newNACL < 0) {
            throw 'Not enough Salt to complete trade';
        }

        this.USD = newUSD;
        this.NACL = newNACL;
    }

    maxBuy(price) {
        return (this.USD/price);
    }

    maxSell(price) {
        return this.NACL;
    }

}