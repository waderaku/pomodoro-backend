from test.db_util import clear_and_insert
from typing import Tuple


def initial_process(test_data: dict) -> Tuple[dict, dict]:
    """テストデータを分解し、DBの更新及びリクエスト・期待結果を取得して返却する

    Args:
        test_data (dict): 今回のテストケースのデータ

    Returns:
        リクエストデータおよび期待結果
    """
    request = test_data["request"]
    answer = test_data["answer"]
    db_data = test_data["db"]
    clear_and_insert(db_data)
    return request, answer
