import networkx as nx
import requests

# Define the coin IDs and ticker symbols
coin_ids = ['ripple', 'cardano', 'bitcoin-cash', 'eos', 'litecoin', 'ethereum', 'bitcoin']
coin_tickers = ['xrp', 'ada', 'bch', 'eos', 'ltc', 'eth', 'btc']

# Create a directed graph
g = nx.DiGraph()

# Function to get exchange rates from CoinGecko API
def get_exchange_rates():
    """
    Fetch the latest exchange rates from the CoinGecko API and add the corresponding edges to the graph.
    """
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': ','.join(coin_ids),
        'vs_currencies': ','.join(coin_tickers)
    }
    try:
        response = requests.get(url, params=params).json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange rates: {e}")
        return

    for coin_id, ticker in zip(coin_ids, coin_tickers):
        for vs_currency, rate in response[coin_id].items():
            g.add_weighted_edges_from([(ticker, vs_currency, rate), (vs_currency, ticker, 1 / rate)])

# Function to find arbitrage opportunities
def find_arbitrage_opportunities():
    """
    Find arbitrage opportunities by finding cycles in the graph with a product of weights deviating significantly from 1.0.
    """
    arbitrage_opportunities = []
    for cycle in nx.simple_cycles(g):
        if len(cycle) > 2:  # Ignore self-loops
            cycle_weight = 1
            for i in range(len(cycle)):
                node1 = cycle[i]
                node2 = cycle[(i + 1) % len(cycle)]
                cycle_weight *= g[node1][node2]['weight']
            if abs(cycle_weight - 1) > 0.001:  # Threshold for significant deviation
                arbitrage_opportunities.append((cycle, cycle_weight))
    return arbitrage_opportunities

# Get the latest exchange rates
get_exchange_rates()

# Find arbitrage opportunities
arbitrage_opportunities = find_arbitrage_opportunities()

# Output the arbitrage opportunities
if not arbitrage_opportunities:
    print("No arbitrage opportunities found.")
else:
    print("Arbitrage opportunities found:")
    for cycle, cycle_weight in arbitrage_opportunities:
        cycle_str = ' -> '.join(cycle)
        print(f"Path: {cycle_str}")
        print(f"Path weight: {cycle_weight}")
        print()

    # Find the smallest and greatest path weight factors
    path_weight_factors = [cycle_weight for _, cycle_weight in arbitrage_opportunities]
    smallest_factor = min(path_weight_factors, key=lambda x: abs(x - 1) if x != 1 else float('inf'))
    greatest_factor = max(path_weight_factors, key=lambda x: abs(x - 1))

    print(f"Smallest path weight factor (closest to 1.0): {smallest_factor}")
    print("Smallest paths:")
    for cycle, cycle_weight in arbitrage_opportunities:
        if cycle_weight == smallest_factor:
            cycle_str = ' -> '.join(cycle)
            print(f"Path: {cycle_str}")
    print()

    print(f"Greatest path weight factor (furthest from 1.0): {greatest_factor}")
    print("Greatest paths:")
    for cycle, cycle_weight in arbitrage_opportunities:
        if cycle_weight == greatest_factor:
            cycle_str = ' -> '.join(cycle)
            print(f"Path: {cycle_str}")