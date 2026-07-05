# Feature Taxonomy for 《末日余生：极限生存》

Use this taxonomy when building the requirement inventory.

## Core modules

- Core loop: create/join match, prepare, survive, loot, build, fight, extract/end, settle.
- Player: movement, direction, animation state, stamina, interaction radius, death/revive.
- Map: 2D/俯视地图, camera, collision, walkable areas, points of interest, safe area/pressure if used.
- Zombies: spawn, pathfinding, chase, attack, damage, death, object pooling.
- Survival status: health, hunger, thirst, stamina, infection.
- Items: loot spawn, pickup, inventory, use, drop, stacking, item config.
- Craft/build: recipes, materials, placement preview, legal placement, durability, destroy/remove.
- Combat: melee/ranged, hit detection, cooldown, damage, feedback, weapon config.
- UI: title, loading, HUD, joystick/buttons, inventory, crafting, build panel, result screen, prompts.
- Network: room, matchmaking, authoritative state, snapshots, reconnect, settlement consistency.
- WeChat: login, lifecycle, safe area, touch, canvas/runtime bridge, resource loading, ads, share, ranking, privacy.
- Data/backend: user profile, match record, config version, leaderboard, event logs, anti-cheat signals.
- Non-functional: performance, memory, startup, package size, screen adaptation, weak network, security.

## Status values

- `planned`: requirement accepted but not built.
- `prototype`: explored in POC only.
- `implemented-master`: implemented in Game Studio/Phaser master.
- `implemented-wechat`: implemented in WeChat adaptation.
- `verified`: verified in browser and WeChat simulator/real device.
- `blocked`: cannot continue without a decision or dependency.
