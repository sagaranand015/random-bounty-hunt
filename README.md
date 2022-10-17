# Random Bounty Hunt

### Aimed at bounty
https://gitcoin.co/issue/29366

### Background of Randomness on Algorand
1. Algorand Blockchain now has a VRF(Verifiable Random Function) oracle deployed in TestNet. See: https://developer.algorand.org/articles/randomness-on-algorand/?from_query=randomness
2. TEAL(language of Smart contracts on Algorand) now has vrf_verify construct built within that allows for verification of the Random Number created by the VRF Oracle. 
3. Randomness on Algorand guide: https://developer.algorand.org/articles/usage-and-best-practices-for-randomness-beacon/?from_query=randomness

### Ideation
The bounty expects us to create ANY application, deployed on the Algorand Blockchain that uses randomness (via the VRF Oracle) on Algorand. The app can optionally verify the random number as given by the VRF Oracle. 

This app aims to create an application that leverages randomness available on Algorand Blockchain to allows users to solve challenges/bounties created by other users in the form of Algorand Assets. These assets might or might not have a physical value assoaicted with them. 
User workflows might be defined:
1. For a user creating a challenge/bounty:
    1. Create an asset in the form of a challenge/bountry
    2. The application takes care of putting this challenge in a chest RANDOMLY

2. For a user solving a challenge/bounty:
    1. Choose a challenge/bounty from a chest RANDOMLY
    2. Solve this challenge to gain access to the asset. 

Notes:
1. Assets might or might not have a monetary value associated with them. 
2. For assets with monetary value, 20% of the asset value is transferred to the creator, 10% to the application and 70% to the user gaining access to the token.
