---
estimated_steps: 9
estimated_files: 1
skills_used: []
---

# T05: Test dashboard navigation and user workflow

1. Start app, navigate to each view
2. Live spike board: verify 20 recent signals, tier colors correct, auto-refresh works
3. Click signal - verify card opens with full context
4. Click market title - verify market detail view shows full timeline
5. Alert history: test each filter (tier, topic, platform), verify results match
6. Test pagination: navigate pages, verify results correct
7. Test navigation: switch between views, verify no lost context
8. Time user workflow: find specific signal in history (<10 seconds target)
9. Document any UX issues

## Inputs

- `app/templates/`

## Expected Output

- `integration_test_results.md`

## Verification

test -f integration_test_results.md && grep -q 'navigation test' integration_test_results.md
