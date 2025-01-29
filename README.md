# Cryptocurrency Exchange Trading and Arbitrage Detection

## Overview
This project implements a **graph-based approach** to cryptocurrency exchange trading, leveraging real-time exchange rates from the [CoinGecko API](https://www.coingecko.com/en/api). The program constructs a **directed weighted graph** of exchange rates between the top 7 cryptocurrencies and searches for **arbitrage opportunities**—scenarios where trading through multiple exchanges yields a profit.

## Features

### Core Functionality
- **Real-Time Exchange Rate Retrieval**: Fetches live exchange rates for the top 7 cryptocurrencies:
  - Bitcoin (`btc`)
  - Ethereum (`eth`)
  - Litecoin (`ltc`)
  - Bitcoin Cash (`bch`)
  - EOS (`eos`)
  - Cardano (`ada`)
  - Ripple (`xrp`)
- **Graph Representation**:
  - Builds a **directed weighted graph** where nodes represent currencies and edges represent exchange rates.
  - Creates bidirectional edges (`currency A → currency B` and `currency B → currency A`).
- **Arbitrage Detection**:
  - Searches for cycles where converting from one currency through a series of exchanges back to itself **results in a net gain**.
  - Identifies paths where the **product of exchange rates deviates from 1.0**, indicating arbitrage opportunities.

## API Usage
Exchange rate data is retrieved using:
```plaintext
https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,litecoin,bitcoin-cash,eos,cardano,ripple&vs_currencies=btc,eth,ltc,bch,eos,ada,xrp
```
The API response contains the exchange rates for each currency pair, structured as follows:
```json
{
  "ethereum": {"eth": 1.0, "btc": 0.0309095},
  "bitcoin": {"eth": 32.335902, "btc": 1.0}
}
```

## Program Workflow
1. **Fetch Exchange Rates**: Retrieve real-time cryptocurrency exchange rates from CoinGecko.
2. **Construct a Graph**:
   - Nodes represent cryptocurrencies.
   - Directed edges represent exchange rates.
3. **Find Paths and Compute Weights**:
   - Identify all possible paths between currency pairs.
   - Compute path weights by multiplying exchange rates along a path.
4. **Detect Arbitrage**:
   - Compare direct and indirect paths between currencies.
   - Identify paths where **returning to the original currency results in a net gain**.
5. **Output Arbitrage Opportunities**:
   - Display **profitable trading paths**.
   - Highlight the **smallest and greatest path weight factors** (degree of arbitrage potential).

## Example Output
```
Arbitrage opportunities found:
Path: btc -> xrp -> eth -> btc
Path weight: 1.0056789

Path: eth -> eos -> btc -> eth
Path weight: 1.0089123

Smallest path weight factor (closest to 1.0): 1.000345
Path: xrp -> eth -> xrp

Greatest path weight factor (furthest from 1.0): 1.012567
Path: bch -> btc -> xrp -> ltc -> eos -> eth
```

## Technologies Used
- **Python**: Main programming language.
- **NetworkX**: Graph creation and traversal.
- **Requests**: API calls to CoinGecko.

## Future Enhancements
- **Support for More Cryptocurrencies**: Expand analysis to additional coins.
- **Visualization Tools**: Graphically represent the exchange rate network.
- **Live Trading Implementation**: Integrate with real trading platforms.

---

_Developed as an exploration into graph traversal algorithms and arbitrage detection in cryptocurrency trading._

