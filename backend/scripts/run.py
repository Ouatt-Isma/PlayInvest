from recurring import assets, perf, challenge, challenge_seed, challenge_res, news, assets_first

# --- Manual runner ---
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Run maintenance tasks manually")
    parser.add_argument(
        "task",
        choices=["assets_first", "assets", "perf", "challenge", "news", "seed", "result"],
        help="Which task to run"
    )
    args = parser.parse_args()

    if args.task == "assets_first":
        assets_first()
    if args.task == "assets":
        assets()
    elif args.task == "perf":
        perf()
    elif args.task == "challenge":
        challenge(False)
    elif args.task == "result":
        challenge_res(False)
    elif args.task == "seed":
        challenge_seed(False)
    elif args.task == "news":
        news()
