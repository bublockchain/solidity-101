# Lesson -1

[Slidedeck]()

[Foundry-Documentation](https://book.getfoundry.sh)

## Installing Foundry

Open your terminal and run this command
```
curl -L https://foundry.paradigm.xyz | bash
```

Once that's done running it should give you a command like 
```
source /Users/xxxxx/.zshenv'
```

Run this to add foundryup to your path. After run ```foundryup``` to complete installation

Lets create a contract to store all of our freinds favorite numbers.

## Create a foundry project

First create a new folder with ```mkdir SimpleStorage``` then go into the folder with ```cd SimpleStorage```

Run ```forge init``` to create a new foundry project then delete the boilerplate contracts in ```/src``` ```/test``` and ```/script```

Create ```SimpleStorage.sol``` in the ```/src```

## Create SimpleStorage.sol

We start all solidity files the same way with ```pragma``` to set the solidity version
```
pragma solidity ^0.8.20
```

Now we need to create the contract
```
contract SimpleStorage {}
```

Now lets create a variable to store the favorite number

```
uint256 private favoriteNumber;
```

Now that we have our number we need a way to store something in it for this we'll use functions
```
function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
```

Becuase our number is private we'll also need someway to access the variable so we'll use a function
```
function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }
```

We have a problem. This contract is fine if we only have one friend but we have lots of friends favorite numbers we want to store. Lets use another data object a struct to store a name with a number. 
```
struct People {
        uint256 favoriteNumber;
        string name;
    }
```

We also need a place to store these newly created People structs so we'll create an array of People structs
```
People[] public people;
```

Lets also create a function to add new people 
```
function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
    }
```
Because the people array is public we don't need to create a retreive function for it.

But there's a problem we want to know our friend John's favorite number but we don't remember what number in the array John is. Instead of parsing through the array until we find John we can fix this with another data object a mapping. We'll create a string to uint256 mapping to store names to numbers.

```
mapping(string => uint256) public nameToFavoriteNumber;
```

Lets modify our addPerson function to also add a new person to our mapping

```
function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
```

After that our contracts fully done. Now it's time to deploy it.

## Deploy via Command Line

First run ```forge compile``` to compile your contarct and make sure theres no typos

Now create a new terminal tab and run ```anvil```

This will give us a bunch of information about the test network we just launched. We're gonna need a few pieces of this to launch our contract. The RPC URL and a private key from a funded wallet. 

We're gonna store this info in our ```.env``` file. Create a ```.env``` file in the top level of our project. Then store our info in it like this

```
RPC_URL=http://127.0.0.1:xxxx
PRIVATE_KEY=0x000000000000000
```

Now it's time to launch our contract.

Create a new terminal tab with anvil still running and run ```source .env```

Now run

```
forge create SimpleStorage --rpc-url $RPC_URL --private-key $PRIVATE_KEY
```

When this goes through you will get an address that your contract is deployed to copy this and we'll add it to our ```.env``` like this 

```
RPC_URL=http://127.0.0.1:xxxx
PRIVATE_KEY=0x000000000000000
CONTRACT_ADDRESS=0x00000000000
```

Now we can send our contract transactions to see if it's working
## Testing with Command Line

We can send our contract transactions with the foundry ```cast``` command. 

Lets store our favorite number in the contract. 

```
cast send $CONTRACT_ADDRESS "store(uint256 _favoriteNumber)" xx --rpc-url $RPC_URL --private-key $PRIVATE_KEY
```

Now lets call the retrieve function to make sure our number got stored

```
cast call $CONTRACT_ADDRESS "retrieve()" --rpc-url $RPC_URL
```

This will return your number in hexidecimal to convert it to decimal run this command

```
cast --to-base 0x000 dec
```

Thats it we created and deployed a contract with foundry. Feel free to call more of the functions and test out the rest of the contract
