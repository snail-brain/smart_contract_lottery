//SPDX-License-Identifier:MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract lottery {
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal priceFeed;

    constructor(address _priceFeedAddress) public {
        usdEntryFee = 50 * 10**18;
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
    }

    function enter() public {
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = priceFeed.latestRoundData;
        uint256 adjustedPrice = Uint256(price) * 10**18;
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public {}

    function endLottery() public {}
}
