# Uniswap V3 Transaction Decoder

A Python script that decodes Uniswap V3 swap transactions on Ethereum Mainnet (L1) by directly interacting with the blockchain via standard JSON-RPC calls.
## Features

- **Direct Blockchain Interaction**: Uses standard JSON-RPC calls to Ethereum nodes (no third-party swap parsing APIs)
- **Comprehensive Decoding**: Supports `exactInputSingle`, `exactOutputSingle`, `exactInput`, `exactOutput`, and `multicall` transactions
- **Multi-hop Support**: Correctly handles multi-hop swaps through multiple pools
- **Human-readable Amounts**: Automatically converts raw token amounts using token decimals
- **Universal Router Support**: Handles both SwapRouter and Universal Router transactions
## Requirements

- Python 3.8+
- Dependencies: `requests`, `eth-abi`, `eth-utils`

## Usage

### Basic Usage

```bash
# Set the RPC URL environment variable
export RPC_URL="https://ethereum-rpc.publicnode.com"

# Decode a transaction
python uniswap_v3_decoder.py <transaction_hash>
```

### Example

```bash
export RPC_URL="https://ethereum-rpc.publicnode.com"
python uniswap_v3_decoder.py 0x7fdee03ffb227454946852b815b6b86d38e77e6190985c1816b41a8a7b790ea0
python uniswap_v3_decoder.py 0xe65ef1a33bee43ae6e79bb1ccee3c1ed8c523f00057b5494bbbaaf37d6c01647
python uniswap_v3_decoder.py 0x028818d4e58333897c9f9498fdcab33d3f7d86334190854f39077a2052026204
python uniswap_v3_decoder.py 0xa3e2249b644b3c8c0fc1bc3d78cc61c167db6175030ed04a23dea547667dddb7
```

### Output

```json
{
  "sender": "0x3b6ef09907a14361201876574b20AFD3bbbe83Ab",
  "recipient": "0x3b6ef09907a14361201876574b20AFD3bbbe83Ab",
  "tokenIn": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
  "tokenOut": "0xF5B5eFc906513b4344EbAbCF47A04901f99F09f3",
  "amountIn": "2.32",
  "amountOut": "1892132"
}
```

### Advanced Usage

Include all swap candidates for debugging:

```bash
python uniswap_v3_decoder.py <transaction_hash> --all
```

## Output Fields

| Field | Description |
|-------|-------------|
| `sender` | The address that initiated the swap |
| `recipient` | The address that received the output tokens |
| `tokenIn` | The contract address of the input token |
| `tokenOut` | The contract address of the output token |
| `amountIn` | The human-readable amount of input tokens (adjusted for decimals) |
| `amountOut` | The human-readable amount of output tokens (adjusted for decimals) |

## Test Cases

The script has been tested with the following real Ethereum mainnet transactions:

### Test Case 1: Simple USDT → Token Swap
- **Transaction**: [0x7fdee03ffb227454946852b815b6b86d38e77e6190985c1816b41a8a7b790ea0](https://etherscan.io/tx/0x7fdee03ffb227454946852b815b6b86d38e77e6190985c1816b41a8a7b790ea0)
- **Description**: Swap 2.32 USDT for 1,892,132 UBX
- **Method**: `exactInputSingle`

### Test Case 2: USDT → Token Swap
- **Transaction**: [0xe65ef1a33bee43ae6e79bb1ccee3c1ed8c523f00057b5494bbbaaf37d6c01647](https://etherscan.io/tx/0xe65ef1a33bee43ae6e79bb1ccee3c1ed8c523f00057b5494bbbaaf37d6c01647)
- **Description**: Swap 50 USDT for 146.25 $MBG
- **Method**: `exactInputSingle`

### Test Case 3: USDC → Token Swap (Exact Output)
- **Transaction**: [0x028818d4e58333897c9f9498fdcab33d3f7d86334190854f39077a2052026204](https://etherscan.io/tx/0x028818d4e58333897c9f9498fdcab33d3f7d86334190854f39077a2052026204)
- **Description**: Swap 59.40 USDC for 32.47 ADI
- **Method**: `exactOutputSingle`

### Test Case 4: Token → WETH Swap
- **Transaction**: [0xa3e2249b644b3c8c0fc1bc3d78cc61c167db6175030ed04a23dea547667dddb7](https://etherscan.io/tx/0xa3e2249b644b3c8c0fc1bc3d78cc61c167db6175030ed04a23dea547667dddb7)
- **Description**: Swap 369.80 BDX for 0.0104 WETH
- **Method**: `exactInput`

## Running Tests

### macOS / Linux (bash/zsh)
```bash
export RPC_URL="https://ethereum-rpc.publicnode.com"
python test_decoder.py
```
### Windows PowerShell (run these lines in PowerShell, not bash)
```bash
$env:RPC_URL="https://ethereum-rpc.publicnode.com"
python test_decoder.py
```


Expected output:
```
================================================================================
TEST SUMMARY
================================================================================
Total Tests: 4
Passed: 4
Failed: 0
Success Rate: 100.0%
================================================================================
```

## How It Works

1. **Fetch Transaction Data**: Uses `eth_getTransactionByHash` and `eth_getTransactionReceipt` RPC calls
2. **Decode Input Data**: Parses the transaction input to identify the swap method and parameters
3. **Extract Swap Events**: Finds Uniswap V3 `Swap` events in the transaction logs
4. **Match Intents to Events**: Correlates decoded swap intents with actual swap events
5. **Resolve Token Details**: Queries token contracts for decimals using `eth_call`
6. **Format Output**: Converts raw amounts to human-readable format

## Supported Routers

- SwapRouter (0xE592427A0AEce92De3Edee1F18E0157C05861564)
- SwapRouter02 (0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45)
- Universal Router (0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B)
- Universal Router V2 (0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD)

## Public RPC Endpoints

You can use any Ethereum mainnet JSON-RPC endpoint. Some free options:

- `https://ethereum-rpc.publicnode.com`
- `https://eth.llamarpc.com`
- `https://rpc.ankr.com/eth`
- `https://cloudflare-eth.com`
