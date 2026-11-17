

## 실행 방법

저장소 루트에서 성적 CSV 파일을 읽으려면 다음 명령을 실행합니다.

```powershell
python load_scores.py scores.csv
```

파일 경로를 생략하면 현재 폴더의 `scores.csv`를 읽습니다. 유효한 성적과
건너뛴 행 및 사유를 출력합니다.

## 테스트 방법

테스트를 실행하려면 `pytest`를 설치한 뒤 저장소 루트에서 실행합니다.

```powershell
python -m pip install pytest
python -m pytest -q
```
