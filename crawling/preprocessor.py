import pandas as pd
from datetime import datetime
import re


class Preprocessor:
    def __init__(self, file):
        if not file.endswith('.csv'):
            raise AttributeError("잘못된 형식의 파일")
        self.df = pd.read_csv(file)
        self.processed = None

    def extract_rows_by_keyword_contains(self, keyword, target_column, ignore_case_sensitive=False):
        if ignore_case_sensitive:
            keyword = keyword.lower()
            self.processed = self.df[self.df[target_column].str.lower().str.contains(keyword)]
            return self.processed
        self.processed = self.df[self.df[target_column].str.contains(keyword)]
        return self.processed

    def extract_rows_by_keyword_exactly(self, keyword, target_column, ignore_case_sensitive=False):
        if ignore_case_sensitive:
            keyword = keyword.lower()
            self.processed = self.df[
                self.df[target_column].apply(lambda x: keyword in x.lower().split())
            ]
            return self.processed
        self.processed = self.df[
                self.df[target_column].apply(lambda x: keyword in x.split())
            ]
        return self.processed

    def preprocessed_to_csv(self, file_name=None):
        if self.processed is None:
            raise AttributeError("처리판 데이터프레임이 없음")
        if file_name is None:
            self.processed.to_csv(f"processed_at_{datetime.now()}.csv", index=False)
            return
        self.processed.to_csv(f"{file_name}.csv", index=False)
