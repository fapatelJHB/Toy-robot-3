import unittest
import io
from io import StringIO
from unittest.mock import patch
import sys
from test_base import captured_io
from test_base import run_unittests
import robot


class Testrobot(unittest.TestCase):

    def test_get_command(self):
        self.assertEqual("OFF".lower(),"off")
        self.assertEqual("HELP".lower(),"help")
        self.assertEqual("FORWARD".lower(),"forward")
        self.assertEqual("BACK".lower(),"back")
        self.assertEqual("RIGHT".lower(),"right")
        self.assertEqual("LEFT".lower(),"left")
        self.assertEqual("SPRINT".lower(),"sprint")
        self.assertEqual("REPLAY".lower(),"replay")
        self.assertEqual("REPLAY SILENT".lower(),"replay silent")
        self.assertEqual("REPLAY REVERSED".lower(),"replay reversed")
        self.assertEqual("REPLAY REVERSED SILENT".lower(),"replay reversed silent")

    def test_get_robot_name(self):
        with captured_io(StringIO("HAL\n")):
            self.assertEqual(robot.get_robot_name(),"HAL")

    # # @patch("sys.stdin", StringIO("''\nHAL"))
    # def test_get_robot_name(self):
    #     """
    #         This function checks if the user input is correct.
    #     """ 
    #     with captured_io(StringIO("''\nHAL")):
    #     # sys.stdout = StringIO()
    #         self.assertEqual(robot.get_robot_name(),"HAL")

    def test_do_help(self):
            with captured_io(StringIO("")):
               self.assertEqual(robot.do_help(),(True,"""I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
REPLAY - replays the commands
REPLAY SILENT -  replays the commands silently.
REPLAY REVERSED - replay the commands in reverse order.
REPLAY REVERSED SILENT - replays commans in reverse silently.
"""))
    def test_split_command_input(self):
        with captured_io(StringIO("")):
            self.assertEqual(robot.split_command_input("forward 10"),("forward", "10"))
            self.assertEqual(robot.split_command_input("back 5"),("back", "5"))
            self.assertEqual(robot.split_command_input("right"),("right", ""))
            self.assertEqual(robot.split_command_input("left"),("left", ""))
            self.assertEqual(robot.split_command_input("sprint"),("sprint", ""))
            self.assertEqual(robot.split_command_input("replay"),("replay", ""))
            self.assertEqual(robot.split_command_input("replay silent"),("replay", "silent"))
            self.assertEqual(robot.split_command_input("replay reversed"),("replay", "reversed"))
            self.assertEqual(robot.split_command_input("replay reversed silent"),("replay", "reversed silent"))


    def test_valid_command(self):
        with captured_io(StringIO("")):
            self.assertEqual(robot.valid_command("off"), True)
            self.assertEqual(robot.valid_command("help"), True)
            self.assertEqual(robot.valid_command("forward 10"), True)
            self.assertEqual(robot.valid_command("back 5"), True)
            self.assertEqual(robot.valid_command("right"), True)
            self.assertEqual(robot.valid_command("left"), True)
            self.assertEqual(robot.valid_command("sprint"), True)
            self.assertEqual(robot.valid_command("replay"), True)
            self.assertEqual(robot.valid_command("replay silent"), True)
            self.assertEqual(robot.valid_command("replay reversed"), True)
            self.assertEqual(robot.valid_command("replay reversed silent"), True)
            self.assertEqual(robot.valid_command("hello"), False)

    def test_do_forward(self):
        with captured_io(StringIO("forward 5\n")):
            self.assertEqual(robot.do_forward("HAL", 5), (True, " > HAL moved forward by 5 steps."))

    def test_do_back(self):
        with captured_io(StringIO("back 7\n")):
            self.assertEqual(robot.do_back("HAL", 7), (True," > HAL moved back by 7 steps."))

    def test_do_right_turn(self):
        with captured_io(StringIO("right\n")):
            self.assertEqual(robot.do_right_turn("HAL"), (True, " > HAL turned right."))
        
    def test_do_left_turn(self):
        with captured_io(StringIO("left\n")):
            self.assertEqual(robot.do_left_turn("HAL"), (True," > HAL turned left."))

    @patch ("sys.stdin", StringIO("HAL\nsprint 3\noff\n"))
    def test_do_sprint(self):
        sys.stdout = StringIO()
        robot.robot_start()
        self.assertEqual(sys.stdout.getvalue(),"""What do you want to name your robot? HAL: Hello kiddo!
HAL: What must I do next?  > HAL moved forward by 3 steps.
 > HAL moved forward by 2 steps.
 > HAL moved forward by 1 steps.
 > HAL now at position (0,6).
HAL: What must I do next? HAL: Shutting down..
""")

    @patch ("sys.stdin", StringIO("HAL\nforward 10\nreplay\noff\n"))
    def test_do_replay(self):
        sys.stdout = StringIO()
        robot.robot_start()
        self.assertEqual(sys.stdout.getvalue(),"""What do you want to name your robot? HAL: Hello kiddo!
HAL: What must I do next?  > HAL moved forward by 10 steps.
 > HAL now at position (0,10).
HAL: What must I do next?  > HAL moved forward by 10 steps.
 > HAL now at position (0,20).
 > HAL replayed 1 commands.
 > HAL now at position (0,20).
HAL: What must I do next? HAL: Shutting down..
""")

    
    @patch("sys.stdin", StringIO("HAL\nforward 3\nback 1\nreplay silent\noff\n"))
    def test_do_replay(self):
        sys.stdout = StringIO()
        robot.robot_start()
        self.assertEqual(sys.stdout.getvalue(),"""What do you want to name your robot? HAL: Hello kiddo!
HAL: What must I do next?  > HAL moved forward by 3 steps.
 > HAL now at position (0,3).
HAL: What must I do next?  > HAL moved back by 1 steps.
 > HAL now at position (0,2).
HAL: What must I do next?  > HAL replayed 2 commands silently.
 > HAL now at position (0,4).
HAL: What must I do next? HAL: Shutting down..
""")

    @patch("sys.stdin", StringIO("HAL\nforward 6\nback 2\nreplay reversed\noff\n"))
    def test_do_replay(self):
        sys.stdout = StringIO()
        robot.robot_start()
        self.assertEqual(sys.stdout.getvalue(),"""What do you want to name your robot? HAL: Hello kiddo!
HAL: What must I do next?  > HAL moved forward by 6 steps.
 > HAL now at position (0,6).
HAL: What must I do next?  > HAL moved back by 2 steps.
 > HAL now at position (0,4).
HAL: What must I do next?  > HAL moved back by 2 steps.
 > HAL now at position (0,2).
 > HAL moved forward by 6 steps.
 > HAL now at position (0,8).
 > HAL replayed 2 commands in reverse.
 > HAL now at position (0,8).
HAL: What must I do next? HAL: Shutting down..
""")

    @patch("sys.stdin", StringIO("HAL\nforward 5\nback 2\nreplay reversed silent\noff\n"))
    def test_do_replay(self):
        sys.stdout = StringIO()
        robot.robot_start()
        self.assertEqual(sys.stdout.getvalue(),"""What do you want to name your robot? HAL: Hello kiddo!
HAL: What must I do next?  > HAL moved forward by 5 steps.
 > HAL now at position (0,5).
HAL: What must I do next?  > HAL moved back by 2 steps.
 > HAL now at position (0,3).
HAL: What must I do next?  > HAL replayed 2 commands in reverse silently.
 > HAL now at position (0,6).
HAL: What must I do next? HAL: Shutting down..
""")

    @patch("sys.stdin", StringIO("HAL\nforward 3\nforward 6\nback 2\nright\nreplay 3\noff\n"))
    def test_do_replay(self):
        sys.stdout = StringIO()
        robot.robot_start()
        self.assertEqual(sys.stdout.getvalue(),"""What do you want to name your robot? HAL: Hello kiddo!
HAL: What must I do next?  > HAL moved forward by 3 steps.
 > HAL now at position (0,3).
HAL: What must I do next?  > HAL moved forward by 6 steps.
 > HAL now at position (0,9).
HAL: What must I do next?  > HAL moved back by 2 steps.
 > HAL now at position (0,7).
HAL: What must I do next?  > HAL turned right.
 > HAL now at position (0,7).
HAL: What must I do next?  > HAL moved forward by 6 steps.
 > HAL now at position (6,7).
 > HAL moved back by 2 steps.
 > HAL now at position (4,7).
 > HAL turned right.
 > HAL now at position (4,7).
 > HAL replayed 3 commands.
 > HAL now at position (4,7).
HAL: What must I do next? HAL: Shutting down..
""")

    @patch("sys.stdin", StringIO("HAL\nforward 3\nforward 6\nback 2\nright\nreplay 3-1\noff\n"))
    def test_do_replay(self):
        sys.stdout = StringIO()
        robot.robot_start()
        self.assertEqual(sys.stdout.getvalue(),"""What do you want to name your robot? HAL: Hello kiddo!
HAL: What must I do next?  > HAL moved forward by 3 steps.
 > HAL now at position (0,3).
HAL: What must I do next?  > HAL moved forward by 6 steps.
 > HAL now at position (0,9).
HAL: What must I do next?  > HAL moved back by 2 steps.
 > HAL now at position (0,7).
HAL: What must I do next?  > HAL turned right.
 > HAL now at position (0,7).
HAL: What must I do next?  > HAL moved forward by 6 steps.
 > HAL now at position (6,7).
 > HAL moved back by 2 steps.
 > HAL now at position (4,7).
 > HAL replayed 2 commands.
 > HAL now at position (4,7).
HAL: What must I do next? HAL: Shutting down..
""")



if __name__ == "__main__":
    unittest.main()