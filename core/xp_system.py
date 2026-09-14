def calculate_level(total_xp):
    xp = int(total_xp)
    if xp < 0:
        xp = 0
    return (xp // 500) + 1


def xp_for_current_level(total_xp):
    xp = max(0, int(total_xp))
    level = calculate_level(xp)

    previous_level_xp = (level - 1) * 500
    current_level_xp = level * 500

    progress = xp - previous_level_xp
    required = current_level_xp - previous_level_xp

    return progress, required


def get_xp_bonus(streak):
    streak = max(0, int(streak))

    if streak >= 30:
        return 1.50

    if streak >= 14:
        return 1.30

    if streak >= 7:
        return 1.20

    if streak >= 4:
        return 1.10

    return 1.0


def calculate_reward(base_xp, streak):
    base = max(0, int(base_xp))
    multiplier = get_xp_bonus(streak)
    return int(base * multiplier)
