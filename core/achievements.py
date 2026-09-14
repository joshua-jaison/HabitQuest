def _safe_value(stats, key, default=0):
    return stats.get(key, default) if isinstance(stats, dict) else default


ACHIEVEMENTS = [
    {
        "name": "First Step",
        "description": "Complete your first habit.",
        "condition": lambda stats: _safe_value(stats, "completed", 0) >= 1
    },
    {
        "name": "Fire Starter",
        "description": "Reach a 3-day streak.",
        "condition": lambda stats: _safe_value(stats, "best_streak", 0) >= 3
    },
    {
        "name": "Warrior",
        "description": "Reach a 7-day streak.",
        "condition": lambda stats: _safe_value(stats, "best_streak", 0) >= 7
    },
    {
        "name": "XP Hunter",
        "description": "Earn 1,000 XP.",
        "condition": lambda stats: _safe_value(stats, "xp", 0) >= 1000
    },
    {
        "name": "Diamond",
        "description": "Reach a 30-day streak.",
        "condition": lambda stats: _safe_value(stats, "best_streak", 0) >= 30
    },
    {
        "name": "Level Master",
        "description": "Reach Level 10.",
        "condition": lambda stats: _safe_value(stats, "level", 0) >= 10
    }
]


def get_unlocked_achievements(stats):
    unlocked = []

    for achievement in ACHIEVEMENTS:
        try:
            if achievement["condition"](stats):
                unlocked.append(achievement)
        except Exception:
            continue

    return unlocked
