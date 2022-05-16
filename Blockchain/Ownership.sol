pragma solidity ^0.5.0;


contract Ownership {
    address payable[] private _owners;
    address payable private _superOwner;

    constructor() internal {
        _superOwner = msg.sender;
        _owners.push(msg.sender);
    }

    modifier onlyOwner {
        require(isOwner(msg.sender), "Only owners have access to this");
        _;
    }

    modifier onlySuperOwner() {
        require(isSuperOwner(msg.sender), "Only the user with Admin rights can add owners");
        _;
    }

    function addOwner(address payable newOwner) public onlySuperOwner {
        require(!isOwner(newOwner), "This account is already owner");
        _owners.push(newOwner);
    }

    function getOwnersCount() public view returns(uint) {
        return _owners.length;
    }

    function getOwners() public view returns(address payable[] memory ) {
        return _owners ;
    }


    function indexOf(address owner) internal view returns(uint) {
    uint ind = 999;
    for (uint i = 0; i < _owners.length; i++) {
        if (_owners[i] == owner) {
            ind = i;
        }
    }
    return ind;
    }

    function removeByIndex(uint i) internal {
    while (i < _owners.length-1) {
        _owners[i] = _owners[i+1];
        i++;
    }
    _owners.length--;
    }

    function removeOwner(address currentOwner) public onlySuperOwner {
        uint i = indexOf(currentOwner);
        require(i != 999, "There are no such owners with the specified address");
        removeByIndex(i);
    }

    function isOwner(address checkingAddress) public view returns(bool){
        uint i = indexOf(checkingAddress);
        if (i != 999) {
            return true;
        }
        else {
            return false;
        }
    }
    function isSuperOwner(address checkingAddress) public view returns(bool) {
        if (checkingAddress == _superOwner) {
            return true;
        }
        else {
            return false;
        }
    }
}
