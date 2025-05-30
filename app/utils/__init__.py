import logging
import inspect
import os
from flask import current_app

def get_logger(name=None):
    """
    統一ロガーを取得する関数
    Laravel風のログ機能を提供
    """
    if name is None:
        # 呼び出し元のモジュール名を取得
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get('__name__', __name__)
    
    logger = logging.getLogger(name)
    
    # current_appが利用可能な場合は、アプリのログ設定を使用
    try:
        if current_app:
            # アプリのハンドラーをコピー
            for handler in current_app.logger.handlers:
                if handler not in logger.handlers:
                    logger.addHandler(handler)
            logger.setLevel(current_app.logger.level)
    except RuntimeError:
        # アプリコンテキスト外の場合は基本設定
        pass
    
    return logger

def _log_with_caller(level, message, **kwargs):
    """正しい呼び出し元情報でログを出力する内部関数"""
    # 呼び出し元の情報を取得
    frame = inspect.currentframe().f_back.f_back  # 2つ上のフレーム
    module_name = frame.f_globals.get('__name__', __name__)
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    func_name = frame.f_code.co_name
    
    # モジュール名からロガーを作成
    logger = logging.getLogger(module_name)
    
    # アプリのハンドラーを設定
    try:
        if current_app:
            for handler in current_app.logger.handlers:
                if handler not in logger.handlers:
                    logger.addHandler(handler)
            logger.setLevel(current_app.logger.level)
    except RuntimeError:
        pass
    
    if kwargs:
        message = f"{message} - {kwargs}"
    
    # 正しい呼び出し元情報でLogRecordを作成
    if logger.isEnabledFor(level):
        record = logger.makeRecord(
            logger.name, level, filename, lineno,
            message, (), None, func_name
        )
        logger.handle(record)

def log_info(message, **kwargs):
    """情報ログ"""
    _log_with_caller(logging.INFO, message, **kwargs)

def log_error(message, **kwargs):
    """エラーログ"""
    _log_with_caller(logging.ERROR, message, **kwargs)

def log_warning(message, **kwargs):
    """警告ログ"""
    _log_with_caller(logging.WARNING, message, **kwargs)

def log_debug(message, **kwargs):
    """デバッグログ"""
    _log_with_caller(logging.DEBUG, message, **kwargs) 