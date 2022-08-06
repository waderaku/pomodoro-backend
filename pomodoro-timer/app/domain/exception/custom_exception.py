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


class DeleteRootTaskException(Exception):
    """削除対象のタスクがrootタスクである場合の例外"""

    def __init__(self):
        super().__init__("rootタスクは削除できません")


class UpdateRootTaskException(Exception):
    """更新対象のタスクがrootタスクである場合の例外"""

    def __init__(self):
        super().__init__("rootタスクは更新できません")


class PasswordIsInvalidException(Exception):
    """パスワードが入力規定を満たしていない場合の例外"""

    def __init__(self):
        super().__init__("パスワードは大文字小文字を含んだ英数字8文字以上24文字以内で入力してください")


class MissMatchPasswordException(Exception):
    """ユーザIDとパスワードがマッチしなかった場合の例外"""

    def __init__(self):
        super().__init__("パスワードが異なります")


class NoExistTokenException(Exception):
    """対象のトークンがDBに存在しなかった場合の例外"""

    def __init__(self):
        super().__init__("当該トークンは存在しません")


class ExpiredTokenException(Exception):
    """対象のトークンが有効期限切れの場合の例外"""

    def __init__(self):
        super().__init__("当該トークンは有効期限切れです")
