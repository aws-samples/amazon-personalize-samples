오프라인 성능 평가
===

기록 데이터가 있는데, Personalize가 해당 데이터를 기반으로 할 때 얼마나 훌륭한 성능을 발휘하는지 평가하고자 합니다. 이를 위해 저희가 제안하는 방법은 다음과 같습니다.

1. 임시로 데이터를 '과거' 훈련 세트와 '미래' 테스트 세트로 분할합니다.
2. '과거' 데이터를 Amazon Personalize에 업로드하고 솔루션을 훈련하고 캠페인을 배포합니다.
3. 캠페인을 사용하여 모든 사용자를 위한 추천을 얻고 '미래' 테스트 세트와 비교합니다.

위에서 설명한 단계를 완료하는 예는 [personalize_temporal_holdout.ipynb](personalize_temporal_holdout.ipynb/)입니다. 기본 인기 기반 추천을 포함했는데, 그보다 훨씬 나은 성능을 보일 것입니다. 해당 추천은 온전성 검사용입니다. 일반적인 다음 단계로서, 훈련 및 테스트 분할을 그대로 유지하되, 보다 세부적인 오프라인 비교를 위해 서로 다른 모델을 훈련해 보세요.

## 라이선스 요약

이 샘플 코드는 수정된 MIT 라이선스에 따라 사용할 수 있습니다. LICENSE 파일을 참조하세요.