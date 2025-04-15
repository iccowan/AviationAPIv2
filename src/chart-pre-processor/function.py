# 1. Pull current and next airacs from DynamoDB for both charts and chart supplement
#   - If none are available, generate current and next
#   - If next should be current, replace current with next and generate new next
# 2. Check the status for next airac
#   - If the status for any packets is not ready, trigger for update
#   - Will only trigger within 14 days of airac cycle beginning
#   - Will handle charts and chart supplement separately (follow the appropriate cycles)
#   - 250417 cycle has both charts and chart supplement as a starting point
# 3. Send out triggers as appropriate
