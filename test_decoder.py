#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Uniswap V3 Transaction Decoder

This script tests the decoder with real Ethereum mainnet transaction hashes.
"""

import os
import sys
import json

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uniswap_v3_decoder import RPC, decode_uniswap_v3_swap

# Test cases with real Ethereum mainnet transaction hashes
TEST_CASES = [
    {
        "name": "Test Case 1: Simple USDT -> Token Swap (exactInputSingle)",
        "tx_hash": "0x7fdee03ffb227454946852b815b6b86d38e77e6190985c1816b41a8a7b790ea0",
        "expected": {
            "sender": "0x3b6ef09907a14361201876574b20AFD3bbbe83Ab",
            "recipient": "0x3b6ef09907a14361201876574b20AFD3bbbe83Ab",
            "tokenIn": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
            "tokenOut": "0xF5B5eFc906513b4344EbAbCF47A04901f99F09f3",  # UBX
            "amountIn": "2.32",
            "amountOut": "1892132"
        },
        "description": "Swap 2.32 USDT for 1,892,132 UBX on Uniswap V3"
    },
    {
        "name": "Test Case 2: USDT -> Token Swap (exactInputSingle)",
        "tx_hash": "0xe65ef1a33bee43ae6e79bb1ccee3c1ed8c523f00057b5494bbbaaf37d6c01647",
        "expected": {
            "sender": "0xcc347DC0076a380f5360bf6f78E47C981b4C7453",
            "recipient": "0xcc347DC0076a380f5360bf6f78E47C981b4C7453",
            "tokenIn": "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
            "tokenOut": "0x45e02bc2875A2914C4f585bBF92a6F28bc07CB70",  # $MBG
            "amountIn": "50",
            "amountOut": "146.252839837202059906"
        },
        "description": "Swap 50 USDT for 146.25 $MBG on Uniswap V3"
    },
    {
        "name": "Test Case 3: USDC -> Token Swap (exactOutputSingle)",
        "tx_hash": "0x028818d4e58333897c9f9498fdcab33d3f7d86334190854f39077a2052026204",
        "expected": {
            "sender": "0x83E9E6d3Ddb272B147ecC3F1D50323C4464d0708",
            "recipient": "0x83E9E6d3Ddb272B147ecC3F1D50323C4464d0708",
            "tokenIn": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",  # USDC
            "tokenOut": "0x8B1484d57abBE239bB280661377363b03c89CaEa",  # ADI
            "amountIn": "59.401751",
            "amountOut": "32.465005605931265505"
        },
        "description": "Swap 59.40 USDC for 32.47 ADI on Uniswap V3"
    },
    {
        "name": "Test Case 4: Token -> WETH Swap (exactInput)",
        "tx_hash": "0xa3e2249b644b3c8c0fc1bc3d78cc61c167db6175030ed04a23dea547667dddb7",
        "expected": {
            "sender": "0x3d102d44296AC2279fDa87BC2E3a7Dd043E60ac0",
            "recipient": "0x3d102d44296AC2279fDa87BC2E3a7Dd043E60ac0",
            "tokenIn": "0x6ad12E761b438beA3EA09F6C6266556Bb24C2181",  # BDX
            "tokenOut": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",  # WETH
            "amountIn": "369.796494252",
            "amountOut": "0.010391501642898139"
        },
        "description": "Swap 369.80 BDX for 0.0104 WETH on Uniswap V3"
    }
]


def run_tests(rpc_url: str):
    """Run all test cases and report results."""
    rpc = RPC(rpc_url)
    
    print("=" * 80)
    print("Uniswap V3 Transaction Decoder - Test Suite")
    print("=" * 80)
    print(f"RPC URL: {rpc_url}")
    print()
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n{'=' * 80}")
        print(f"Test {i}: {test['name']}")
        print(f"Description: {test['description']}")
        print(f"Transaction Hash: {test['tx_hash']}")
        print("-" * 80)
        
        try:
            result = decode_uniswap_v3_swap(rpc, test['tx_hash'])
            
            print("\nDecoded Result:")
            print(json.dumps(result, indent=2))
            
            # Verify results
            expected = test['expected']
            all_match = True
            
            print("\nVerification:")
            for key in expected:
                actual = result.get(key)
                exp = expected[key]
                match = actual == exp
                status = "✓" if match else "✗"
                print(f"  {status} {key}: {actual} {'==' if match else '!='} {exp}")
                if not match:
                    all_match = False
            
            if all_match:
                print("\n✓ TEST PASSED")
                passed += 1
            else:
                print("\n✗ TEST FAILED - Values don't match")
                failed += 1
                
        except Exception as e:
            print(f"\n✗ TEST FAILED - Error: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {len(TEST_CASES)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {passed / len(TEST_CASES) * 100:.1f}%")
    print("=" * 80)
    
    return failed == 0


def main():
    """Main entry point."""
    rpc_url = os.environ.get("RPC_URL", "").strip()
    
    if not rpc_url:
        print("Error: RPC_URL environment variable not set")
        print('Please set it to an Ethereum mainnet JSON-RPC endpoint.')
        print('\nExample: export RPC_URL="https://ethereum-rpc.publicnode.com"')
        sys.exit(1)
    
    success = run_tests(rpc_url)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
