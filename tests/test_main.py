import unittest
from unittest.mock import patch
from main import backup_mysql, restore_mysql, backup_postgres, restore_postgres, backup_mongo, restore_mongo

class TestBackupRestore(unittest.TestCase):

    @patch('os.system')
    def test_backup_mysql(self, mock_system):
        backup_mysql()
        mock_system.assert_called_once_with(
            "docker exec -i $(docker-compose ps -q mysql) mysqldump -uroot -prootpassword mydb > mysql_backup.sql"
        )

    @patch('os.system')
    def test_restore_mysql(self, mock_system):
        restore_mysql()
        mock_system.assert_called_once_with(
            "docker exec -i $(docker-compose ps -q mysql) mysql -uroot -prootpassword mydb < mysql_backup.sql"
        )

    @patch('os.system')
    def test_backup_postgres(self, mock_system):
        backup_postgres()
        mock_system.assert_called_once_with(
            "docker exec -i $(docker-compose ps -q postgres) pg_dump -Uadmin -d mydb > postgres_backup.sql"
        )

    @patch('os.system')
    def test_restore_postgres(self, mock_system):
        restore_postgres()
        mock_system.assert_called_once_with(
            "docker exec -i $(docker-compose ps -q postgres) psql -Uadmin -d mydb < postgres_backup.sql"
        )

    @patch('os.system')
    def test_backup_mongo(self, mock_system):
        backup_mongo()
        mock_system.assert_called_once_with(
            "docker exec -i $(docker-compose ps -q mongodb) mongodump --archive=mongo_backup.archive"
        )

    @patch('os.system')
    def test_restore_mongo(self, mock_system):
        restore_mongo()
        mock_system.assert_called_once_with(
            "docker exec -i $(docker-compose ps -q mongodb) mongorestore --archive=mongo_backup.archive"
        )

if __name__ == '__main__':
    unittest.main()

import unittest
from src.sample import add  # Adjust the import based on your project structure

class TestSample(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()
