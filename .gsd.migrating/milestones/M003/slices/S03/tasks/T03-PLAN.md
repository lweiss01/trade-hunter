---
estimated_steps: 8
estimated_files: 2
skills_used: []
---

# T03: Implement slippage estimation logic

1. Create app/liquidity.py with estimate_slippage(bid_price, ask_price, bid_size, ask_size, position_value)
2. For $100 position:
   - contracts_needed = position_value / avg_price
   - If buying (bid side): slippage = contracts_needed * (ask_price - mid_price)
   - If bid/ask size insufficient: increase slippage estimate (thin market penalty)
3. Return estimated slippage in dollars
4. Handle missing data: return None
5. Write unit tests with various liquidity scenarios

## Inputs

- None specified.

## Expected Output

- `app/liquidity.py`
- `tests/test_slippage.py`

## Verification

python -m pytest tests/test_slippage.py -v
