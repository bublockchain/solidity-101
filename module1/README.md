# Module 1: Development Environment
## Overview
This module contains the following files:
```
module1/
├── .gitignore
└── README.md
```
It is intentionally "empty". You will be creating new files later. 


## Introduction
This module will introduce you to the development environment that you 
will use for solidity blockchain development. You will learn how to install 
and configure the tools that you will be using to develop smart contracts in
solidity.

* [ ] Download and install [Visual Studio Code](https://code.visualstudio.com/)
* [ ] Download and install [Truffle](https://www.trufflesuite.com/truffle)

## Truffle
Now that you have installed Truffle, you can use it to create a new project.

* [ ] Create a new project using the command `truffle init`
    * Make sure that you are in the `module1` directory when you run this command.
    * Use `cd module1` to change directories.
* [ ] Verify that your files match the following:
```
module1/
├── contracts/
│   └── .gitkeep
├── migrations/
│   └── .gitkeep
├── test/
│   └── .gitkeep
├── .gitignore
├── README.md
└── truffle-config.js
```

## Creating a Smart Contract
Now that you have a project, you can create a smart contract. 

* [ ] Create a new file called `HelloWorld.sol` in the `module1 > contracts` directory.
* [ ] Add the following code:
```solidity
// Specify the version of Solidity, the compiler will use for compilation
pragma solidity ^0.8.0;

// Define a contract named 'HelloWorld'
contract HelloWorld {

  // Define a function that does not accept any arguments and returns a string
  function sayHello() public pure returns (string memory) {
    return "Hello, World!";
  }
}
```
* [ ] Build your project using the command `truffle compile`
* [ ] Run the tests using the command `truffle test`

