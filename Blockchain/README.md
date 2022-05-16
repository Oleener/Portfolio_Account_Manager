# Portfolio Account Manager V3
Version 3 focuses on integrating Portfolio Manager with Ethereum Blockchain through creating an ERC20-compatible token and provide users with the ability to purchase and sell it as well as to get rewarded (new user is created, user has verified email, user purchases assets for the portfolio). For the owners of the Potfolio Manager tool the interaction with the blockchain and with the token allows to motetize the application and to attract more clients through the rewards system. This Blockchain folder consists of the following elements:
* Smart contracts to create ERC20-compatible token and specific functions to manage the token
* TBD - Libraries with functions and settings for integrating the main application (Portfolio Manager) with the blockchain (create and restore accounts (wallets), add/remove owners, purchase/sell tokens, manage the total supply of the token and Ethereum amount available on the contract for the owners).
 
---

## Technologies 

AWS Services + Ganache CLI: 

Elastic Compute (EC2) Cloud is a part of Amazon.com's cloud-computing platform, Amazon Web Services, that allows users to rent virtual computers on which to run their own computer applications. EC2 instance and Ganache CLI are used to create a publicly accessible blockchain for this project's test purposes. 

Additionally, this project uses the following packages: 

* Remix - A browser-based compiler and IDE that enables users to build Etherum contracts with Solidity language and to debug any transactions. 

* Solidity - An object-oriented, high-level language for implementing smart contracts. 

* MetaMask - A crypto wallet and gateway to blockchain apps. It is used in the project to test smart contracts functionality.

* web3 - A Python library used for interacting with Ethereum (TBD). It is used (will be used) in the main application (Portfolio Manager) to establish a connection to the test publicly available blockchain (hosted on AWS EC2) and to interact with the smart contracts deployed on that network. 

---

## Installation Guide 

TBD

---

## Usage 

For smart contracts testing download both KinoCoin.sol and Ownership.sol smart contracts and open them in Remix SDE (or similar tools). 

You can deploy and test these contracts locally or on test blockchain (run on AWS EC2 instance). For the second option you can use Metamask (or similar tools to interact with Ethereum blockchains) to create a new connection:
* RPC URL: http://ec2-34-201-91-146.compute-1.amazonaws.com:7545
* Chain ID: 1234

After getting the connection established you can deploy KinoCoin.sol (no need to deploy Ownership.sol separately - it's inherited by KinoCoin.sol). The test network has 10 test accounts with the balance - you can use them for testing:

**Available Accounts:**

(0) 0x9E770eB12148Aff8eD9481e8BB053b2eDCd466e3 (100 ETH)

(1) 0x8444B3127e667ea2019515A0dd19e70a3f0F5dCC (100 ETH)

(2) 0x08970F6D6077e0011957197dF08B4fE46d086772 (100 ETH)

(3) 0xfD1b27cC249902035d7996385A8B11578D41C93B (100 ETH)

(4) 0x3bDf2C5578d1F682bF47ddCFd54F91eDaD0bbc4e (100 ETH)

(5) 0x9E420c91aaDBfA270aF0FeeE5f58b8d1d1498d24 (100 ETH)

(6) 0xe667cE15490358301De71307D7CbAd147244096f (100 ETH)

(7) 0x7D0D7908E3fB3427cD056bD71986259240AB7391 (100 ETH)

(8) 0x470F9AAD0203914B3418d99A27a379Af212F90F0 (100 ETH)

(9) 0xe84Ee126E82A365D25C7A15D5B729E8422b80cF3 (100 ETH)

**Private Keys**:

(0) 0x32037ffd074a6186a5e5e72031a10e5ace3eea2c711b426e20f79bdf156916f3

(1) 0x694d122049c4c69a72fceec375c536ca74d27882108137b9f771c9a3f5ed6cfc

(2) 0x57bd1821987e073d953b5f9f060a358845acec9ad0cfb5f0e64fd817e0eaa326

(3) 0xcf81a5dfe57a50e86408c9ac0e85d787ca0bb43269486830122669ea16c73430

(4) 0xc29e27f7bf82e728758c4275a0471ed04f89f49243259776e4f4d86a7f3b8b15

(5) 0xa80c8b402045b4974599d0e135579a87839027a1a89f897c5d40a6ef466ea6b3

(6) 0xeed2004e7964477f60622d3bbc793ea07183c5d1340cb16d6c71ec012d7a2b0b

(7) 0x34efefc615da240fb13dce8565585a58b08ed2da39ca4d1a7cbc3a4da8a29397

(8) 0x6aaa518d669c1a2bbd104f53d0953e9c370be3ba85517acdd182bf88f635c6fb

(9) 0xbbc01ce30668b5146d8959a910a4145cbe32fbb01cec88a287bac2b99befa302

---

## Presentation  

Additionally to this README file the Powerpoint presentation available in the folder also summarizes the goal and the features available/will be available in Portfolio Manager v. 3.

---

## Contributors

### Portfolio Account Manager Version 3 Brought To you by:

Kirill Panov (us.kirpa1986@gmail.com)
Isaiah Tensae (isaiahtensae@gmail.com)
Olena Shemedyuk (olenashemedyuk@gmail.com)
Nomi Enkhbold (nomienk28@gmail.com)

---

## License

MIT
