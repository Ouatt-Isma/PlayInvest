# app/services/challenges_scheduler.py

from typing import Dict, Optional, List, Tuple, Set
from datetime import datetime, timedelta, timezone, time
import random

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.models.asset import Asset
from app.db.models.weekly_challenge import (
    WeeklyChallenge,
    WeeklyChallengeSide,
    EntityKind,
)
from app.core.config import settings 
TZ_FR = settings.TZ_FR

# -----------------------------------------------------------------------------
# 1) Templates: each side is a small filter dict: keys can be 'type' and/or 'region'
#    We’ll materialize these to real ASSETs when creating the challenge.
# -----------------------------------------------------------------------------
COMBO_TEMPLATES: List[Tuple[Dict[str, str], Dict[str, str]]] = [
    # Same type, different regions
    ({"type": "Action", "region": "Europe"},  {"type": "Action", "region": "Afrique"}),
    ({"type": "Action", "region": "USA"},     {"type": "Action", "region": "Europe"}),
    ({"type": "Action", "region": "Afrique"}, {"type": "Action", "region": "Europe"}),

    ({"type": "ETF",    "region": "Europe"},  {"type": "ETF",    "region": "USA"}),
    ({"type": "ETF",    "region": "Afrique"}, {"type": "ETF",    "region": "Europe"}),

    # Cross-type, same region
    ({"type": "ETF",    "region": "Europe"},  {"type": "Action", "region": "Europe"}),
    ({"type": "ETF",    "region": "USA"},     {"type": "Action", "region": "USA"}),
    ({"type": "ETF",    "region": "Afrique"}, {"type": "Action", "region": "Afrique"}),

    # Cross-type, cross-region
    ({"type": "Crypto"},                      {"type": "Action", "region": "USA"}),
    ({"type": "Crypto"},                      {"type": "Action", "region": "Europe"}),
    ({"type": "Crypto"},                      {"type": "ETF",    "region": "USA"}),

    # Pure random within a type
    ({"type": "Action"},                      {"type": "Action"}),
    ({"type": "ETF"},                         {"type": "ETF"}),
    ({"type": "Crypto"},                      {"type": "Crypto"}),

    # Totally open (acts like a built-in fallback)
    ({},                                      {}),
]

# -----------------------------------------------------------------------------
# 2) Labels & descriptions (FR)
# -----------------------------------------------------------------------------
TYPE_LABEL = {
    "Action": "actions",
    "ETF": "ETF",
    "Crypto": "crypto",
}
REGION_LABEL = {
    "Europe": "Europe",
    "USA": "USA",
    "Afrique": "Afrique",
    "World": "Monde",
}

def _label_from_filter(f: Dict[str, str]) -> str:
    """Construit un libellé FR à partir d'un filtre (type/region)."""
    t = f.get("type")
    r = f.get("region")
    if t and r:
        return f"{TYPE_LABEL.get(t, t)} {REGION_LABEL.get(r, r)}"
    if t:
        return TYPE_LABEL.get(t, t)
    if r:
        return f"marchés {REGION_LABEL.get(r, r)}"
    return "actifs au hasard"

def _description_for_filters(left_filter: Dict[str, str], right_filter: Dict[str, str]) -> str:
    L = _label_from_filter(left_filter)
    R = _label_from_filter(right_filter)
    return f"Qui va mieux performer cette semaine : {L} ou {R} ? Faites votre choix !"

def _description_generic(a_name: str, b_name: str) -> str:
    return f"Qui va mieux performer cette semaine : {a_name} ou {b_name} ? À vous de jouer !"

# -----------------------------------------------------------------------------
# 3) Time window helpers (UTC)
# -----------------------------------------------------------------------------
def _next_week_window_utc(now: Optional[datetime] = None) -> Tuple[datetime, datetime]:
    """
    Next week window in UTC:
      Monday 00:00:00 → Sunday 23:59:59.999999
    """
    now = now or datetime.now(timezone.utc)
    weekday = now.date().weekday()  # Monday=0
    days_until_next_monday = (7 - weekday) % 7 or 7
    start = datetime.combine(now.date() + timedelta(days=days_until_next_monday), time(0, 0), tzinfo=timezone.utc)
    end = start + timedelta(days=7) - timedelta(microseconds=1)
    return start, end

def _next_weekend_window_fr(
    now: Optional[datetime] = None,
    return_utc: bool = False
) -> Tuple[datetime, datetime]:
    """
    Next weekend window in France time (Europe/Paris):
      Start: Saturday 00:00
      End:   Sunday 23:59:59.999999
    Returns datetimes either in Europe/Paris or converted to UTC if return_utc=True.
    """
    # Get 'now' in Europe/Paris
    if now is None:
        local_now = datetime.now(TZ_FR)
    else:
        local_now = now.astimezone(TZ_FR) if now.tzinfo else now.replace(tzinfo=TZ_FR)

    # Monday=0 ... Saturday=5, Sunday=6
    weekday = local_now.date().weekday()
    days_until_saturday = (5 - weekday) % 7 or 7  # next Saturday, not "today" if it's already Saturday

    # Start: Saturday 00:00 (local France time)
    start_local = datetime.combine(
        local_now.date() + timedelta(days=days_until_saturday),
        time(0, 0, 0, 0),
        tzinfo=TZ_FR,
    )

    # End: Sunday 23:59:59.999999 (local France time)
    end_local = datetime.combine(
        start_local.date() + timedelta(days=1),
        time(23, 59, 59, 999_999),
        tzinfo=TZ_FR,
    )

    if return_utc:
        return start_local.astimezone(timezone.utc), end_local.astimezone(timezone.utc)
    return start_local, end_local

# -----------------------------------------------------------------------------
# 4) Asset picking helpers
# -----------------------------------------------------------------------------
def _pick_random_asset(
    db: Session,
    type_: Optional[str] = None,
    region: Optional[str] = None,
    exclude_ids: Optional[Set[int]] = None,
) -> Optional[Asset]:
    q = db.query(Asset)
    if type_:
        q = q.filter(Asset.type == type_)
    if region:
        q = q.filter(Asset.region == region)
    if exclude_ids:
        q = q.filter(~Asset.id.in_(exclude_ids))
    return q.order_by(func.random()).first()

def _pick_two_any_assets(db: Session, exclude_ids: Optional[Set[int]] = None) -> Optional[Tuple[Asset, Asset]]:
    q = db.query(Asset)
    if exclude_ids:
        q = q.filter(~Asset.id.in_(exclude_ids))
    rows = q.order_by(func.random()).limit(2).all()
    if len(rows) < 2:
        return None
    return rows[0], rows[1]

def _materialize_two_assets(
    db: Session,
    left_filter: Dict[str, str],
    right_filter: Dict[str, str],
) -> Optional[Tuple[Asset, Asset]]:
    left = _pick_random_asset(db, type_=left_filter.get("type"), region=left_filter.get("region"))
    if not left:
        return None
    right = _pick_random_asset(
        db,
        type_=right_filter.get("type"),
        region=right_filter.get("region"),
        exclude_ids={left.id},
    )
    if not right:
        return None
    return left, right

def _choose_assets_or_fallback(db: Session) -> Tuple[Tuple[Asset, Asset], Optional[Dict[str, str]], Optional[Dict[str, str]]]:
    """
    Try all templates in random order; if none fits, fallback to any two assets.
    Returns: ((assetA, assetB), left_filter_or_None, right_filter_or_None)
    """
    templates = COMBO_TEMPLATES[:]
    random.shuffle(templates)
    for lf, rf in templates:
        picked = _materialize_two_assets(db, lf, rf)
        if picked:
            return picked, lf, rf
    picked = _pick_two_any_assets(db)
    if not picked:
        raise RuntimeError("Aucun couple d'actifs disponible (base insuffisante).")
    return picked, None, None  # fallback (no filters)

# -----------------------------------------------------------------------------
# 5) Public API
# -----------------------------------------------------------------------------
def create_challenge_for_next_week(db: Session, check=True) -> WeeklyChallenge:
    """
    Pick a random template, draw two concrete assets matching the filters
    (or fallback to any two assets), and create a challenge for the NEXT week.
    """
    start_at, end_at = _next_weekend_window_fr()
    now_fr = datetime.now(TZ_FR)
    tomorrow = (now_fr + timedelta(days=1)).date()

    if(check):
        assert start_at.date() == tomorrow, f"Expected {tomorrow}, got {start_at.date()}"


    # Avoid duplicates for that exact window
    existing = (
        db.query(WeeklyChallenge)
        .filter(WeeklyChallenge.start_at == start_at, WeeklyChallenge.end_at == end_at)
        .first()
    )
    if existing:
        return existing

    (left_asset, right_asset), lf, rf = _choose_assets_or_fallback(db)

    # Description
    if lf is not None and rf is not None:
        desc = _description_for_filters(lf, rf)
    else:
        desc = _description_generic(left_asset.name or left_asset.symbol,
                                    right_asset.name or right_asset.symbol)

    # Create the challenge (keep is_active=False until the week starts)
    challenge = WeeklyChallenge(
        start_at=start_at,
        end_at=end_at,
        is_active=True,
        description=desc,
    )
    db.add(challenge)
    db.flush()  # to get challenge.id

    # Two ASSET sides
    side_a = WeeklyChallengeSide(
        challenge_id=challenge.id,
        side='A',
        entity_kind=EntityKind.ASSET,
        asset_id=left_asset.id,
    )
    side_b = WeeklyChallengeSide(
        challenge_id=challenge.id,
        side='B',
        entity_kind=EntityKind.ASSET,
        asset_id=right_asset.id,
    )
    db.add_all([side_a, side_b])
    db.commit()

    return challenge

def seed_many_weeks_ahead(db: Session, weeks: int = 4) -> List[WeeklyChallenge]:
    """
    Create challenges for the next N weeks (if missing),
    each time picking a template (or falling back) and saving a FR description.
    """
    created: List[WeeklyChallenge] = []
    base_start, base_end = _next_week_window_utc()

    for i in range(weeks):
        s = base_start + timedelta(days=7 * i)
        e = base_end + timedelta(days=7 * i)

        exists = (
            db.query(WeeklyChallenge)
            .filter(WeeklyChallenge.start_at == s, WeeklyChallenge.end_at == e)
            .first()
        )
        if exists:
            continue

        (a, b), lf, rf = _choose_assets_or_fallback(db)

        if lf is not None and rf is not None:
            desc = _description_for_filters(lf, rf)
        else:
            desc = _description_generic(a.name or a.symbol, b.name or b.symbol)

        ch = WeeklyChallenge(start_at=s, end_at=e, is_active=False, description=desc)
        db.add(ch)
        db.flush()

        db.add_all([
            WeeklyChallengeSide(challenge_id=ch.id, side='A', entity_kind=EntityKind.ASSET, asset_id=a.id),
            WeeklyChallengeSide(challenge_id=ch.id, side='B', entity_kind=EntityKind.ASSET, asset_id=b.id),
        ])
        db.commit()
        created.append(ch)

    return created


def seed_next_week(db, check=True):
    ch = create_challenge_for_next_week(db, check)
    return {"ok": True, "challengeId": ch.id, "startAt": ch.start_at, "endAt": ch.end_at}
