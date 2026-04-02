---
estimated_steps: 9
estimated_files: 1
skills_used: []
---

# T05: Test liquidity context display with varied scenarios

1. Generate test events with varying liquidity:
   - High liquidity: tight spread (1%), high trade count (50+)
   - Medium liquidity: moderate spread (3%), medium trades (10)
   - Low liquidity: wide spread (8%), few trades (2)
   - No data: missing bid/ask fields
2. For each scenario, verify signal card shows correct liquidity metrics
3. Verify slippage estimates reasonable (higher for thin markets)
4. Verify 'N/A' handling when data missing
5. Document threshold for 'actionable' vs 'thin market' liquidity

## Inputs

- `app/liquidity.py`
- `app/templates/signal_card.html`

## Expected Output

- `integration_test_results.md`

## Verification

test -f integration_test_results.md && grep -q 'liquidity test' integration_test_results.md
