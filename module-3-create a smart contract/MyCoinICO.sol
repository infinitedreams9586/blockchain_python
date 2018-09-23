// MyCoin ICO

//compiler version
pragma solidity ^0.4.11;

contract MyCoinIco {
    
    // Introducing the maximum supply of MyCoins available for sale
    uint public max_mycoins = 1000000;
    
    // Introducing the USD to MyCoins conversion rate
    uint public usd_to_mycoins = 1000;
    
    // Introducing the total number of MyCoins already bought
    uint public total_mycoins_bought = 0;
    
    // Mapping from the investor address to its equity in MyCoins and USD
    mapping(address => uint) equity_mycoin;
    mapping(address => uint) equity_usd;
    
    // Checking if an investor can buy MyCoins
    modifier can_buy_mycoins(uint usd_invested) {
        require (usd_invested * usd_to_mycoins <= (max_mycoins - total_mycoins_bought));
        _;
    }
    
    // Getting the equity in MyCoins of an investor
    function equity_in_mycoins(address investor) external constant returns (uint) {
        return equity_mycoin[investor];
    }
    
    //Getting the equity in USD of an investor
    function equity_in_usd(address investor) external constant returns (uint) {
        return equity_usd[investor];
    }
    
    //Buying MyCoins
    function buy_mycoins(address investor, uint usd_invested) external 
    can_buy_mycoins(usd_invested) {
        uint mycoins_bought = usd_invested * usd_to_mycoins;
        equity_mycoin[investor] += mycoins_bought;
        equity_usd[investor] = equity_mycoin[investor] / usd_to_mycoins;
        total_mycoins_bought += mycoins_bought;
    }
    
    //Selling MyCoins
    function sell_mycoins(address investor, uint mycoins_tosell) external {
        uint total_mycoins_investor_has = equity_mycoin[investor];
        if (total_mycoins_investor_has >= mycoins_tosell){
            equity_mycoin[investor] -= mycoins_tosell;
            equity_usd[investor] = equity_mycoin[investor] / usd_to_mycoins;
            total_mycoins_bought -= mycoins_tosell;
        }
    }
    
}
