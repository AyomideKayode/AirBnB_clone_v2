#!usr/bin/python3

import unittest
from unittest.mock import patch
from io import StringIO
from models import storage
from console import HBNBCommand


class TestConsoleMethods(unittest.TestCase):

    def setUp(self):
        self.console = HBNBCommand()

    def tearDown(self):
        del self.console


    def test_create(self):
        """ Test create command
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_create("BaseModel")
            output = fake_out.getvalue().strip()
            self.assertTrue(output != "")

    def test_show(self):
        """ Test show command
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_show("BaseModel 1234")
            output = fake_out.getvalue().strip()
            self.assertTrue("** no instance found **" in output)

    def test_destroy(self):
        """ Test destroy command
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_destroy("BaseModel 1234")
            output = fake_out.getvalue().strip()
            self.assertTrue("** no instance found **" in output)

    def test_all(self):
        """ Test all command
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_all("BaseModel")
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "[]")
            # Will add more assertions based on expected output

    def test_count(self):
        """ Test count command
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_count("BaseModel")
            output = fake_out.getvalue().strip()
            self.assertEqual(output, "0")
            # Will add more assertions based on expected output

    def test_update(self):
        """ Test update command
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_update("BaseModel 1234 name \"John Doe\"")
            output = fake_out.getvalue().strip()
            self.assertTrue("** no instance found **" in output)
            # Will add more assertions based on expected output

    # Will add more tests for other commands and edge cases as needed


class TestConsoleCreate(unittest.TestCase):

    def setUp(self):
        """Set up the HBNBCommand instance"""
        self.console = HBNBCommand()
        storage.reload()

    def tearDown(self):
        """Clean up resources"""
        del self.console

    @patch('sys.stdout', new_callable=StringIO)
    def test_create(self, mock_stdout):
        """Test create command with valid parameters"""
        self.console.onecmd(
            "create Place name=\"My_House\" number_rooms=3")
        obj_id = mock_stdout.getvalue().strip()
        expected_output = "My House"
        self.assertIn(expected_output, str(
            storage.all()["Place." + obj_id]))

    @patch('sys.stdout', new_callable=StringIO)
    def test_create_invalid_class(self, mock_stdout):
        """Test create command with an invalid class"""
        self.console.onecmd(
            "create InvalidClass name=\"My_House\" number_rooms=3")
        expected_output = "** class doesn't exist **"
        self.assertIn(expected_output, mock_stdout.getvalue().strip())

    # Will add more test cases for different scenarios


if __name__ == "__main__":
    unittest.main()
