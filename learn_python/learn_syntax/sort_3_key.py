leaderboards = {
    "ridwan kebab":    {"score": 90, "time": 180},
    "fajar racing":    {"score": 90, "time": 180},
    "crazy killer":    {"score": 87, "time": 231},
    "abbas kehidupan": {"score": 42, "time": 231},
    "rahmat toilet":   {"score": 82, "time": 231},
    "andi speaker":    {"score": 90, "time": 180},
}

sorted_lb = sorted(
    leaderboards,
    key=lambda x: (-leaderboards[x]['score'], leaderboards[x]['time'], x)
)

print(sorted_lb[:3])