import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import psycopg2
# Import required modules
import os
import sys

current_dir = os.getcwd()
# Append the parent directory to sys.path
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# ignore warrnings
import warnings
from database.database_connection import get_db_connection, insert_dataframe_to_db, insert_detection_data

class TestDatabaseOperations(unittest.TestCase):

    @patch("database_operations.psycopg2.connect")
    def test_get_db_connection_success(self, mock_connect):
        """Test successful database connection."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn = get_db_connection()
        self.assertIsNotNone(conn)
        mock_connect.assert_called_once()

    @patch("database_operations.psycopg2.connect", side_effect=psycopg2.OperationalError)
    def test_get_db_connection_failure(self, mock_connect):
        """Test database connection failure."""
        with self.assertRaises(psycopg2.OperationalError):
            get_db_connection()

    @patch("database_operations.get_db_connection")
    def test_insert_dataframe_to_db(self, mock_get_db_connection):
        """Test inserting data into telegram_data table."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        data = {
            "message_id": ["1", "2"],
            "date": ["2024-02-01 12:00:00", "2024-02-01 12:05:00"],
            "sender": ["User1", "User2"],
            "channel": ["Channel1", "Channel2"],
            "text": ["Hello", "World"]
        }
        df = pd.DataFrame(data)

        insert_dataframe_to_db(df)

        self.assertEqual(mock_cursor.execute.call_count, 2)
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("database_operations.get_db_connection")
    def test_insert_detection_data(self, mock_get_db_connection):
        """Test inserting detection results into detection_results table."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        data = {
            "image_name": ["img1.jpg", "img2.jpg"],
            "confidence_score": [0.95, 0.87],
            "class_name": ["person", "dog"],
            "bbox_coordinates": ["[50, 60, 100, 120]", "[30, 40, 80, 90]"],
            "result_image_path": ["path1", "path2"],
            "detection_time": ["2024-02-01 12:10:00", "2024-02-01 12:15:00"]
        }
        df = pd.DataFrame(data)

        insert_detection_data(df)

        self.assertEqual(mock_cursor.execute.call_count, 2)
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()
