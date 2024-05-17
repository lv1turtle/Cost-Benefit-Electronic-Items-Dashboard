import pandas as pd
from datetime import datetime
import re


class Preprocessor:
    """
    생성자로 받은 csv파일을 키워드를 통해 행을 필터링한 후, 데이터프레임으로 반환 및 csv로 저장하는 클래스
    """
    def __init__(self, file):
        """
        csv파일만 생성자로 받음
        :param file:
        """
        if not file.endswith('.csv'):
            raise AttributeError("잘못된 형식의 파일")
        self.df = pd.read_csv(file)
        self.processed = None

    def extract_rows_by_keyword_contains(self, keyword, target_column, ignore_case_sensitive=False):
        """
        해당하는 keyword가 target_column 값 내에 포함되어있으면,
        해당 행을 제외시킴.
        행이 제외된 데이터 프레임은 반환됨
        :param keyword: 필터링할 키워드
        :param target_column: 키워드를 통해 필터링될 대상 컬럼
        :param ignore_case_sensitive: 대소문자 무시 여부
        :return: 필터링된 데이터 프레임
        """
        if ignore_case_sensitive:
            keyword = keyword.lower()
            self.processed = self.df[self.df[target_column].str.lower().str.contains(keyword)]
            return self.processed
        self.processed = self.df[self.df[target_column].str.contains(keyword)]
        return self.processed

    def extract_rows_by_keyword_exactly(self, keyword, target_column, ignore_case_sensitive=False):
        """
        해당하는 keyword가 target_column 값의 단어들 중 일치하면,
        해당 행을 제외시킴.
        행이 제외된 데이터 프레임은 반환됨
        :param keyword: 필터링할 키워드
        :param target_column: 키워드를 통해 필터링될 대상 컬럼
        :param ignore_case_sensitive: 대소문자 무시 여부
        :return: 필터링된 데이터 프레임
        """
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
        """
        처리한 데이터 프레임을 csv파일로 저장
        :param file_name: 저장될 파일의 이름, 없을 시 "processed_at_{저장시간}.csv" 로 저장
        :return:
        """
        if self.processed is None:
            raise AttributeError("처리판 데이터프레임이 없음")
        if file_name is None:
            self.processed.to_csv(f"processed_at_{datetime.now()}.csv", index=False)
            return
        self.processed.to_csv(f"{file_name}.csv", index=False)
