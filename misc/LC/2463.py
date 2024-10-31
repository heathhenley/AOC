import time
from typing import List


def min_distance(
        robot: List[int], factory: List[List[int]]) -> int:
  """ This is the basic recursive version """
  robot.sort()
  factory.sort(key=lambda x: x[0])

  flat_factory = []
  for pos, limit in factory:
    for n in range(limit):
      flat_factory.append(pos)


  # the recursive function but memoized
  def min_distance(robot_idx, factory_idx):
    if robot_idx == len(robot):
      return 0
    if factory_idx == len(flat_factory):
      return int(1e12)

    # We either put this robot at the next factory
    # and increment both, or we skip
    take = abs(robot[robot_idx] - flat_factory[factory_idx]) + min_distance(
      robot_idx + 1, factory_idx + 1
    )
    skip = min_distance(robot_idx, factory_idx + 1)
    return min(take, skip)
  return min_distance(0, 0)



def min_distance_memo(
        robot: List[int], factory: List[List[int]]) -> int:
  """ This is recursive with some help (memoization) """
  robot.sort()
  factory.sort(key=lambda x: x[0])

  flat_factory = []
  for pos, limit in factory:
    for n in range(limit):
      flat_factory.append(pos)

  dp = [[None] * (len(flat_factory) + 1) for _ in range(len(robot) + 1)]

  # the recursive function but memoized
  def min_distance(robot_idx, factory_idx):
    if dp[robot_idx][factory_idx] is not None:
      return dp[robot_idx][factory_idx]
    if robot_idx == len(robot):
      return 0
    if factory_idx == len(flat_factory):
      return int(1e15)

    # We either put this robot at the next factory
    # and increment both, or we skip
    take = abs(robot[robot_idx] - flat_factory[factory_idx]) + min_distance(
      robot_idx + 1, factory_idx + 1
    )
    skip = min_distance(robot_idx, factory_idx + 1)
    dp[robot_idx][factory_idx] = min(take, skip)
    return dp[robot_idx][factory_idx]
  return min_distance(0, 0)


def min_distance_dp(robots: List[int], factory: List[List[int]]) -> int:
  """ This is the iterative dp version that's hard for me to understand
  https://leetcode.com/problems/minimum-total-distance-traveled/editorial/#approach-3-tabulation (there are what I need to work on, would never come up
  with this on my own at this point)
  """
  robots.sort()
  factory.sort(key=lambda x: x[0])

  flat_factory = []
  for pos, limit in factory:
    for _ in range(limit):
      flat_factory.append(pos)

  dp = [[0] * (len(flat_factory) + 1) for _ in range(len(robots) + 1)]

  # Base cases - no factories, super large distance
  for i in range(len(robots)):
    dp[i][len(flat_factory)] = int(1e12)
  
  # Fill in the dp table "bottom up"
  for i in range(len(robots) - 1, -1, -1):
    for j in range(len(flat_factory) - 1, -1, -1):

      # the robot takes the current factory
      take = abs(robots[i] - flat_factory[j]) + dp[i + 1][j + 1]

      # the robot skips the current factory
      skip = dp[i][j + 1]

      # keep the best option
      dp[i][j] = min(take, skip)
  return dp[0][0]


def main():
  test_cases = [
    # [robot, factory, expected]
    [[0, 4, 6], [[2, 2], [6, 2]], 4],
    [[1, -1], [[-2, 1], [2, 1]], 2],
    [[670355988,403625544,886437985,224430896,126139936,-477101480,-868159607,-293937930], [[333473422,7],[912209329,7],[468372740,7],[-765827269,4],[155827122,4],[635462096,2],[-300275936,2],[-115627659,0]], 509199280],
    [[9,11,99,101], [[10,1],[7,1],[14,1],[100,1],[96,1],[103,1]], 6],
    [
      [-130743012,30616327,665137438,-607129880,333278053,824237381,209140304,-21439914,-728431071,-26955918,-570435494,-320226115,-922013064,-228553160,468665987,879432909,-514864202,-668531403,-678242745,-418104261,199254410,-792384378,741930631],
[[-456262106,1],[58412189,11],[967520832,9],[564041132,8],[-443010337,8],[990138357,22],[-10111256,12],[-140527933,14],[533615261,8],[-963214494,4],[893755326,23],[-865481531,8],[762205277,14],[288241408,11],[-133736866,0],[177042365,11],[138164674,17],[437863739,21],[889552593,8],[-161328206,8],[-968994624,9],[607416877,15]], 1546649980
    ],
    [
      [962255677,-762380105,610274894,287954409,-174071320,510854000,209588877,-627021703,929978413,-872247930,-254613561,-695693307,273170072,-129426337,258902041,-989276030,448027560,504198179,112451797,109792351,-322156405,-380712099,707713409,-472416523,728170436,-779134100,446380576,-812550074,-769951228,695511021,424224538,223803204,46344209,-15114572,-694291265,-383187880,-999006547,246881285,-818037168,543668069,668603845,158001964,576972324,120851165,-333849828,631376623,-396777663,-278402403,768654267,-292947840,-254013834,101637354,629916051,-113519946,-979293075,-69520082,-974399764,115721148,768431981,106384285,-593233852,-26727529,-177159837,341435688,-501779315,-77583181,198530612,-274592839,-4670352,-47596640,-103706810,-335160238,-836850602,788886075,336043023,587141203,-314677424,-963669904,90164672,279365649,764238393,889244647,-279030903,-980274141,452706496,-412429358,-359352345,-96367870,949411067],
      [[862501446,82],[130806691,39],[536699542,62],[960461717,30],[-66506845,35],[425475801,57],[-379948987,5],[-79176803,35],[791543774,64],[-896818851,70],[-714762162,70],[724321334,64],[-15419134,21],[-540512804,73],[-645047783,43],[-700555237,26],[884358537,3],[-338556156,88],[-686047305,71],[-968731566,69],[-238605164,32],[655598560,47],[-610222584,49],[443324453,59],[458880521,74],[178848810,9],[945417347,34],[-401726654,13],[492870083,82],[-698352865,45],[717554124,72],[-652972719,15],[774950957,76],[654106114,60],[987022832,42],[572527606,1],[-792322581,80],[74886721,5],[-10650224,78],[855010118,5],[829406390,52],[775843733,59],[136216918,35],[348488334,33],[-549569589,47],[216615365,39],[419335869,72],[678935972,43],[87293041,21],[605212671,41],[837466621,78],[-751548635,49],[268749781,7],[34102526,5],[205187289,39],[137453687,3],[-636914444,29],[-204800253,58],[-894087485,88],[713520819,2],[-643641067,29],[480615375,74],[516137558,32],[-232834387,51],[-845017501,77],[669128166,32],[71898632,15],[-588947881,78],[-428125224,47],[546355741,88],[-113754207,12],[700373809,56],[315929856,74],[-1032453,63],[91744921,23],[290716055,80],[958690681,51],[-46875217,45],[394398244,15],[906926938,48],[632776740,24],[-57761147,68],[-205738629,83],[-199178552,3],[365155321,5],[261708256,71],[-673282328,39],[25956262,84],[510346503,35],[324592030,89],[-222463178,8],[561735826,33],[-197197912,85],[-158885796,55],[108694393,80],[-82191069,68]], 943450757
    ]
  ]

  for i, (robot, factory, expected) in enumerate(test_cases):
    print(f"Running test {i}...")
    for f in [min_distance_memo, min_distance_dp]:
      try:
        tic = time.perf_counter()
        res = f(robot, factory)
        print(
          f"  {f.__name__}: {time.perf_counter() - tic:05f} seconds")
        assert res == expected, f"expected {expected} but got {res}"
      except RecursionError as e:
        print("  {f.__name__} failed with recursion error")


if __name__ == "__main__":
  main()