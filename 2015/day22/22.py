# Day 22: Wizard Simulator 20XX (2015)
from copy import deepcopy, copy
from dataclasses import dataclass, field
from typing import List

from common.utils import problem_harness, timeit, read_input


@dataclass
class Effect:
  name: str = ''
  cost: int = 0
  remaining_duration: int = 0
  # recurring stuff
  armor: int = 0
  damage: int = 0
  heal: int = 0
  mana_regen: int = 0
  # instant stuff
  instant_hp_gain: int = 0
  instant_damage: int = 0

@dataclass
class Character:
  hp: int = 0
  mana: int = 0
  armor: int = 0
  damage: int = 0
  spent: int = 0

@dataclass
class GameState:
  player: Character
  boss: Character
  active_effects: List[Effect]
  history: List[Effect] = field(default_factory=list)

  def __str__(self):
    s = f"  Player: {self.player}\n  Boss: {self.boss}\n  Active Effects: "
    for effect in self.active_effects:
      s += f"{effect.name}({effect.remaining_duration}) "
    s += "\n  History: "
    s += "->".join([e.name for e in self.history])
    return s
  
  def game_over(self) -> bool:
    return self.player.hp <= 0 or self.boss.hp <= 0
  
  def player_wins(self) -> bool:
    return self.game_over() and self.boss.hp <= 0
  

AvailableSpells = [
  Effect('Recharge', cost=229, remaining_duration=5, mana_regen=101),
  Effect('Shield', cost=113, remaining_duration=6, armor=7),
  Effect('Drain', cost=73, instant_damage=2, instant_hp_gain=2),
  Effect('Poison', cost=173, remaining_duration=6, damage=3),
  Effect('Magic Missile', cost=53, instant_damage=4),
]


def apply_active_effects(state: GameState) -> GameState:
  for effect in state.active_effects:
    if effect.name == 'Shield' and effect.remaining_duration == 6:
      state.player.armor += effect.armor
    state.boss.hp -= effect.damage
    state.player.hp += effect.heal
    state.player.mana += effect.mana_regen
    effect.remaining_duration -= 1
    if effect.remaining_duration <= 0:
      if effect.name == 'Shield':
        state.player.armor -= effect.armor
  state.active_effects = [
    e for e in state.active_effects if e.remaining_duration > 0]
  return state

def valid(spell: Effect, state: GameState) -> bool:
  if spell.cost > state.player.mana:
    return False
  if spell.name in [e.name for e in state.active_effects]:
    return False
  return True


# Notes:
# - player turn:
#   - apply effects
#   - pick a spell + apply instant effects
#   - save on player's active effects
# - boss turn:
#   - apply effects
#   - boss does damage
# - check if anyone has died / there is a winner
# 
# Anytime there is a decision about the effect to choose we should try both
# taking it and not taking it and track the best outcome - could do it
# recursively? Probably need deep copies of the game state to do this so the
# player and bosses are new 


def play_game(
    s: GameState,
    min_cost: int,
    hard_mode=False) -> int:
  
  # check if the game is over 
  if s.game_over():
    return min(min_cost, s.player.spent) if s.player_wins() else min_cost

  if s.player.spent > min_cost:
    return min_cost # already spent more than the minimum
  
  # player loses a point (part 2)
  if hard_mode:
    s.player.hp -= 1

  # apply any active effects
  s = apply_active_effects(s)

  # start player turn
  for tmp in AvailableSpells:

    # make a copy of the spell so we can mutate it
    spell = deepcopy(tmp)

    if not valid(spell, s):
      continue 

    # apply the spell: - copy of state so we don't mutate
    state = deepcopy(s)
    #state = GameState(
    #  player=deepcopy(s.player),
    #  boss=deepcopy(s.boss),
    #  active_effects=deepcopy(s.active_effects),
    #  history=deepcopy(s.history)
    #)
    state.history.append(spell)

    # apply the spell: cost
    state.player.mana -= spell.cost
    state.player.spent += spell.cost

    # we can bail if we're spending more than the current best solution
    # that we have found
    if state.player.spent > min_cost:
      continue

    # apply instant effects
    state.player.hp += spell.instant_hp_gain
    state.boss.hp -= spell.instant_damage
  
    # save the active effect
    if spell.remaining_duration > 0:
      state.active_effects.append(spell)


    # check if the game is over
    if state.game_over():
      if state.player_wins():
        min_cost = min(min_cost, state.player.spent)
      continue

    # boss turn - apply effects
    state = apply_active_effects(state)

    # check if the game is over - effects could have killed the boss 
    if state.game_over():
      if state.player_wins():
        min_cost = min(min_cost, state.player.spent)
      continue
   
    # boss turn - boss does damage
    state.player.hp -= max(1, state.boss.damage - state.player.armor)

    # check if the game is over
    if state.game_over():
      if state.player_wins():
        min_cost = min(min_cost, state.player.spent)
      continue

    # recurse
    min_cost = min(min_cost, play_game(state, min_cost, hard_mode))

  return min_cost



@timeit
def part1(_: str) -> int:
  # What is the least amount of many you can spend and still win the fight?
  boss = Character(hp=71, damage=10)
  player = Character(hp=50, mana=500)
  state = GameState(player=player, boss=boss, active_effects=[])
  return play_game(state, float('inf'))


@timeit
def part2(_: str) -> int:
  boss = Character(hp=71, damage=10)
  player = Character(hp=50, mana=500)
  state = GameState(player=player, boss=boss, active_effects=[])
  return play_game(state, float('inf'), hard_mode=True)


def main():
  problem_harness(part1, part2)


if __name__ == '__main__':
  main()
