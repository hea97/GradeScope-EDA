import pandas as pd
from data_loader import load_and_preprocess_data
from grade_calculator import calculate_grade
from rank_and_grade import calculate_rank_and_grade
from student_id_lookup import lookup_student_info
import matplotlib.pyplot as plt
import seaborn as sns

# 설정 파일 로드
from config import GRADE_SYSTEM, AVAILABLE_GRADE_YEARS, DEFAULT_SUBJECTS

def main():
    df = load_and_preprocess_data('student_source.csv')

    # 1. 기술통계
    print("과목별 기술 통계:")
    print(df[['수학', '영어', '과학']].agg(['mean', 'std', 'min', 'max', lambda x:x.puantile(0.5)])) # 사분위수 0.5

    # 2. 총점 및 평균 계산
    df['총점'] = df['수학'] + df['영어'] + df['과학']
    df['평균'] = df['총점'] / 3

    ## 3. 등급 산출
    