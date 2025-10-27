Hello! This is some info of the program:

It is around 90% based on python, and 10% of json. To make your own levels for the game, go to levels and either add a new json file or modify the current ones, and use this json structure for each wave/level:

{
  "waves": [
    [
      {"type": "tank", "count": 25},
      {"type": "basic", "count": 35},
      {"type": "fast", "count": 45},
      {"reward": "200"}
    ],
    [
      {"type": "tank", "count": 50},
      {"type": "basic", "count": 40},
      {"type": "fast", "count": 64},
      {"reward": "400"}
    ]
  ]
}


To make your own exe of the game, run build.bat. The output is in output folder.

The game is like 50% coded by AI (except for classes/configs/ideas/jsons/docs/bat files/paths/level_select/utils/.gitignore).

Maybe have fun playing the game? In its current form (1.1.0 when writing this) its a basic tower defense game.