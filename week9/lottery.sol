pragma solidity ^0.4.0;

contract Lottery {
    
    mapping (uint8 => address[]) playersByNumber;
    Ticket[] tickets;
    uint8 minBetSize;
    address owner;
    enum LotteryState { Accepting, Finished }
    LotteryState state; 

    /// Create a new lottery with minimum betsize.
    function Lottery(uint8 _minBetSize) public {
        owner = msg.sender;
        minBetSize = _minBetSize;
        state = LotteryState.Accepting;
    }
    
    function makeBet(uint8 _lotteryNumber) {
        require(
            state == LotteryState.Accepting,
            "Rejected: Lottery closed."
        );
        require(msg.value > minBetSize ether);
        
        playersByNumber[_lotteryNumber].push(msg.sender)
        return;
    }
    
    function calculateWinner() {
        // random number generator with limit based on Ticket.length
        require(msg.sender == owner);
        state = LotteryState.Finished;
        uint8 winningNumber = random();
        distributeFunds(winningNumber);
        selfdestruct(owner);
    }

    function distributeFunds(uint8 winningNumber) private returns(uint256) {
        uint256 winnerCount = playersByNumber[winningNumber].length;
                require(winnerCount == 1);
        if (winnerCount > 0) {
            uint256 balanceToDistribute = this.balance/(2*winnerCount);
            for (uint i = 0; i<winnerCount; i++) {
                require(i==0);
                playersByNumber[winningNumber][i].transfer(balanceToDistribute);
            }
        }
        return this.balance;
    }
}
