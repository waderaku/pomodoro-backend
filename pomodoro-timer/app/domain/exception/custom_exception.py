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


class NoExistUserException(Exception):
    """対象のユーザーが存在しない場合の例外"""

    def __init__(self):
        super().__init__("当該ユーザーは存在しません")


class NotSettingConfigException(Exception):
    """カレンダーやタスクリストの指定がない状態でGoogleとリンクしようとしている場合の例外"""

    def __init__(self):
        super().__init__("config設定がないためGoogleとリンクさせることは出来ません")


class NoExistParentTaskException(Exception):
    """対象の親タスクが存在しない場合の例外"""

    def __init__(self):
        super().__init__("対象の親タスクが存在しません")


class AlreadyDoneParentTaskException(Exception):
    """対象の親タスクが既に完了していた場合の例外"""

    def __init__(self):
        super().__init__("親タスクがすでに完了しています")


class NotShortcutTaskException(Exception):
    """対象のタスクがrootの直下のタスクだった時にshortcutタスクではない場合の例外"""

    def __init__(self):
        super().__init__("ショートカットフラグが設定されていません")
