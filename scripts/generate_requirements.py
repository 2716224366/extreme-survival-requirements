#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate functional requirements docs for 《末日余生：极限生存》.

The output intentionally excludes schedules, dates, staffing plans, launch
forecasts, and budget estimates. It focuses on product and implementation
requirements that help a future Codex session continue the project.
"""

from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_NAME = "《末日余生：极限生存》"


FEATURES = [
    {
        "id": "ES-FR-CORE-001",
        "module": "核心循环",
        "feature": "单局生存流程",
        "priority": "Must",
        "purpose": "定义玩家进入一局游戏后的完整体验闭环：进入地图、探索、搜刮、维持生存、遭遇僵尸、建造防御、结束并结算。",
        "behavior": "玩家从开始界面进入游戏，在地图中自由移动，寻找物资，处理饥饿、口渴、体力、感染和生命威胁，并在死亡或达成结束条件后进入结算。",
        "rules": [
            "一局游戏必须有明确开始、进行中、暂停/前后台、结束、结算五类状态。",
            "游戏结束原因至少包括玩家死亡、主动结束、时间/目标结束三类；具体启用哪些由配置决定。",
            "任何结算数据必须来自可信逻辑；微信版涉及榜单或奖励时不能只相信客户端本地结果。",
            "广告复活若启用，必须标记为辅助局或独立榜规则，不能污染纯净成绩。",
        ],
        "state": ["matchState", "elapsedTime", "endReason", "isAssistedRun", "score", "survivalStats", "configVersion"],
        "inputs": ["开始游戏", "暂停/恢复", "玩家死亡事件", "目标完成事件", "广告复活回调", "前后台生命周期"],
        "outputs": ["HUD 状态变化", "结束提示", "结算面板", "本局摘要", "可选排行榜/奖励写入请求"],
        "shared": "状态机、结算规则、辅助局标记、分数计算和配置读取应保持平台无关。",
        "master": "浏览器母版必须能完整跑通单局流程，并暴露调试信息帮助验证状态切换。",
        "wechat": "微信版必须处理前后台切换、音频/计时恢复、广告回调失败、网络失败和安全区展示。",
        "acceptance": [
            "从开始界面进入地图后，玩家可以完成至少一条可重复的生存流程。",
            "死亡或结束后进入结算界面，结算原因和核心数据可读。",
            "前后台切换后，游戏不会卡死、黑屏或重复结算。",
        ],
        "tests": ["状态机单元测试", "浏览器完整流程试玩", "微信模拟器前后台切换", "真机结束/结算验证"],
        "open": ["是否需要明确撤离点/救援目标，还是首版只按生存时长和死亡结算。"],
        "reader": {
            "what": "玩家进入一局末日生存游戏，在危险地图里努力活下去。",
            "show": "游戏显示地图、角色、状态、物资、僵尸、提示和结算结果。",
            "success": "玩家能完成一局，并看懂自己为什么结束、获得了什么结果。",
            "failure": "死亡、主动退出、网络或广告异常时要有清楚提示，不能让玩家不知道发生了什么。",
            "excluded": "暂不承诺复杂剧情关卡、多地图战役或大型开放世界。",
            "confirm": "需要确认一局结束的主要目标：只看生存时长，还是加入撤离/任务目标。",
        },
    },
    {
        "id": "ES-FR-PLAYER-001",
        "module": "玩家",
        "feature": "360° 移动、朝向与基础动画",
        "priority": "Must",
        "purpose": "保证玩家角色在 2D 地图上移动顺手，方向反馈清晰，是后续战斗、搜刮和建造的基础。",
        "behavior": "玩家可通过键盘、鼠标或触摸摇杆控制角色向任意方向移动；角色朝向跟随移动方向或瞄准方向。",
        "rules": [
            "移动输入应归一化，斜向移动不能比横向/纵向更快。",
            "角色不能穿过障碍物、地图边界或不可行走区域。",
            "移动速度、转向速度、碰撞半径和动画状态必须由配置控制。",
            "无输入时角色进入 idle 状态；有输入时进入 walk/run 状态。",
        ],
        "state": ["position", "velocity", "facingAngle", "moveSpeed", "collisionRadius", "animationState"],
        "inputs": ["键盘 WASD/方向键", "鼠标/指针", "触摸摇杆", "虚拟按键", "配置表"],
        "outputs": ["角色位置", "角色朝向", "动画状态", "相机跟随目标", "移动调试信息"],
        "shared": "输入向量到移动意图、碰撞查询和角色状态更新应平台无关。",
        "master": "浏览器母版必须同时支持键盘和鼠标/触摸模拟，方便桌面调试。",
        "wechat": "微信版必须使用触摸摇杆/按钮，适配不同屏幕比例和安全区，避免触摸事件丢失。",
        "acceptance": [
            "玩家能前后左右和斜向移动，速度一致且没有抖动。",
            "角色碰到障碍物会被阻挡，不会穿墙。",
            "微信模拟器和至少一台真机上触摸移动可用。",
        ],
        "tests": ["输入归一化测试", "障碍碰撞测试", "浏览器键鼠试玩", "微信触摸试玩"],
        "open": ["是否需要冲刺按钮，以及冲刺是否消耗体力。"],
        "reader": {
            "what": "玩家可以像操控摇杆游戏一样控制小人在地图上移动。",
            "show": "角色会朝移动方向转身，并用走路/站立等表现反馈当前状态。",
            "success": "移动顺滑、方向准确，不会莫名卡住或穿过障碍物。",
            "failure": "如果碰到墙、树、建筑等障碍，角色应该被挡住，而不是穿过去。",
            "excluded": "暂不包含攀爬、载具、复杂翻越或物理推挤。",
            "confirm": "需要确认是否做冲刺，以及冲刺是否消耗体力。",
        },
    },
    {
        "id": "ES-FR-PLAYER-002",
        "module": "玩家",
        "feature": "死亡、倒地与复活规则",
        "priority": "Must",
        "purpose": "定义玩家失败、死亡反馈、是否复活，以及广告复活如何不破坏公平。",
        "behavior": "玩家生命降为 0 后进入死亡或倒地状态；如果允许复活，系统展示复活入口；否则进入结算。",
        "rules": [
            "生命值不能低于 0；死亡状态不能继续移动、攻击、拾取或建造。",
            "复活必须恢复到可配置生命值，并可设置短暂无敌或出生安全检查。",
            "广告复活必须记录为 assisted revive；对应对局不得进入纯净竞技榜。",
            "联机版本中死亡和复活结果必须由服务端或可信逻辑确认。",
        ],
        "state": ["hp", "isDead", "isDowned", "reviveCount", "reviveSource", "invulnerableUntil", "assistedRunFlag"],
        "inputs": ["受到伤害", "广告完成", "复活按钮", "结算按钮", "服务端确认"],
        "outputs": ["死亡动画/提示", "复活按钮", "结算触发", "辅助局标记", "复活事件"],
        "shared": "死亡条件、复活限制、辅助局标记和结算影响应平台无关。",
        "master": "母版可用调试按钮模拟死亡/复活，方便验证状态机。",
        "wechat": "微信版复活入口若接广告，必须处理广告加载失败、关闭未看完、回调延迟和重复点击。",
        "acceptance": [
            "生命降为 0 后不能继续正常操作。",
            "复活后角色恢复可控，且不会重复触发多次复活。",
            "广告复活失败时有明确提示，并能回到结算或重试路径。",
        ],
        "tests": ["伤害致死测试", "重复复活点击测试", "广告失败回调测试", "辅助局结算测试"],
        "open": ["首版是否启用广告复活，还是先只做普通重开。"],
        "reader": {
            "what": "玩家被僵尸击败或状态耗尽后会死亡，可以根据规则重开或复活。",
            "show": "游戏会显示死亡提示、复活入口或结算结果。",
            "success": "玩家能明确知道自己死因，并能选择重开或符合规则地复活。",
            "failure": "广告没看完、加载失败或复活次数用完时，需要给出清楚提示。",
            "excluded": "暂不包含复杂队友救援、尸体背包掉落等高级规则。",
            "confirm": "需要确认广告复活是否进入首版，以及是否影响排行榜。",
        },
    },
    {
        "id": "ES-FR-MAP-001",
        "module": "地图",
        "feature": "2D 俯视地图、碰撞与兴趣点",
        "priority": "Must",
        "purpose": "提供可探索、可碰撞、可放置物资和僵尸的基础地图环境。",
        "behavior": "地图包含道路、草地、建筑/障碍、可交互点、物资点和僵尸刷新点；玩家在可行走区域移动。",
        "rules": [
            "地图必须区分可行走区域和不可行走区域。",
            "兴趣点需要可配置，便于后续增加房屋、补给点或危险区。",
            "相机应跟随玩家，同时保留 HUD 和触摸控件可用空间。",
            "资源尺寸和对象数量必须适合微信小游戏首包/分包策略。",
        ],
        "state": ["mapId", "walkableLayer", "collisionLayer", "poiList", "spawnPoints", "cameraBounds"],
        "inputs": ["地图配置", "碰撞查询", "玩家位置", "屏幕尺寸", "资源加载结果"],
        "outputs": ["地图渲染", "碰撞结果", "相机位置", "兴趣点交互范围"],
        "shared": "地图配置、碰撞语义、兴趣点定义应平台无关。",
        "master": "母版可使用调试网格和碰撞显示，帮助快速调整地图。",
        "wechat": "微信版必须处理横竖屏选择、刘海/安全区、不同宽高比下的相机显示。",
        "acceptance": [
            "玩家在地图上可移动，边界和障碍有效。",
            "至少存在多个兴趣点/物资点/僵尸点。",
            "不同模拟机尺寸下画面铺满屏幕且不遮挡关键操作。",
        ],
        "tests": ["碰撞层检查", "相机边界测试", "多屏幕比例截图", "资源加载失败回退"],
        "open": ["地图最终是横屏还是竖屏；当前 POC 已验证横屏更适合移动空间。"],
        "reader": {
            "what": "玩家会在一张末日小镇/野外地图上探索。",
            "show": "画面中有道路、障碍、树木、建筑区域、物资点和危险区域。",
            "success": "玩家能看清自己在哪里，也能理解哪里能走、哪里不能走。",
            "failure": "如果地图资源加载失败，要能提示或回退，而不是黑屏。",
            "excluded": "暂不包含多地图、无缝大世界或所有建筑室内可进入。",
            "confirm": "需要确认游戏采用横屏还是竖屏作为正式方向。",
        },
    },
    {
        "id": "ES-FR-ZOMBIE-001",
        "module": "僵尸",
        "feature": "生成、追击、攻击与死亡",
        "priority": "Must",
        "purpose": "构成主要威胁，驱动玩家移动、战斗、建造和资源消耗。",
        "behavior": "僵尸在刷新点生成，进入感知范围后追击玩家，接近后攻击，受到足够伤害后死亡。",
        "rules": [
            "僵尸类型至少支持普通和快速两类配置。",
            "同屏数量必须受上限控制，避免性能失控。",
            "僵尸需要使用对象池或等效复用策略。",
            "联机版本中僵尸状态和伤害结果不能由普通客户端单方面决定。",
        ],
        "state": ["zombieId", "type", "hp", "position", "targetId", "state", "spawnPoint", "attackCooldown"],
        "inputs": ["刷新配置", "玩家位置", "寻路/追击查询", "受到伤害", "时间步进"],
        "outputs": ["僵尸移动", "攻击事件", "受击反馈", "死亡事件", "对象池回收"],
        "shared": "僵尸状态机、属性配置、伤害结算和对象池策略应尽量平台无关。",
        "master": "母版要能快速调数量、速度、血量和攻击范围，便于压力测试。",
        "wechat": "微信版需要控制绘制数量、纹理尺寸和更新频率，低端机可降级表现。",
        "acceptance": [
            "僵尸会生成、追击、攻击和死亡。",
            "30 只以内压力场景不会导致明显卡死。",
            "玩家能通过移动或攻击理解僵尸威胁。",
        ],
        "tests": ["状态机测试", "对象池泄漏检查", "数量压力测试", "低端机帧率观察"],
        "open": ["是否需要夜间阶段提升僵尸数量或速度。"],
        "reader": {
            "what": "僵尸会在地图上出现，并主动追玩家。",
            "show": "玩家能看到僵尸移动、攻击、受伤和死亡反馈。",
            "success": "僵尸既有威胁，又不会多到让游戏卡死或看不清。",
            "failure": "僵尸卡墙、瞬移、无限攻击或打不到玩家都需要修复。",
            "excluded": "暂不包含 Boss、复杂群体策略或肢体破坏。",
            "confirm": "需要确认僵尸整体难度偏轻松还是偏硬核。",
        },
    },
    {
        "id": "ES-FR-SURVIVAL-001",
        "module": "生存状态",
        "feature": "生命、饥饿、口渴、体力、感染",
        "priority": "Must",
        "purpose": "让玩家不仅要躲避僵尸，还要管理持续下降或变化的生存状态。",
        "behavior": "玩家拥有生命、饥饿、口渴、体力和感染等数值；数值变化会影响行动能力和失败风险。",
        "rules": [
            "生命归零会触发死亡。",
            "饥饿/口渴可随时间下降，并在过低时产生惩罚。",
            "体力用于冲刺、攻击或其他消耗动作，需恢复机制。",
            "感染可由僵尸攻击或特殊事件触发，表现和惩罚必须清楚。",
            "所有数值、下降速度、阈值和惩罚应配置化。",
        ],
        "state": ["hp", "hunger", "thirst", "stamina", "infection", "statusEffects", "lastChangedAt"],
        "inputs": ["时间步进", "受击", "使用物品", "冲刺/攻击", "配置表"],
        "outputs": ["HUD 数值", "警告提示", "状态惩罚", "死亡事件", "治疗/补给反馈"],
        "shared": "数值计算、阈值、惩罚、恢复和状态效果应平台无关。",
        "master": "母版需要调试面板或快捷键改变状态，帮助验证边界情况。",
        "wechat": "微信版 HUD 必须在小屏幕上清楚显示关键状态，警告不能遮挡移动区域。",
        "acceptance": [
            "状态数值会按规则变化。",
            "过低或异常状态会给玩家明确反馈。",
            "使用补给品能按规则恢复对应状态。",
        ],
        "tests": ["数值边界测试", "补给恢复测试", "HUD 警告显示测试", "死亡触发测试"],
        "open": ["感染是否是首版核心机制，还是作为后续增强。"],
        "reader": {
            "what": "玩家不只会被僵尸打死，也需要注意饥饿、口渴、体力和感染。",
            "show": "界面会显示这些状态，并在危险时提醒玩家。",
            "success": "玩家能通过找物资、使用补给和避免受伤来维持状态。",
            "failure": "状态太低时会行动困难、受伤或死亡，必须提前提示。",
            "excluded": "暂不包含复杂疾病树、心理状态、睡眠或温度系统。",
            "confirm": "需要确认生存状态是偏轻度压力，还是偏硬核管理。",
        },
    },
    {
        "id": "ES-FR-ITEM-001",
        "module": "物资与背包",
        "feature": "搜刮、拾取、使用、丢弃与配置",
        "priority": "Must",
        "purpose": "支持玩家在地图中寻找资源，并通过背包管理生存与建造材料。",
        "behavior": "玩家接近物资点或掉落物后可拾取物品；物品进入背包后可使用、消耗、堆叠或丢弃。",
        "rules": [
            "物品必须有唯一配置 ID、类型、堆叠上限、用途和图标。",
            "背包容量必须有限制，避免无限拾取。",
            "拾取和使用失败要给出原因，例如距离不够、背包满、状态已满或材料不足。",
            "联机版本中稀缺物资拾取必须避免多人同时拿到同一份。",
        ],
        "state": ["itemId", "itemType", "quantity", "stackLimit", "inventorySlots", "lootSpawnId", "ownerOrRoomId"],
        "inputs": ["交互按钮", "物资配置", "玩家位置", "背包状态", "服务端确认"],
        "outputs": ["拾取反馈", "背包变化", "使用效果", "丢弃物", "失败提示"],
        "shared": "物品配置、容量规则、使用效果和错误码应平台无关。",
        "master": "母版要快速生成测试物品，方便验证背包和状态恢复。",
        "wechat": "微信版背包 UI 需适配触摸点击、拖动或简化选择，避免小屏误触。",
        "acceptance": [
            "玩家能拾取、查看、使用和丢弃基础物品。",
            "背包满、材料不足等失败情况有提示。",
            "物品效果能正确影响生命/饥饿/口渴/体力/建造材料。",
        ],
        "tests": ["背包容量测试", "堆叠测试", "使用效果测试", "多人拾取冲突测试"],
        "open": ["首版背包采用格子制还是简化列表制。"],
        "reader": {
            "what": "玩家可以在地图上找食物、水、材料和武器等物资。",
            "show": "拾取后物品进入背包，玩家能看到数量、图标和用途。",
            "success": "玩家能用物资解决生存问题，或作为建造/战斗材料。",
            "failure": "背包满、离物资太远或不能使用时要明确提示。",
            "excluded": "暂不包含复杂重量系统、耐久系统或枪械配件系统。",
            "confirm": "需要确认背包是格子形式还是更简单的列表形式。",
        },
    },
    {
        "id": "ES-FR-CRAFT-001",
        "module": "合成与建造",
        "feature": "基础合成与防御工事",
        "priority": "Must",
        "purpose": "让玩家把搜刮到的材料转化成生存优势，例如制作物品或放置路障/木墙/封窗。",
        "behavior": "玩家打开合成/建造界面，选择配方或工事，满足材料和位置规则后生成结果。",
        "rules": [
            "配方必须配置化，包含材料、产物、数量和解锁条件。",
            "建造必须检查材料、距离、碰撞、区域、数量上限和放置合法性。",
            "放置前应显示预览，合法/非法状态要明显区分。",
            "建造物应有耐久，能被僵尸或规则破坏。",
        ],
        "state": ["recipeId", "materials", "buildType", "placementPosition", "placementValid", "durability", "ownerId"],
        "inputs": ["建造按钮", "配方配置", "背包材料", "指针/触摸位置", "碰撞查询"],
        "outputs": ["预览图", "建造成功/失败提示", "材料消耗", "建造物实例", "耐久变化"],
        "shared": "配方、材料消耗、合法性检查和耐久规则应平台无关。",
        "master": "母版需要调试网格、放置预览和碰撞可视化，便于调整手感。",
        "wechat": "微信版建造操作要适合触摸，按钮和预览不能挡住玩家关键视野。",
        "acceptance": [
            "玩家能用材料制作至少一种物品或放置至少一种工事。",
            "非法位置不能建造，并有明确反馈。",
            "材料消耗和建造结果一致。",
        ],
        "tests": ["配方测试", "合法/非法放置测试", "材料扣除测试", "耐久破坏测试"],
        "open": ["首版是否只做网格吸附建造，避免自由旋转造成同步和碰撞问题。"],
        "reader": {
            "what": "玩家可以把材料做成有用物品，或放置简单防御工事保护自己。",
            "show": "建造前会有预览，能放的位置和不能放的位置要看得出来。",
            "success": "材料足够且位置合法时，建造物成功出现并消耗材料。",
            "failure": "材料不足、距离太远、位置冲突或区域不允许时不能建造。",
            "excluded": "暂不包含自由地形改造、大型基地、复杂电力或自动化系统。",
            "confirm": "需要确认建造是网格吸附，还是允许更自由的摆放。",
        },
    },
    {
        "id": "ES-FR-COMBAT-001",
        "module": "战斗",
        "feature": "武器、攻击、命中、伤害与反馈",
        "priority": "Must",
        "purpose": "让玩家可以主动对抗僵尸，并通过武器差异形成策略选择。",
        "behavior": "玩家使用近战或远程武器攻击，系统按范围、方向、冷却和目标状态计算命中与伤害。",
        "rules": [
            "武器必须配置攻击范围、伤害、冷却、表现和消耗。",
            "攻击需要有前摇/冷却或等效限制，不能无限连发。",
            "命中反馈至少包含音效/动画/数值或受击表现之一。",
            "联机版本中关键伤害结果必须由服务端或可信同步确认。",
        ],
        "state": ["weaponId", "damage", "range", "cooldown", "attackState", "lastAttackAt", "targetHitList"],
        "inputs": ["攻击按钮", "武器配置", "玩家朝向", "目标碰撞", "时间步进"],
        "outputs": ["攻击动画", "命中事件", "伤害数值", "受击反馈", "击杀事件"],
        "shared": "武器配置、冷却、命中检测语义和伤害公式应平台无关。",
        "master": "母版可显示攻击范围和命中框，便于调手感。",
        "wechat": "微信版攻击按钮必须适合拇指操作，避免和移动摇杆冲突。",
        "acceptance": [
            "玩家能攻击僵尸并造成伤害。",
            "攻击冷却有效，不能无间隔攻击。",
            "命中/未命中/击杀反馈清楚。",
        ],
        "tests": ["攻击范围测试", "冷却测试", "伤害边界测试", "按钮误触测试"],
        "open": ["首版是否包含远程武器，还是先以近战为主。"],
        "reader": {
            "what": "玩家可以使用武器攻击僵尸。",
            "show": "攻击时有动画或特效，打中后僵尸有受击反馈。",
            "success": "玩家能理解自己有没有打中、造成了多少效果、僵尸是否死亡。",
            "failure": "距离不够、冷却没好或方向不对时，攻击不应错误命中。",
            "excluded": "暂不包含复杂枪械配件、弹道穿透或部位伤害。",
            "confirm": "需要确认首版武器以近战为主，还是加入远程武器。",
        },
    },
    {
        "id": "ES-FR-UI-001",
        "module": "界面",
        "feature": "HUD、触摸控件、背包、建造、结算",
        "priority": "Must",
        "purpose": "让玩家在手机屏幕上清楚看到状态、操作按钮和系统反馈。",
        "behavior": "界面展示生命/状态、移动摇杆、攻击/交互/背包/建造按钮、提示信息和结算面板。",
        "rules": [
            "HUD 不能遮挡核心视野和触摸移动区域。",
            "所有关键按钮要适配安全区和不同屏幕比例。",
            "状态变化、失败原因和危险警告必须可读。",
            "结算面板必须说明结束原因和主要结果。",
        ],
        "state": ["hudState", "safeArea", "screenSize", "visiblePanel", "promptQueue", "resultSummary"],
        "inputs": ["屏幕尺寸", "安全区", "玩家状态", "背包数据", "按钮点击", "结算数据"],
        "outputs": ["HUD", "虚拟摇杆", "按钮", "弹窗", "提示", "结算界面"],
        "shared": "UI 状态和展示数据应与玩法逻辑解耦。",
        "master": "母版可使用 DOM 或 Phaser UI 快速迭代布局，但要记录微信版等效实现。",
        "wechat": "微信版优先使用 Canvas/小游戏可用 UI 方案，保证全屏、自适应和触摸命中。",
        "acceptance": [
            "常用操作在手机模拟器上可见且可点。",
            "横屏/不同机型不会出现关键按钮超出屏幕。",
            "结算信息能被项目 owner 看懂。",
        ],
        "tests": ["多分辨率截图", "安全区检查", "触摸命中测试", "结算文案检查"],
        "open": ["背包和建造是否使用同一侧边面板，还是分成两个入口。"],
        "reader": {
            "what": "玩家通过屏幕按钮、摇杆和面板操作游戏。",
            "show": "界面会显示状态条、按钮、背包、建造入口和结果界面。",
            "success": "玩家不用猜按钮作用，也不会因为屏幕适配问题点不到。",
            "failure": "按钮遮挡、文字太小、刘海遮住信息或黑边异常都需要修复。",
            "excluded": "暂不包含复杂皮肤商城、社交大厅或大量动画菜单。",
            "confirm": "需要确认 HUD 风格是偏简洁生存，还是偏卡通休闲。",
        },
    },
    {
        "id": "ES-FR-NET-001",
        "module": "联机",
        "feature": "房间、状态同步、重连与结算一致性",
        "priority": "Should",
        "purpose": "支持多人目标时，保证多个玩家看到的关键状态一致，避免刷榜和结算分歧。",
        "behavior": "玩家可通过匹配或房间进入同一局，服务端或可信同步层负责关键状态、掉落、建造、伤害和结算。",
        "rules": [
            "房间需要创建、加入、准备、开局、进行中、结算、销毁状态。",
            "关键状态不能完全依赖普通客户端自报。",
            "断线重连需要令牌、超时和失败处理。",
            "结算必须幂等，避免重复奖励或重复写榜。",
        ],
        "state": ["roomId", "playerId", "seatState", "tick", "snapshotVersion", "reconnectToken", "settlementId"],
        "inputs": ["匹配请求", "房间码", "玩家输入", "服务端快照", "断线/重连", "结算请求"],
        "outputs": ["房间状态", "玩家同步", "世界快照", "重连结果", "结算确认"],
        "shared": "协议字段、房间状态、结算规则和错误码要文档化。",
        "master": "母版可先用本地模拟或轻量 WebSocket 验证协议和状态。",
        "wechat": "微信版要处理网络权限、弱网、前后台断连和重连提示。",
        "acceptance": [
            "多人进入同一房间后关键状态不会持续分歧。",
            "断线后能重连或明确失败退出。",
            "结算只发生一次，且结果一致。",
        ],
        "tests": ["房间状态测试", "弱网测试", "断线重连测试", "重复结算测试"],
        "open": ["多人联机是否为首个可玩版本的必需功能，还是先做单人完整闭环。"],
        "reader": {
            "what": "如果做多人，玩家可以和其他人进入同一局一起生存。",
            "show": "玩家能看到房间、队友、同步动作和最终统一结算。",
            "success": "大家看到的关键结果一致，不会一个人显示赢、另一个人显示失败。",
            "failure": "掉线、重连失败或房间异常时要有明确提示。",
            "excluded": "暂不包含观战、大型房间或复杂语音社交。",
            "confirm": "需要确认多人是否是首版必须项，还是先用单人版本验证玩法。",
        },
    },
    {
        "id": "ES-FR-WECHAT-001",
        "module": "微信小游戏",
        "feature": "微信运行时、触摸、资源、登录、广告与发布适配",
        "priority": "Must",
        "purpose": "保证浏览器母版中验证过的功能能在微信开发者工具、模拟器和真机中运行。",
        "behavior": "微信适配版加载游戏资源，创建 Canvas/WebGL 运行环境，处理触摸、生命周期、安全区、登录、广告和上传提审相关要求。",
        "rules": [
            "微信版源码必须独立保留，不能覆盖浏览器母版源码。",
            "平台桥接层集中处理微信 API，不把 wx 依赖散落到共享 gameplay 逻辑。",
            "资源加载失败必须有重试或降级路径。",
            "登录、广告、榜单、隐私授权必须遵守微信平台规则。",
            "AppSecret、云密钥和私人 token 不得进入客户端仓库。",
        ],
        "state": ["platform", "systemInfo", "safeArea", "assetManifest", "loginState", "adState", "lifecycleState"],
        "inputs": ["wx 生命周期", "触摸事件", "资源加载回调", "wx.login", "广告 API", "开发者工具配置"],
        "outputs": ["运行时初始化", "触摸输入", "资源缓存", "登录凭证", "广告结果", "错误日志"],
        "shared": "共享逻辑只依赖抽象平台接口，不直接调用微信 API。",
        "master": "母版需要保留等效的浏览器平台接口实现，方便本地调试。",
        "wechat": "微信版实现真实 wx 平台接口，并保留模拟器和真机验证记录。",
        "acceptance": [
            "微信开发者工具中不黑屏，画面铺满目标手机模拟器。",
            "触摸移动、图片加载、生命周期和基础错误日志可用。",
            "真机预览能进入游戏并完成基础操作。",
        ],
        "tests": ["开发者工具模拟器", "真机预览", "资源失败测试", "前后台切换", "广告回调测试"],
        "open": ["正式 AppID、登录、广告和排行榜能力何时启用由项目 owner 决定。"],
        "reader": {
            "what": "最终游戏要能作为微信小游戏运行。",
            "show": "玩家在微信里打开后能看到完整画面，用手指操作，并正常加载资源。",
            "success": "微信开发者工具和真机都能进入游戏，不黑屏、不只显示一小块、不丢触摸。",
            "failure": "网络、广告或登录失败时不能卡死，要告诉玩家或回退。",
            "excluded": "暂不承诺一次性接入所有微信商业化和社交能力。",
            "confirm": "需要确认正式 AppID、登录、广告、排行榜分别何时启用。",
        },
    },
    {
        "id": "ES-FR-DATA-001",
        "module": "数据与配置",
        "feature": "配置、存档、事件记录与版本信息",
        "priority": "Must",
        "purpose": "让游戏行为可配置、问题可追踪、版本可定位，并为后续后台/运营数据打基础。",
        "behavior": "游戏读取配置驱动数值；记录版本、关键事件、错误和结算摘要；必要时保存本地或服务端进度。",
        "rules": [
            "配置必须有版本号，日志必须能关联客户端版本和配置版本。",
            "事件记录不能包含不必要的个人敏感信息。",
            "本地存档只能保存低风险数据；排行榜和奖励必须走可信后端。",
            "错误日志要能帮助定位平台、机型、资源版本和发生模块。",
        ],
        "state": ["clientVersion", "configVersion", "resourceVersion", "saveData", "eventQueue", "errorLog"],
        "inputs": ["配置文件", "玩家事件", "错误事件", "结算数据", "平台信息"],
        "outputs": ["配置对象", "本地存档", "事件日志", "错误日志", "结算摘要"],
        "shared": "配置 schema、事件名称、错误码和版本字段应统一。",
        "master": "母版可把日志输出到控制台和本地调试面板。",
        "wechat": "微信版需要使用小游戏可用的存储、日志和上报路径，并避免敏感信息泄漏。",
        "acceptance": [
            "能在日志中看到客户端版本、配置版本和平台信息。",
            "配置变化能影响游戏数值，不需要改代码。",
            "错误能被捕获并显示或记录。",
        ],
        "tests": ["配置加载测试", "版本日志测试", "错误捕获测试", "隐私字段检查"],
        "open": ["是否使用后端保存长期账号数据，还是首版只保留本地进度和结算摘要。"],
        "reader": {
            "what": "游戏需要记录配置、版本和必要的游戏事件，方便排查问题。",
            "show": "玩家通常看不到这些细节，但能受益于更稳定的版本和更快的问题修复。",
            "success": "出问题时能知道是哪一版、哪个资源、哪个功能出错。",
            "failure": "不能把密钥或不必要的个人信息放进客户端或日志。",
            "excluded": "暂不包含复杂用户画像或过度数据采集。",
            "confirm": "需要确认是否做账号云存档，还是先只做本地存档。",
        },
    },
    {
        "id": "ES-NFR-001",
        "module": "非功能",
        "feature": "性能、兼容、安全与可维护性",
        "priority": "Must",
        "purpose": "保证游戏不仅能跑，还能在目标手机、微信环境和后续迭代中稳定维护。",
        "behavior": "系统要控制帧率、内存、资源体积、启动速度、触摸响应、安全和代码边界。",
        "rules": [
            "浏览器母版和微信适配版都必须保留可运行说明。",
            "平台相关代码必须隔离，便于替换和排错。",
            "新增功能必须说明性能影响和微信适配影响。",
            "禁止提交 AppSecret、数据库密码、云密钥、个人 token 或未授权资产。",
        ],
        "state": ["fps", "memory", "assetSize", "startupTime", "platformAdapterVersion", "knownIssues"],
        "inputs": ["性能采样", "构建产物", "资源清单", "平台信息", "错误日志"],
        "outputs": ["性能报告", "兼容记录", "构建说明", "已知问题", "风险清单"],
        "shared": "编码规范、配置版本、错误码和测试记录要贯穿两套代码。",
        "master": "母版优先保证开发效率和可调试性。",
        "wechat": "微信版优先保证真机可运行、首包/资源策略、触摸和生命周期稳定。",
        "acceptance": [
            "新窗口 Codex 能根据文档找到两套代码和运行方式。",
            "关键功能有验收标准和测试记录位置。",
            "敏感信息和平台专用代码没有污染共享逻辑。",
        ],
        "tests": ["构建说明检查", "敏感信息扫描", "平台边界审查", "性能记录检查"],
        "open": ["需要确认目标最低设备范围和正式性能红线。"],
        "reader": {
            "what": "游戏需要在手机上稳定、流畅、安全地运行。",
            "show": "玩家感受到的是加载更快、操作更顺、崩溃更少。",
            "success": "新功能不会让游戏明显变卡、变黑屏或在微信里无法运行。",
            "failure": "卡顿、黑屏、资源失败、按钮失效、密钥泄漏都属于严重问题。",
            "excluded": "暂不承诺支持所有极老设备或所有特殊系统版本。",
            "confirm": "需要确认最低支持设备和可接受的性能目标。",
        },
    },
]


def bullet(items: list[str], indent: str = "") -> str:
    return "\n".join(f"{indent}- {item}" for item in items)


def detect_dirs(project_root: Path) -> tuple[str, str]:
    poc = project_root / "phaser-wechat-poc"
    master = poc / "src"
    wechat = poc / "wechatgame"
    master_label = str(master) if master.exists() else "Game Studio/Phaser master source directory"
    wechat_label = str(wechat) if wechat.exists() else "WeChat Mini Game adaptation source directory"
    return master_label, wechat_label


def ai_doc(project_root: Path) -> str:
    master_dir, wechat_dir = detect_dirs(project_root)
    rows = [
        "| ID | Module | Feature | Priority | Shared logic | Phaser master | WeChat adaptation | Status |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for f in FEATURES:
        rows.append(
            f"| {f['id']} | {f['module']} | {f['feature']} | {f['priority']} | required | required | required | planned |"
        )

    blocks = []
    for f in FEATURES:
        blocks.append(
            f"""### {f['id']}: {f['feature']}

- **Module**: {f['module']}
- **Priority**: {f['priority']}
- **Purpose**: {f['purpose']}
- **Player-visible behavior**: {f['behavior']}
- **Rules**:
{bullet(f['rules'], '  ')}
- **State/data**: {", ".join(f['state'])}
- **Inputs**: {", ".join(f['inputs'])}
- **Outputs/events**: {", ".join(f['outputs'])}
- **Shared implementation notes**: {f['shared']}
- **Game Studio / Phaser master requirements**: {f['master']}
- **WeChat Mini Game adaptation requirements**: {f['wechat']}
- **Acceptance criteria**:
{bullet(f['acceptance'], '  ')}
- **Test notes**:
{bullet(f['tests'], '  ')}
- **Open questions**:
{bullet(f['open'], '  ')}
"""
        )

    return f"""# {PROJECT_NAME} AI 功能需求文档

> This document is for Codex/developer continuation. It contains functional requirements only and intentionally excludes schedules, dates, sprint plans, staffing plans, launch forecasts, and budget estimates.

## 1. Project continuation contract

- Final product target: WeChat Mini Game.
- Development strategy: build gameplay first in a Game Studio + Phaser/TypeScript browser master, then migrate stable features into a separate WeChat Mini Game adaptation.
- Both code versions must remain available and runnable.
- Current master source location: `{master_dir}`.
- Current WeChat adaptation source location: `{wechat_dir}`.
- Shared gameplay logic should stay platform-independent.
- WeChat-specific runtime logic belongs in a platform adaptation layer.
- A feature is not done until the master version and WeChat adaptation both have clear acceptance evidence.

## 2. Functional requirement index

{chr(10).join(rows)}

## 3. Module requirements

{chr(10).join(blocks)}

## 4. Cross-cutting implementation rules

- Use stable requirement IDs in code comments, tests, issue names, and future docs when practical.
- Add platform APIs behind an adapter boundary instead of calling WeChat APIs directly from shared gameplay modules.
- Keep configuration data versioned and readable by both code versions.
- For every feature, record whether behavior was verified in browser master, WeChat simulator, and real device.
- Keep open questions visible; do not silently decide product behavior that affects player experience.

## 5. Explicit non-goals

- No development schedule in this document.
- No launch date, revenue guarantee, or platform approval guarantee.
- No first-person mode, large open world, complex physics destruction, all-building interiors, or large social lobby unless separately approved.
"""


def reader_doc() -> str:
    sections = []
    for f in FEATURES:
        r = f["reader"]
        sections.append(
            f"""### {f['module']}：{f['feature']}

- **玩家能做什么**：{r['what']}
- **游戏会显示什么**：{r['show']}
- **规则说明**：{f['behavior']}
- **成功条件**：{r['success']}
- **失败/异常情况**：{r['failure']}
- **暂不包含**：{r['excluded']}
- **需要你确认**：{r['confirm']}
"""
        )

    return f"""# {PROJECT_NAME} 功能需求说明书

> 这是一份给项目 owner 阅读和确认的功能需求文档。它只描述功能，不包含开发周期、日期、排期或上线承诺。

## 1. 一句话说明

《末日余生：极限生存》是一款 2D 俯视/轻量斜视角的末日生存微信小游戏。玩家在危险地图中移动、搜刮、维持生存状态、对抗僵尸、建造简单防御，并在一局结束后获得结算结果。

## 2. 版本制作方式

- 先制作浏览器试玩母版，用来快速验证玩法是否好玩、操作是否顺手。
- 再制作微信小游戏适配版，用来处理微信平台的触摸、屏幕、安全区、登录、广告、资源加载和真机运行。
- 两个版本都会保留。母版用于继续调玩法，微信版用于最终发布和真机验证。
- 两个版本的玩法规则应保持一致；微信平台专用问题只放在适配层处理。

## 3. 玩家核心体验

玩家进入一局游戏后，需要在地图上探索和搜刮物资，同时注意生命、饥饿、口渴、体力和感染等状态。僵尸会带来持续威胁，玩家可以战斗、躲避、使用物资或建造简单工事来提高生存机会。游戏结束后，系统展示本局表现和奖励。

## 4. 功能模块

{chr(10).join(sections)}

## 5. 首版不包含的内容

- 不承诺大规模开放世界。
- 不承诺第一人称玩法。
- 不承诺复杂物理破坏。
- 不承诺所有建筑都可进入。
- 不承诺大型社交大厅、观战、语音或复杂公会系统。
- 不承诺广告收益或平台审核结果。

## 6. 需要集中确认的问题

- 游戏正式方向采用横屏还是竖屏？
- 一局结束目标是生存时长、撤离目标、任务目标，还是组合？
- 首个完整版本是否必须多人联机，还是先完成单人核心闭环？
- 感染、饥饿、口渴的惩罚强度应该偏轻松还是偏硬核？
- 广告复活是否进入首版，是否影响排行榜？
- 背包采用格子形式还是简化列表形式？
- 建造采用网格吸附还是更自由的摆放？
- 美术风格更偏卡通轻松，还是偏末日压迫感？
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".", help="Project root path")
    parser.add_argument("--out-dir", default=None, help="Output directory")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else project_root / "deliverables" / "requirements"
    out_dir.mkdir(parents=True, exist_ok=True)

    ai_path = out_dir / "ai-functional-requirements.md"
    reader_path = out_dir / "reader-functional-requirements.md"
    ai_path.write_text(ai_doc(project_root), encoding="utf-8", newline="\n")
    reader_path.write_text(reader_doc(), encoding="utf-8", newline="\n")

    print(ai_path)
    print(reader_path)


if __name__ == "__main__":
    main()
