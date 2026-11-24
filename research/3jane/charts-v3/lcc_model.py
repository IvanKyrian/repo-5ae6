"""LCC return per $1M commitment: income / time-weighted capital deployed, annualized.
Margin (7.5%) is deployed until the call; the full $1M (USD3) after it."""
P, MARGIN, TERM = 1_000_000, 0.075, 90
def run(deal, call_day, H=180, usd3=0.0694, aave=0.04):
    hard = jane = capdays = 0.0
    for d in range(H):
        called = call_day is not None and d >= call_day
        if not called:
            cap = P * MARGIN
            if deal == 'private' and d < TERM:
                hard += cap * (aave + 0.12) / 365; jane += cap * 0.18 / 365
            else:
                hard += cap * (aave + 0.0125 / MARGIN) / 365
        else:
            cap = P; k = d - call_day
            if deal == 'private' and call_day < TERM and k < 70:
                hard += cap * usd3 / 365; jane += cap * (0.18 - usd3) / 365
            else:
                bonus = 0.0075 if (deal == 'public' or call_day >= TERM) and k < 35 else 0
                hard += cap * (usd3 + bonus) / 365
        capdays += cap
    apr = (hard + jane) / capdays * 365
    return apr, jane / (hard + jane), hard + jane
if __name__ == '__main__':
    for deal in ('public', 'private'):
        for c in (0, 30, 60, 90, 150, None):
            apr, js, inc = run(deal, c)
            print(deal, 'call day', c, 'APR %.1f%%' % (apr*100), 'JANE share %.0f%%' % (js*100), 'income $%.1fk' % (inc/1e3))
