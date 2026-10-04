def countingValleys(steps, path):
    over_mountain = False
    down = False
    valley = 0

    for pat in path:
        if pat == "U":
            down = True

        if down and over_mountain:
            valley += 1
            over_mountain = False

    return valley

if __name__ == "__main__":
    steps = 8
    path = "UDDDUDUU"

    result = countingValleys(steps, path)

    print(result)