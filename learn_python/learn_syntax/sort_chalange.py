from sort_syntax import leaderboards

def natural_keys(s) -> list:
    return [leaderboards[s]['score'], -leaderboards[s]['time']]

sorted_lb = sorted(
    leaderboards,
    key=natural_keys,
    reverse=True
)

## Or
# sorted_lb = sorted(
#     leaderboards,
#     key=lambda x: (leaderboards[x]['score'], -leaderboards[x]['time']),
#     reverse=True
# )

print(sorted_lb[:3])