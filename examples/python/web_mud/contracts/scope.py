# ======================================================= #
# SCOPE
# ======================================================= #

SCOPES = {
    "room":
        lambda player, other_player:
        player.avatar.position == other_player.avatar.position,

    "world":
        lambda player, other_player: True
}
