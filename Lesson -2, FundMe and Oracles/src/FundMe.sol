pragma solidity ^0.8.20;

import {AggregatorV3Interface} from "node_modules/@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    uint256 public MINIMUM_USD;

    address[] public funders;
    mapping(address => uint) public addressToAmountFunded;

    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    constructor(uint256 _minimumUsd) {
        owner = msg.sender;
        MINIMUM_USD = _minimumUsd * 1e18;
    }

    function fund() public payable {
        require(
            getConversionRate(msg.value) >= MINIMUM_USD,
            "You need to spend more ETH"
        );
        funders.push(msg.sender);
        addressToAmountFunded[msg.sender] += msg.value;
    }

    function withdraw() public onlyOwner {
        require(address(this).balance > 0, "You have no funds to withdraw");
        bool sendSuccess = payable(msg.sender).send(address(this).balance);
        require(sendSuccess, "Failed to withdraw funds from contract");
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x694AA1769357215DE4FAC081bf1f309aDC325306
        );
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 1e10);
    }

    function getConversionRate(
        uint256 ethAmount
    ) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1e18;
        return ethAmountInUsd;
    }
}
