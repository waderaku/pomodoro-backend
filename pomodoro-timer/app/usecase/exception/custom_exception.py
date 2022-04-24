class AdditionalNegativeValueException(Exception):
    """追加する値が負の値であった場合の整合性エラー"""

    def __init__(self):
        super().__init__("endはstart以降の時間を設定してください")


class NoExistTaskException(Exception):
    """対象のタスクが存在しない場合の例外"""

    def __init__(self):
        super().__init__("対象のタスクが存在しません")


class AlreadyExistUserException(Exception):
    """既に対象のユーザーが存在する場合の例外"""

    def __init__(self):
        super().__init__("当該ユーザーは既に存在します")
