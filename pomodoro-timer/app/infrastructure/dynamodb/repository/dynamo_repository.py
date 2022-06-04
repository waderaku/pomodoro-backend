from app.infrastructure.dynamodb.util.get_table import get_pomodoro_table


class DynamoRepository:
    """DynamoDBへアクセスするリポジトリ全般で行われる共通処理をまとめたクラス"""

    def __init__(self):
        """Repositoryのコンストラクタ.
        pomodoro-infoテーブルオブジェクトを生成する
        """
        self._table = get_pomodoro_table()
