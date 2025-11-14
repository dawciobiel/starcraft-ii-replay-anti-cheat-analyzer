-- Schema Version: 1.2
-- schema.sql

-- 🧑 Players
CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    player_name TEXT NOT NULL,
    is_human BOOLEAN,
    toon_id INTEGER,
    bnet_uri TEXT,
    region TEXT,
    realm TEXT,
    race TEXT,
    team TEXT,
    color TEXT,
    mmr INTEGER,
    enemy_workers_killed INTEGER
);

-- 🕒 Timeline
CREATE TABLE timeline (
    timeline_id INTEGER PRIMARY KEY,
    tick INTEGER,
    second REAL
);

-- 🏠 Structures
CREATE TABLE structures (
    structure_id INTEGER PRIMARY KEY,
    player_id INTEGER,
    name TEXT,
    x INTEGER,
    y INTEGER,
    z INTEGER,
    is_flying BOOLEAN,
    timeline_id INTEGER,
    FOREIGN KEY(player_id) REFERENCES players(player_id),
    FOREIGN KEY(timeline_id) REFERENCES timeline(timeline_id)
);

-- 🧍 Units
CREATE TABLE units (
    unit_id INTEGER PRIMARY KEY,
    player_id INTEGER,
    name TEXT,
    x INTEGER,
    y INTEGER,
    z INTEGER,
    hp INTEGER,
    shield INTEGER,
    energy INTEGER,
    timeline_id INTEGER,
    FOREIGN KEY(player_id) REFERENCES players(player_id),
    FOREIGN KEY(timeline_id) REFERENCES timeline(timeline_id)
);

-- 🎥 Camera Events
CREATE TABLE camera_events (
    camera_id INTEGER PRIMARY KEY,
    player_id INTEGER,
    x INTEGER,
    y INTEGER,
    timeline_id INTEGER,
    FOREIGN KEY(player_id) REFERENCES players(player_id),
    FOREIGN KEY(timeline_id) REFERENCES timeline(timeline_id)
);

-- 🧪 Upgrades (optional)
CREATE TABLE upgrades (
    upgrade_id INTEGER PRIMARY KEY,
    player_id INTEGER,
    name TEXT,
    completed_at INTEGER,
    FOREIGN KEY(player_id) REFERENCES players(player_id)
);

-- 🚨 Alerts (generated during analysis)
CREATE TABLE alerts (
    alert_id INTEGER PRIMARY KEY,
    player_id INTEGER,
    tick INTEGER,
    type TEXT,
    description TEXT,
    FOREIGN KEY(player_id) REFERENCES players(player_id)
);

-- 🎯 Command Events
CREATE TABLE command_events (
    command_id INTEGER PRIMARY KEY,
    player_id INTEGER,
    timeline_id INTEGER,
    x INTEGER,
    y INTEGER,
    ability_name TEXT,
    target_unit_id INTEGER,
    FOREIGN KEY(player_id) REFERENCES players(player_id),
    FOREIGN KEY(timeline_id) REFERENCES timeline(timeline_id)
);

-- 📈 Player APM
CREATE TABLE player_apm (
    apm_id INTEGER PRIMARY KEY,
    player_id INTEGER,
    timeline_id INTEGER,
    apm INTEGER,
    epm INTEGER,
    FOREIGN KEY(player_id) REFERENCES players(player_id),
    FOREIGN KEY(timeline_id) REFERENCES timeline(timeline_id)
);

-- 🖱️ Selection Events
CREATE TABLE selection_events (
    selection_id INTEGER PRIMARY KEY,
    player_id INTEGER,
    timeline_id INTEGER,
    selected_unit_ids TEXT,
    camera_x INTEGER,
    camera_y INTEGER,
    FOREIGN KEY(player_id) REFERENCES players(player_id),
    FOREIGN KEY(timeline_id) REFERENCES timeline(timeline_id)
);

-- 👥 Control Group Events

CREATE TABLE control_group_events (

    control_group_event_id INTEGER PRIMARY KEY,

    player_id INTEGER,

    timeline_id INTEGER,

    control_group_id INTEGER,

    action TEXT,

    units_selected TEXT,

    FOREIGN KEY(player_id) REFERENCES players(player_id),

    FOREIGN KEY(timeline_id) REFERENCES timeline(timeline_id)

);



-- 📊 Player Stats Events



CREATE TABLE player_stats_events (



    stats_id INTEGER PRIMARY KEY,



    player_id INTEGER,



    timeline_id INTEGER,



    minerals_collection_rate INTEGER,



    vespene_collection_rate INTEGER,



    workers_active_count INTEGER,



    food_used INTEGER,



    food_made INTEGER,



    FOREIGN KEY(player_id) REFERENCES players(player_id),



    FOREIGN KEY(timeline_id) REFERENCES timeline(timeline_id)



);







-- 💀 Unit Deaths







CREATE TABLE unit_deaths (







    death_id INTEGER PRIMARY KEY,







    unit_id INTEGER,







    killer_player_id INTEGER,







    player_id INTEGER, -- Owner of the unit that died







    timeline_id INTEGER,







    unit_name TEXT,







    x INTEGER,







    y INTEGER,







    FOREIGN KEY(player_id) REFERENCES players(player_id),







    FOREIGN KEY(killer_player_id) REFERENCES players(player_id),







    FOREIGN KEY(timeline_id) REFERENCES timeline(timeline_id)







);












