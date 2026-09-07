{
  "patcher": {
    "fileversion": 1,
    "appversion": {
      "major": 8,
      "minor": 6,
      "revision": 0,
      "architecture": "x64",
      "modernui": 1
    },
    "classnamespace": "box",
    "rect": [
      0,
      0,
      1060,
      820
    ],
    "boxes": [
      {
        "box": {
          "id": "obj-1",
          "maxclass": "comment",
          "patching_rect": [
            30,
            20,
            430,
            20
          ],
          "text": "Max/MSP version: OSC display tester, native Max objects only"
        }
      },
      {
        "box": {
          "id": "obj-40",
          "maxclass": "newobj",
          "patching_rect": [
            55,
            70,
            105,
            22
          ],
          "patcher": {
            "fileversion": 1,
            "appversion": {
              "major": 8,
              "minor": 6,
              "revision": 0,
              "architecture": "x64",
              "modernui": 1
            },
            "classnamespace": "box",
            "rect": [
              0,
              0,
              720,
              760
            ],
            "boxes": [
              {
                "box": {
                  "id": "obj-2",
                  "maxclass": "inlet",
                  "patching_rect": [
                    45,
                    70,
                    30,
                    20
                  ]
                }
              },
              {
                "box": {
                  "id": "obj-3",
                  "maxclass": "inlet",
                  "patching_rect": [
                    610,
                    70,
                    30,
                    20
                  ]
                }
              },
              {
                "box": {
                  "id": "obj-4",
                  "maxclass": "outlet",
                  "patching_rect": [
                    340,
                    700,
                    30,
                    20
                  ]
                }
              },
              {
                "box": {
                  "id": "obj-5",
                  "maxclass": "number",
                  "patching_rect": [
                    340,
                    90,
                    50,
                    22
                  ]
                }
              },
              {
                "box": {
                  "id": "obj-6",
                  "maxclass": "newobj",
                  "patching_rect": [
                    255,
                    130,
                    45,
                    22
                  ],
                  "text": "== 0"
                }
              },
              {
                "box": {
                  "id": "obj-7",
                  "maxclass": "newobj",
                  "patching_rect": [
                    340,
                    130,
                    45,
                    22
                  ],
                  "text": "== 1"
                }
              },
              {
                "box": {
                  "id": "obj-8",
                  "maxclass": "newobj",
                  "patching_rect": [
                    425,
                    130,
                    45,
                    22
                  ],
                  "text": "== 2"
                }
              },
              {
                "box": {
                  "id": "obj-9",
                  "maxclass": "newobj",
                  "patching_rect": [
                    45,
                    115,
                    70,
                    22
                  ],
                  "text": "t f f f"
                }
              },
              {
                "box": {
                  "id": "obj-10",
                  "maxclass": "newobj",
                  "patching_rect": [
                    45,
                    170,
                    70,
                    22
                  ],
                  "text": "gate 1 1"
                }
              },
              {
                "box": {
                  "id": "obj-11",
                  "maxclass": "newobj",
                  "patching_rect": [
                    185,
                    170,
                    70,
                    22
                  ],
                  "text": "gate 1 0"
                }
              },
              {
                "box": {
                  "id": "obj-12",
                  "maxclass": "newobj",
                  "patching_rect": [
                    390,
                    170,
                    70,
                    22
                  ],
                  "text": "gate 1 0"
                }
              },
              {
                "box": {
                  "id": "obj-13",
                  "maxclass": "newobj",
                  "patching_rect": [
                    45,
                    220,
                    55,
                    22
                  ],
                  "text": "> 0.3"
                }
              },
              {
                "box": {
                  "id": "obj-14",
                  "maxclass": "newobj",
                  "patching_rect": [
                    45,
                    260,
                    55,
                    22
                  ],
                  "text": "sel 1"
                }
              },
              {
                "box": {
                  "id": "obj-15",
                  "maxclass": "newobj",
                  "patching_rect": [
                    45,
                    305,
                    45,
                    22
                  ],
                  "text": "i 0"
                }
              },
              {
                "box": {
                  "id": "obj-16",
                  "maxclass": "newobj",
                  "patching_rect": [
                    100,
                    305,
                    45,
                    22
                  ],
                  "text": "+ 1"
                }
              },
              {
                "box": {
                  "id": "obj-17",
                  "maxclass": "newobj",
                  "patching_rect": [
                    45,
                    350,
                    55,
                    22
                  ],
                  "text": ">= 3"
                }
              },
              {
                "box": {
                  "id": "obj-18",
                  "maxclass": "newobj",
                  "patching_rect": [
                    45,
                    390,
                    55,
                    22
                  ],
                  "text": "sel 1"
                }
              },
              {
                "box": {
                  "id": "obj-19",
                  "maxclass": "message",
                  "patching_rect": [
                    45,
                    440,
                    35,
                    22
                  ],
                  "text": "1"
                }
              },
              {
                "box": {
                  "id": "obj-20",
                  "maxclass": "newobj",
                  "patching_rect": [
                    90,
                    440,
                    110,
                    22
                  ],
                  "text": "print is_running"
                }
              },
              {
                "box": {
                  "id": "obj-21",
                  "maxclass": "newobj",
                  "patching_rect": [
                    185,
                    220,
                    55,
                    22
                  ],
                  "text": "t f f"
                }
              },
              {
                "box": {
                  "id": "obj-22",
                  "maxclass": "newobj",
                  "patching_rect": [
                    185,
                    260,
                    65,
                    22
                  ],
                  "text": ">= 1.5"
                }
              },
              {
                "box": {
                  "id": "obj-23",
                  "maxclass": "newobj",
                  "patching_rect": [
                    280,
                    260,
                    55,
                    22
                  ],
                  "text": "== 0"
                }
              },
              {
                "box": {
                  "id": "obj-24",
                  "maxclass": "newobj",
                  "patching_rect": [
                    185,
                    305,
                    55,
                    22
                  ],
                  "text": "sel 1"
                }
              },
              {
                "box": {
                  "id": "obj-25",
                  "maxclass": "newobj",
                  "patching_rect": [
                    280,
                    305,
                    55,
                    22
                  ],
                  "text": "sel 1"
                }
              },
              {
                "box": {
                  "id": "obj-26",
                  "maxclass": "message",
                  "patching_rect": [
                    185,
                    350,
                    35,
                    22
                  ],
                  "text": "2"
                }
              },
              {
                "box": {
                  "id": "obj-27",
                  "maxclass": "message",
                  "patching_rect": [
                    280,
                    350,
                    35,
                    22
                  ],
                  "text": "0"
                }
              },
              {
                "box": {
                  "id": "obj-28",
                  "maxclass": "newobj",
                  "patching_rect": [
                    225,
                    350,
                    90,
                    22
                  ],
                  "text": "print is_sup"
                }
              },
              {
                "box": {
                  "id": "obj-29",
                  "maxclass": "newobj",
                  "patching_rect": [
                    390,
                    220,
                    55,
                    22
                  ],
                  "text": "< 0.8"
                }
              },
              {
                "box": {
                  "id": "obj-30",
                  "maxclass": "newobj",
                  "patching_rect": [
                    390,
                    260,
                    55,
                    22
                  ],
                  "text": "sel 1"
                }
              },
              {
                "box": {
                  "id": "obj-31",
                  "maxclass": "newobj",
                  "patching_rect": [
                    390,
                    305,
                    45,
                    22
                  ],
                  "text": "i 0"
                }
              },
              {
                "box": {
                  "id": "obj-32",
                  "maxclass": "newobj",
                  "patching_rect": [
                    445,
                    305,
                    45,
                    22
                  ],
                  "text": "+ 1"
                }
              },
              {
                "box": {
                  "id": "obj-33",
                  "maxclass": "newobj",
                  "patching_rect": [
                    390,
                    350,
                    55,
                    22
                  ],
                  "text": ">= 3"
                }
              },
              {
                "box": {
                  "id": "obj-34",
                  "maxclass": "newobj",
                  "patching_rect": [
                    390,
                    390,
                    55,
                    22
                  ],
                  "text": "sel 1"
                }
              },
              {
                "box": {
                  "id": "obj-35",
                  "maxclass": "message",
                  "patching_rect": [
                    390,
                    440,
                    35,
                    22
                  ],
                  "text": "1"
                }
              },
              {
                "box": {
                  "id": "obj-36",
                  "maxclass": "newobj",
                  "patching_rect": [
                    435,
                    440,
                    115,
                    22
                  ],
                  "text": "print is_slowing"
                }
              },
              {
                "box": {
                  "id": "obj-37",
                  "maxclass": "message",
                  "patching_rect": [
                    610,
                    120,
                    35,
                    22
                  ],
                  "text": "0"
                }
              },
              {
                "box": {
                  "id": "obj-38",
                  "maxclass": "message",
                  "patching_rect": [
                    570,
                    210,
                    35,
                    22
                  ],
                  "text": "0"
                }
              },
              {
                "box": {
                  "id": "obj-39",
                  "maxclass": "message",
                  "patching_rect": [
                    625,
                    210,
                    35,
                    22
                  ],
                  "text": "0"
                }
              }
            ],
            "lines": [
              {
                "patchline": {
                  "source": [
                    "obj-2",
                    0
                  ],
                  "destination": [
                    "obj-9",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-9",
                    0
                  ],
                  "destination": [
                    "obj-10",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-9",
                    1
                  ],
                  "destination": [
                    "obj-11",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-9",
                    2
                  ],
                  "destination": [
                    "obj-12",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-5",
                    0
                  ],
                  "destination": [
                    "obj-6",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-5",
                    0
                  ],
                  "destination": [
                    "obj-7",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-5",
                    0
                  ],
                  "destination": [
                    "obj-8",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-6",
                    0
                  ],
                  "destination": [
                    "obj-10",
                    1
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-7",
                    0
                  ],
                  "destination": [
                    "obj-11",
                    1
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-8",
                    0
                  ],
                  "destination": [
                    "obj-12",
                    1
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-5",
                    0
                  ],
                  "destination": [
                    "obj-4",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-10",
                    0
                  ],
                  "destination": [
                    "obj-13",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-13",
                    0
                  ],
                  "destination": [
                    "obj-14",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-14",
                    0
                  ],
                  "destination": [
                    "obj-15",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-15",
                    0
                  ],
                  "destination": [
                    "obj-16",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-15",
                    0
                  ],
                  "destination": [
                    "obj-17",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-16",
                    0
                  ],
                  "destination": [
                    "obj-15",
                    1
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-17",
                    0
                  ],
                  "destination": [
                    "obj-18",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-18",
                    0
                  ],
                  "destination": [
                    "obj-19",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-18",
                    0
                  ],
                  "destination": [
                    "obj-20",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-18",
                    0
                  ],
                  "destination": [
                    "obj-38",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-11",
                    0
                  ],
                  "destination": [
                    "obj-21",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-21",
                    0
                  ],
                  "destination": [
                    "obj-22",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-21",
                    1
                  ],
                  "destination": [
                    "obj-23",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-22",
                    0
                  ],
                  "destination": [
                    "obj-24",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-23",
                    0
                  ],
                  "destination": [
                    "obj-25",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-24",
                    0
                  ],
                  "destination": [
                    "obj-26",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-24",
                    0
                  ],
                  "destination": [
                    "obj-28",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-25",
                    0
                  ],
                  "destination": [
                    "obj-27",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-25",
                    0
                  ],
                  "destination": [
                    "obj-38",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-25",
                    0
                  ],
                  "destination": [
                    "obj-39",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-12",
                    0
                  ],
                  "destination": [
                    "obj-29",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-29",
                    0
                  ],
                  "destination": [
                    "obj-30",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-30",
                    0
                  ],
                  "destination": [
                    "obj-31",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-31",
                    0
                  ],
                  "destination": [
                    "obj-32",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-31",
                    0
                  ],
                  "destination": [
                    "obj-33",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-32",
                    0
                  ],
                  "destination": [
                    "obj-31",
                    1
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-33",
                    0
                  ],
                  "destination": [
                    "obj-34",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-34",
                    0
                  ],
                  "destination": [
                    "obj-35",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-34",
                    0
                  ],
                  "destination": [
                    "obj-36",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-34",
                    0
                  ],
                  "destination": [
                    "obj-39",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-19",
                    0
                  ],
                  "destination": [
                    "obj-5",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-26",
                    0
                  ],
                  "destination": [
                    "obj-5",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-27",
                    0
                  ],
                  "destination": [
                    "obj-5",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-35",
                    0
                  ],
                  "destination": [
                    "obj-5",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-37",
                    0
                  ],
                  "destination": [
                    "obj-5",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-3",
                    0
                  ],
                  "destination": [
                    "obj-37",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-3",
                    0
                  ],
                  "destination": [
                    "obj-38",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-3",
                    0
                  ],
                  "destination": [
                    "obj-39",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-38",
                    0
                  ],
                  "destination": [
                    "obj-15",
                    1
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-39",
                    0
                  ],
                  "destination": [
                    "obj-31",
                    1
                  ]
                }
              }
            ]
          },
          "text": "p speed-check"
        }
      },
      {
        "box": {
          "id": "obj-41",
          "maxclass": "newobj",
          "patching_rect": [
            55,
            115,
            80,
            22
          ],
          "text": "print state"
        }
      },
      {
        "box": {
          "id": "obj-42",
          "maxclass": "number",
          "patching_rect": [
            150,
            115,
            55,
            22
          ]
        }
      },
      {
        "box": {
          "id": "obj-43",
          "maxclass": "button",
          "patching_rect": [
            150,
            35,
            24,
            24
          ]
        }
      },
      {
        "box": {
          "id": "obj-44",
          "maxclass": "newobj",
          "patching_rect": [
            310,
            35,
            55,
            22
          ],
          "text": "sel 0"
        }
      },
      {
        "box": {
          "id": "obj-45",
          "maxclass": "newobj",
          "patching_rect": [
            485,
            35,
            55,
            22
          ],
          "text": "sel 1"
        }
      },
      {
        "box": {
          "id": "obj-46",
          "maxclass": "newobj",
          "patching_rect": [
            650,
            35,
            55,
            22
          ],
          "text": "sel 2"
        }
      },
      {
        "box": {
          "id": "obj-47",
          "maxclass": "message",
          "patching_rect": [
            335,
            80,
            50,
            22
          ],
          "text": "start"
        }
      },
      {
        "box": {
          "id": "obj-48",
          "maxclass": "message",
          "patching_rect": [
            410,
            80,
            45,
            22
          ],
          "text": "stop"
        }
      },
      {
        "box": {
          "id": "obj-63",
          "maxclass": "newobj",
          "patching_rect": [
            335,
            120,
            70,
            22
          ],
          "patcher": {
            "fileversion": 1,
            "appversion": {
              "major": 8,
              "minor": 6,
              "revision": 0,
              "architecture": "x64",
              "modernui": 1
            },
            "classnamespace": "box",
            "rect": [
              0,
              0,
              650,
              560
            ],
            "boxes": [
              {
                "box": {
                  "id": "obj-49",
                  "maxclass": "inlet",
                  "patching_rect": [
                    50,
                    35,
                    30,
                    20
                  ]
                }
              },
              {
                "box": {
                  "id": "obj-50",
                  "maxclass": "outlet",
                  "patching_rect": [
                    330,
                    500,
                    30,
                    20
                  ]
                }
              },
              {
                "box": {
                  "id": "obj-51",
                  "maxclass": "newobj",
                  "patching_rect": [
                    50,
                    80,
                    150,
                    22
                  ],
                  "text": "route stop reset start"
                }
              },
              {
                "box": {
                  "id": "obj-52",
                  "maxclass": "message",
                  "patching_rect": [
                    65,
                    125,
                    35,
                    22
                  ],
                  "text": "0"
                }
              },
              {
                "box": {
                  "id": "obj-53",
                  "maxclass": "message",
                  "patching_rect": [
                    120,
                    125,
                    35,
                    22
                  ],
                  "text": "0"
                }
              },
              {
                "box": {
                  "id": "obj-54",
                  "maxclass": "message",
                  "patching_rect": [
                    245,
                    125,
                    35,
                    22
                  ],
                  "text": "1"
                }
              },
              {
                "box": {
                  "id": "obj-55",
                  "maxclass": "toggle",
                  "patching_rect": [
                    245,
                    165,
                    24,
                    24
                  ]
                }
              },
              {
                "box": {
                  "id": "obj-56",
                  "maxclass": "button",
                  "patching_rect": [
                    190,
                    165,
                    24,
                    24
                  ]
                }
              },
              {
                "box": {
                  "id": "obj-57",
                  "maxclass": "newobj",
                  "patching_rect": [
                    190,
                    210,
                    70,
                    22
                  ],
                  "text": "gate 1 1"
                }
              },
              {
                "box": {
                  "id": "obj-58",
                  "maxclass": "message",
                  "patching_rect": [
                    170,
                    255,
                    70,
                    22
                  ],
                  "text": "255 200"
                }
              },
              {
                "box": {
                  "id": "obj-59",
                  "maxclass": "newobj",
                  "patching_rect": [
                    260,
                    255,
                    85,
                    22
                  ],
                  "text": "delay 4000"
                }
              },
              {
                "box": {
                  "id": "obj-60",
                  "maxclass": "message",
                  "patching_rect": [
                    260,
                    305,
                    60,
                    22
                  ],
                  "text": "0 200"
                }
              },
              {
                "box": {
                  "id": "obj-61",
                  "maxclass": "newobj",
                  "patching_rect": [
                    350,
                    305,
                    85,
                    22
                  ],
                  "text": "delay 3000"
                }
              },
              {
                "box": {
                  "id": "obj-62",
                  "maxclass": "newobj",
                  "patching_rect": [
                    235,
                    390,
                    70,
                    22
                  ],
                  "text": "line 50"
                }
              }
            ],
            "lines": [
              {
                "patchline": {
                  "source": [
                    "obj-49",
                    0
                  ],
                  "destination": [
                    "obj-51",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-51",
                    0
                  ],
                  "destination": [
                    "obj-52",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-51",
                    0
                  ],
                  "destination": [
                    "obj-53",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-51",
                    1
                  ],
                  "destination": [
                    "obj-53",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-51",
                    2
                  ],
                  "destination": [
                    "obj-56",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-51",
                    2
                  ],
                  "destination": [
                    "obj-54",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-52",
                    0
                  ],
                  "destination": [
                    "obj-55",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-54",
                    0
                  ],
                  "destination": [
                    "obj-55",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-55",
                    0
                  ],
                  "destination": [
                    "obj-57",
                    1
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-56",
                    0
                  ],
                  "destination": [
                    "obj-57",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-57",
                    0
                  ],
                  "destination": [
                    "obj-58",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-57",
                    0
                  ],
                  "destination": [
                    "obj-59",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-58",
                    0
                  ],
                  "destination": [
                    "obj-62",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-59",
                    0
                  ],
                  "destination": [
                    "obj-60",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-59",
                    0
                  ],
                  "destination": [
                    "obj-61",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-60",
                    0
                  ],
                  "destination": [
                    "obj-62",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-61",
                    0
                  ],
                  "destination": [
                    "obj-57",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-53",
                    0
                  ],
                  "destination": [
                    "obj-62",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-62",
                    0
                  ],
                  "destination": [
                    "obj-50",
                    0
                  ]
                }
              }
            ]
          },
          "text": "p pulse"
        }
      },
      {
        "box": {
          "id": "obj-64",
          "maxclass": "number",
          "patching_rect": [
            335,
            155,
            60,
            22
          ]
        }
      },
      {
        "box": {
          "id": "obj-65",
          "maxclass": "newobj",
          "patching_rect": [
            455,
            220,
            70,
            22
          ],
          "text": "t b f f"
        }
      },
      {
        "box": {
          "id": "obj-66",
          "maxclass": "message",
          "patching_rect": [
            370,
            260,
            100,
            22
          ],
          "text": "/update"
        }
      },
      {
        "box": {
          "id": "obj-67",
          "maxclass": "message",
          "patching_rect": [
            480,
            260,
            160,
            22
          ],
          "text": "/pix 1 $1 $1 $1"
        }
      },
      {
        "box": {
          "id": "obj-68",
          "maxclass": "message",
          "patching_rect": [
            650,
            260,
            160,
            22
          ],
          "text": "/pix 0 $1 $1 $1"
        }
      },
      {
        "box": {
          "id": "obj-69",
          "maxclass": "message",
          "patching_rect": [
            35,
            190,
            95,
            22
          ],
          "text": "/clear"
        }
      },
      {
        "box": {
          "id": "obj-70",
          "maxclass": "message",
          "patching_rect": [
            35,
            235,
            165,
            22
          ],
          "text": "/all 120 120 120"
        }
      },
      {
        "box": {
          "id": "obj-71",
          "maxclass": "message",
          "patching_rect": [
            250,
            385,
            95,
            22
          ],
          "text": "/ping"
        }
      },
      {
        "box": {
          "id": "obj-72",
          "maxclass": "button",
          "patching_rect": [
            245,
            315,
            24,
            24
          ]
        }
      },
      {
        "box": {
          "id": "obj-73",
          "maxclass": "comment",
          "patching_rect": [
            285,
            317,
            90,
            20
          ],
          "text": "reconnect"
        }
      },
      {
        "box": {
          "id": "obj-91",
          "maxclass": "newobj",
          "patching_rect": [
            170,
            385,
            80,
            22
          ],
          "patcher": {
            "fileversion": 1,
            "appversion": {
              "major": 8,
              "minor": 6,
              "revision": 0,
              "architecture": "x64",
              "modernui": 1
            },
            "classnamespace": "box",
            "rect": [
              0,
              0,
              780,
              520
            ],
            "boxes": [
              {
                "box": {
                  "id": "obj-10001",
                  "maxclass": "inlet",
                  "patching_rect": [
                    60,
                    40,
                    30,
                    20
                  ]
                }
              },
              {
                "box": {
                  "id": "obj-10002",
                  "maxclass": "inlet",
                  "patching_rect": [
                    210,
                    40,
                    30,
                    20
                  ]
                }
              },
              {
                "box": {
                  "id": "obj-10003",
                  "maxclass": "newobj",
                  "patching_rect": [
                    210,
                    90,
                    70,
                    22
                  ],
                  "text": "loadbang"
                }
              },
              {
                "box": {
                  "id": "obj-10004",
                  "maxclass": "button",
                  "patching_rect": [
                    300,
                    90,
                    24,
                    24
                  ]
                }
              },
              {
                "box": {
                  "id": "obj-10005",
                  "maxclass": "message",
                  "patching_rect": [
                    210,
                    135,
                    120,
                    22
                  ],
                  "text": "host 127.0.0.1"
                }
              },
              {
                "box": {
                  "id": "obj-10006",
                  "maxclass": "message",
                  "patching_rect": [
                    345,
                    135,
                    80,
                    22
                  ],
                  "text": "port 8010"
                }
              },
              {
                "box": {
                  "id": "obj-10007",
                  "maxclass": "newobj",
                  "patching_rect": [
                    60,
                    210,
                    170,
                    22
                  ],
                  "text": "udpsend 127.0.0.1 8010"
                }
              },
              {
                "box": {
                  "id": "obj-10008",
                  "maxclass": "newobj",
                  "patching_rect": [
                    470,
                    250,
                    120,
                    22
                  ],
                  "text": "udpreceive 8012"
                }
              },
              {
                "box": {
                  "id": "obj-10009",
                  "maxclass": "newobj",
                  "patching_rect": [
                    470,
                    300,
                    95,
                    22
                  ],
                  "text": "route /sensor"
                }
              },
              {
                "box": {
                  "id": "obj-10010",
                  "maxclass": "outlet",
                  "patching_rect": [
                    470,
                    360,
                    30,
                    20
                  ]
                }
              }
            ],
            "lines": [
              {
                "patchline": {
                  "source": [
                    "obj-10001",
                    0
                  ],
                  "destination": [
                    "obj-10007",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-10003",
                    0
                  ],
                  "destination": [
                    "obj-10005",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-10003",
                    0
                  ],
                  "destination": [
                    "obj-10006",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-10002",
                    0
                  ],
                  "destination": [
                    "obj-10004",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-10004",
                    0
                  ],
                  "destination": [
                    "obj-10005",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-10004",
                    0
                  ],
                  "destination": [
                    "obj-10006",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-10005",
                    0
                  ],
                  "destination": [
                    "obj-10007",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-10006",
                    0
                  ],
                  "destination": [
                    "obj-10007",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-10008",
                    0
                  ],
                  "destination": [
                    "obj-10009",
                    0
                  ]
                }
              },
              {
                "patchline": {
                  "source": [
                    "obj-10009",
                    0
                  ],
                  "destination": [
                    "obj-10010",
                    0
                  ]
                }
              }
            ]
          },
          "text": "p display"
        }
      },
      {
        "box": {
          "id": "obj-92",
          "maxclass": "newobj",
          "patching_rect": [
            170,
            450,
            65,
            22
          ],
          "text": "route 1"
        }
      },
      {
        "box": {
          "id": "obj-93",
          "maxclass": "flonum",
          "patching_rect": [
            175,
            500,
            70,
            22
          ]
        }
      },
      {
        "box": {
          "id": "obj-94",
          "maxclass": "button",
          "patching_rect": [
            135,
            500,
            24,
            24
          ]
        }
      },
      {
        "box": {
          "id": "obj-95",
          "maxclass": "comment",
          "patching_rect": [
            250,
            500,
            120,
            20
          ],
          "text": "vitesse capteur"
        }
      },
      {
        "box": {
          "id": "obj-96",
          "maxclass": "message",
          "patching_rect": [
            485,
            130,
            45,
            22
          ],
          "text": "255"
        }
      },
      {
        "box": {
          "id": "obj-97",
          "maxclass": "message",
          "patching_rect": [
            650,
            105,
            45,
            22
          ],
          "text": "100"
        }
      },
      {
        "box": {
          "id": "obj-98",
          "maxclass": "newobj",
          "patching_rect": [
            485,
            80,
            55,
            22
          ],
          "text": "t b b"
        }
      },
      {
        "box": {
          "id": "obj-99",
          "maxclass": "comment",
          "patching_rect": [
            410,
            455,
            430,
            20
          ],
          "text": "lancer Terminal et copier/coller la ligne suivante + ENTER"
        }
      },
      {
        "box": {
          "id": "obj-100",
          "maxclass": "comment",
          "patching_rect": [
            430,
            480,
            390,
            20
          ],
          "text": "cliquer reconnect si message: udp send: not connected"
        }
      },
      {
        "box": {
          "id": "obj-101",
          "maxclass": "comment",
          "patching_rect": [
            420,
            560,
            560,
            40
          ],
          "text": "python3 \"/Users/retake7/Documents/WORK-LAPTOP/SOLAR DEVICE/TECH/PROGRAMMATION/SolarDevice/DisplayController/main.py\" /dev/cu.usbmodem112201"
        }
      }
    ],
    "lines": [
      {
        "patchline": {
          "source": [
            "obj-40",
            0
          ],
          "destination": [
            "obj-41",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-40",
            0
          ],
          "destination": [
            "obj-42",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-40",
            0
          ],
          "destination": [
            "obj-44",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-40",
            0
          ],
          "destination": [
            "obj-45",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-40",
            0
          ],
          "destination": [
            "obj-46",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-43",
            0
          ],
          "destination": [
            "obj-40",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-44",
            0
          ],
          "destination": [
            "obj-47",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-44",
            0
          ],
          "destination": [
            "obj-48",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-47",
            0
          ],
          "destination": [
            "obj-63",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-48",
            0
          ],
          "destination": [
            "obj-63",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-63",
            0
          ],
          "destination": [
            "obj-64",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-63",
            0
          ],
          "destination": [
            "obj-65",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-65",
            0
          ],
          "destination": [
            "obj-66",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-65",
            1
          ],
          "destination": [
            "obj-67",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-65",
            2
          ],
          "destination": [
            "obj-68",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-66",
            0
          ],
          "destination": [
            "obj-91",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-67",
            0
          ],
          "destination": [
            "obj-91",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-68",
            0
          ],
          "destination": [
            "obj-91",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-69",
            0
          ],
          "destination": [
            "obj-91",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-70",
            0
          ],
          "destination": [
            "obj-91",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-71",
            0
          ],
          "destination": [
            "obj-91",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-72",
            0
          ],
          "destination": [
            "obj-91",
            1
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-91",
            0
          ],
          "destination": [
            "obj-92",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-92",
            0
          ],
          "destination": [
            "obj-93",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-92",
            0
          ],
          "destination": [
            "obj-94",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-93",
            0
          ],
          "destination": [
            "obj-40",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-45",
            0
          ],
          "destination": [
            "obj-98",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-98",
            0
          ],
          "destination": [
            "obj-96",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-98",
            1
          ],
          "destination": [
            "obj-48",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-96",
            0
          ],
          "destination": [
            "obj-65",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-46",
            0
          ],
          "destination": [
            "obj-97",
            0
          ]
        }
      },
      {
        "patchline": {
          "source": [
            "obj-97",
            0
          ],
          "destination": [
            "obj-65",
            0
          ]
        }
      }
    ]
  }
}