# Random Bounty Hunt

### Aimed at bounty
https://gitcoin.co/issue/29366

### Background of Randomness on Algorand
1. Algorand Blockchain now has a VRF(Verifiable Random Function) oracle deployed in TestNet. See: https://developer.algorand.org/articles/randomness-on-algorand/?from_query=randomness
2. TEAL(language of Smart contracts on Algorand) now has vrf_verify construct built within that allows for verification of the Random Number created by the VRF Oracle. 
3. Randomness on Algorand guide: https://developer.algorand.org/articles/usage-and-best-practices-for-randomness-beacon/?from_query=randomness

### Ideation
The bounty expects us to create ANY application, deployed on the Algorand Blockchain that uses randomness (via the VRF Oracle) on Algorand. The app can optionally verify the random number as given by the VRF Oracle. 

### Implementation
This DApp aims to create an application that leverages randomness available on Algorand Blockchain to allows users/institutions to execute a type of Random Sampling from a list of dataset configured in this dApp. 
Solution Approach:
1. The Algorand randomness beacon returns a list of 38 random values from an already deployed smart contract. 
2. The DApp uses systematic random sampling using the random values found in [1]
3. The Dapp also leverages Dune to get the datasets on the fly. Various tasks running in the backend will make sure that these datasets are up to date at all times. 
4. The DApp will take care of getting the random number from the randomness beacon on-chain and use that to perform random sampling on the dataset chosen
5. The application returns the set of sampled data from the dataset to the user.
6. The application also makes sure to use some user data(maybe an API key or an auth token created using time) to generate random data from the beacon. 

