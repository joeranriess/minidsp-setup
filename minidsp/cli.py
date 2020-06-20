# This one is the CLI code written by mfeif.
# I don' use it in my setup, but I wanted to keep it so
#you can test initially on the commany line

"""command line access to the board"""

import argparse

from minidsp.board_2x4hd import Board2x4HD

# I removed gain and config from here, because I don't want to casually
# muck with those and possibly damage my speakers. Others may want them back.
#
# I also removed dirac stuff, because I don't have one and can't test it.

controls = [
    # read only ones...
    "status",
    "levels",
    "muted",
    # ones that do one thing...
    "mute",
    "unmute",
    # ones that always do one thing and can take an argument...
    "volume_up",
    "volume_down",
    # ones that can either return current state or change it
    "volume",
    "source",
]


def main():
    # argparse setup
    parser = argparse.ArgumentParser(
        description="Send commands to a MiniDSP 2x4 HD board"
    )
    parser.add_argument("control", type=str, help="Control (" + ", ".join(controls) + ")")
    parser.add_argument(
        "value", type=str, nargs="?", help="Value to set, if an action is to be 'set'"
    )
    args = parser.parse_args()

    board = Board2x4HD()

    # read-only things:
    if args.control == "status":
        print("Status:", board.status)
    elif args.control == "levels":
        print("Playing Levels are {}".format(board.levels))
    elif args.control == "muted":
        print("Muted" if board.muted else "Unmuted")

    # do-one-thing things
    elif args.control == "mute":
        board.mute()
        print("Muted")
    elif args.control == "unmute":
        board.unmute()
        print("Unmuted")

    # can take a value or not
    elif args.control in ("volume_up", "volume_down"):
        if args.value:
            try:
                notches = int(args.value)
            except ValueError:
                parser.error(
                    "Volume change must be provided as an integer representing notches"
                )
        else:
            notches = 1
        if args.control == "volume_up":
            board.volume_up(notches)
        elif args.control == "volume_down":
            board.volume_down(notches)
        print("New volume: {} dB".format(board.volume))

    # ones that can either return current state or change it
    elif args.control == "volume":
        if args.value:
            try:
                vol_float = float(args.value)
            except ValueError:
                parser.error(
                    "Volume must be provided in db and without units ('-127.5' to '0')"
                )
            board._set_volume(vol_float)
        print("Volume: {} dB".format(board.volume))
    elif args.control == "source":
        if args.value:
            if args.value in ("usb", "analog", "toslink"):
                board._set_source(args.value)
            else:
                parser.error("invalid source name")
        print(board.source)


if __name__ == "__main__":
    main()
