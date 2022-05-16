pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "./Ownership.sol";

contract KinoToken is ERC20, ERC20Detailed, Ownership {
    uint exchange_rate = 1000;

    constructor(string memory name, string memory symbol) 
    ERC20Detailed(name, symbol, 18) 
    public payable {}


    function mint(address acc, uint amount) internal{
        _mint(acc, amount);
    }

    function splitProfit() public payable onlySuperOwner{
        uint sharableAmount = address(this).balance - totalSupply() / exchange_rate;
        require(sharableAmount != 0, "Nothing to share, sharable amount of Eth equals to 0");
        address payable[] memory owners  = getOwners();
        uint ownersCount = getOwnersCount();
        
        uint share = sharableAmount / ownersCount;
        for (uint i = 0; i < ownersCount; i++) {
            owners[i].transfer(share);    
        }

   } 


    function buyTokens() public payable {
        uint amount = msg.value * exchange_rate;
        mint(msg.sender, amount); 
    }

    function withdraw(uint amount, address payable recipient) public {
        uint amountEth = amount / exchange_rate;
        recipient.transfer(amountEth);
        _burn(msg.sender, amount);
    }

    function getContractBalance() public view onlyOwner returns(uint) {
        return address(this).balance;
    }


    function() external payable {
    }

}
