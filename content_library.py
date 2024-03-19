game_content_library = {
    "start": {
        "description": "You wake up in a forest, surrounded by towering trees and the sound of distant wildlife.",
        "choices": {
            "move left": "path",
            "move right": "river"
        }
    },
    "path": {
        "description": "You find a path leading to a mysterious cave.",
        "choices": {
            "enter cave": "cave",
            "return": "start"
        }
    },
    "river": {
        "description": "You stumble upon a river with clear water. Across it, you see a quaint village.",
        "choices": {
            "cross river": "village",
            "return": "start"
        }
    },
    "cave": {
        "description": "Inside the cave, you find ancient ruins, possibly hinting at a lost civilization.",
        "choices": {
            "explore ruins": "end",
            "return": "path"
        }
    },
    "village": {
        "description": "The village is peaceful, with villagers going about their day. A market bustles with activity.",
        "choices": {
            "visit market": "end",
            "return": "river"
        }
    },
    "end": {
        "description": "Your journey has come to an end, but countless more await.",
        "choices": {}
    }
}
