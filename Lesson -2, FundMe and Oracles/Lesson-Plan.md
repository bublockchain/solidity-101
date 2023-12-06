# Lesson -2

## [Slidedeck](https://docs.google.com/presentation/d/1yqEW0564v9CnwOyB_ZTccEWcSgS5uZBJOOixesa6wjA/edit?usp=sharing)

## [Chainlink Price Feeds](https://docs.chain.link/data-feeds/price-feeds/addresses?network=ethereum&page=1&search=ETH+%2F+USD)

## [Foundry Docs](https://book.getfoundry.sh)

# Creating FundMe.sol

Make a new directory and make it a foundry project

```
mkdir FundMe
cd FundMe
forge init
```

Open the folder in your editor of choice and delete the boilerplate contracts in `/src`, `/test`, and `/srcipt`

Create the file `FundMe.sol` in `/src`

Define the solidity version and create the contract

```
pragma solidity ^0.8.20;

contract FundMe{

}
```

Create the fund function and make it payable to be able to recieve ether

```
function fund() public payable {

}
```

Lets create something to track the wallets that have sent us money and how much they have sent us

```
address[] public funders;
mapping(address => uint) public addressToAmountFunded;
```

Lets update fund() to update these

```
function fund() public payable {
        funders.push(msg.sender);
        addressToAmountFunded[msg.sender] += msg.value;
    }
```

Now that we have money lets make a function to withdraw it to our wallet

```
function withdraw() public {

}
```

Lets make sure that we do have money first or we're going to waste gas calling the function

```
function withdraw() public {
        require(address(this).balance > 0, "You have no funds to withdraw");
    }
```

Now we can send the ether to our wallet

```
function withdraw() public {
        require(address(this).balance > 0, "You have no funds to withdraw");
        bool sendSuccess = payable(msg.sender).send(address(this).balance);
        require(sendSuccess, "Failed to withdraw funds from contract");
    }
```

But there's a problem anyone can call this and send the money to their wallet. Lets make it so that only we can call the function. We'll do this with a modifier

```
error OnlyOwner();

modifier onlyOwner() {
        if (msg.sender != owner) {
            revert OnlyOwner();
        }
        _;
    }
```

Let's set the owner variable when we create the contract with our constructor

```
address owner;

constructor() {
        owner = msg.sender;
    }
```

And finally lets update withdraw with our modifier

```
function withdraw() public onlyOwner {
        require(address(this).balance > 0, "You have no funds to withdraw");
        bool sendSuccess = payable(msg.sender).send(address(this).balance);
        require(sendSuccess, "Failed to withdraw funds from contract");
    }
```

This is our contract pretty much done but lets add some functionality. Lets make it so users ahve to send above a minmum USD amount when they donate to our contract

This comes with a problem, theyre sending us ETH not USD so we will need the price of ETH to USD. How do we get that though? Can we get it through an API? We can get it through the WEB3 version of API's called Oracles. Lets create our getPrice and getConversion fucntions that will hold the logic to connect to an Oracle.

```
function getPrice() public view returns (uint256){

}

function getConversionRate(uint256 ethAmount) public view returns (uint256) {

}
```

Instead of downloading and using a full oracle contract in our project we're going to use an Interface for the already deployed contract. We're going to use chainlinks ETh/USD contract on the Sepolia Testnet. Lets download the Interface contract via NPM into our project.

```
npm install @chainlink/contracts --save
```

Lets import the contract int our FundMe.sol

```
import {AggregatorV3Interface} from "node_modules/@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
```

Let's use the Interface to get the price of ETH/USD inside getPrice()

```
 function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x694AA1769357215DE4FAC081bf1f309aDC325306);
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 1e10);
    }
```

The address inside our interface is the already deployed contract on the Seplia network which can be found [here](https://docs.chain.link/data-feeds/price-feeds/addresses?network=ethereum&page=1&search=ETH+%2F+USD)

Lets use the conversion rate to get the amount of ETH sent in USD inside getConversionRate()

```
function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1e18;
        return ethAmountInUsd;
    }
```

Now that we have our conversion rate lets set our minimum USD.

```
 uint256 public MINIMUM_USD = 5e18;
```

Now we can set a require statement in our fund() function

```
function fund() public payable {
        require(getConversionRate(msg.value) >= MINIMUM_USD, "You need to spend more ETH");
        funders.push(msg.sender);
        addressToAmountFunded[msg.sender] += msg.value;
    }
```

And thats it our FundMe contract is fully done and we can deploy it with a script. Lets create one so we can test it out. Create `FundMe.s.sol`in `/script`

let's set the solidity version and make our contract same as always

```
pragma solidity ^0.8.20;

contract FundMeScript {

}
```

Now let's import some helper contracts from Foundry and our FundMe contract.

```
import {script, console2} from "../lib/forge-std/src/Script.sol";
import {FundMe} from "../src/FundMe.sol";
```

To implement methods from our script contract we have to make FundMeScript a child of Script

```
contract FundMeScript is Script {

}
```

Now we have to implement the run() function that goes in all scripts

```
function run() public {

}
```

Now lets create an instance of our fundMe contract which when put after vm.startBroadcast will deploy our contract

```
function run() public {
        vm.startBroadcast();
        FundMe fund = new FundMe();
        vm.stopBroadcast();
    }
```

Lets also add a transaction in sending 1 ether to our contract and print out the value of our contract to make sure it worked

```
function run() public {
        vm.startBroadcast();
        FundMe fund = new FundMe();
        fund.fund{value: 1e18}();
        vm.stopBroadcast();
        console2.log(address(fund).balance);
    }
```

That's our fully completed script and FundMe contracts!
