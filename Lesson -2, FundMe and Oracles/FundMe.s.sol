pragma solidity ^0.8.20;

import {Script, console2} from "../lib/forge-std/src/Script.sol";
import {FundMe} from "../src/FundMe.sol";

contract FundMeScript is Script {
    function run() public {
        vm.startBroadcast();
        FundMe fund = new FundMe(5);
        fund.fund{value: 1e18}();
        console2.log(address(fund).balance);
        vm.stopBroadcast();
    }
}
