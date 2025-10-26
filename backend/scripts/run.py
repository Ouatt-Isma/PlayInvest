from recurring import assets, perf, challenge, challenge_seed, challenge_res, news, assets_first, log, get_db
from app.services.update_assets import update_assets_brvm
from app.services.weekly_notifs import send_weekly_notif_all_users



def test(db):
    send_weekly_notif_all_users(db)
# --- Manual runner ---
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Run maintenance tasks manually")
    parser.add_argument(
        "task",
        choices=["assets_first", "assets", "perf", "challenge", "news", "seed", "result", "assets_brvm", "test"],
        help="Which task to run"
    )
    args = parser.parse_args()

    if args.task == "assets_first":
        assets_first()
    if args.task == "assets_brvm":
        try:
            with get_db() as db:
                update_assets_brvm(db)
            log.info("Update BRVM() completed")
        except Exception as e:
            log.exception("Update BRVM() failed")
        
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
    elif args.task == "test":
        try:
            with get_db() as db:
                test(db)
            log.info("Test completed")
        except Exception as e:
            log.exception("Test() failed")

