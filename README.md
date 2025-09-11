# Survival Game (Zork-like)

## Team Members
- Kevin Yavari Yoshioka
- Jean Karlo Buitrago Orozco

## Project Description
This project is a **text-based RPG survival game** developed in Python.  
The player takes the role of a survivor trapped inside a nuclear facility after a sudden attack.  
The goal is to **explore rooms, collect useful objects, survive encounters with infected enemies, and escape through the exits** by finding the correct keys.

The game features:
- **Inventory system** with capacity, item usage, and the ability to drop items in rooms.  
- **Map system** represented as a graph, where each room is connected logically and may contain objects or enemies.  
- **Enemy encounters** with turn-based combat mechanics.  
- **Audio integration with OpenAL**, providing ambient sounds, footsteps, combat effects, and room-specific audio.  
- **Condition-based gameplay**, including bleeding status, healing with first aid kits, and buffs from special items like the blanket (increasing defense).

## Justification
We designed the game this way for several reasons:

1. **Immersion through audio**  
   By integrating OpenAL, we added spatial and environmental sounds to create tension and atmosphere. This makes the text-based game feel more alive and interactive.

2. **Replayability through exploration**  
   The map and room-connection system allow for non-linear exploration. Players are free to choose different paths, making each run unique.

3. **Strategic inventory management**  
   Limiting inventory space forces players to make meaningful decisions: which items to keep, use, or drop. This increases the survival challenge.

4. **Balance between narrative and mechanics**  
   Instead of overwhelming players with complex rules, we focused on a simple yet engaging system where exploration, combat, and resource management are interconnected with the story.

5. **Modular and extensible codebase**  
   We implemented separate classes (`Game`, `Room`, `Player`, `Enemy`, `Object`, `Inventory`, `AudioManager`, etc.), which makes the project easier to maintain and expand. New items, enemies, or rooms can be added without rewriting the whole system.

---

This approach ensured that the game is **immersive, challenging, and extensible**, while also highlighting good programming practices such as object-oriented design, modularity, and event-driven logic.
