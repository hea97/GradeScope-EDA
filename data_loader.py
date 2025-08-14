import pandas as pd

def load_data(file_path):
    df = pd.read_csv(file_path)
    # 데이터 전처리 (결측치 처리, 자료형 변환 등)
    return df