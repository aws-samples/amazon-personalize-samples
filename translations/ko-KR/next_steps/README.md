# Amazon Personalize 다음 단계

Amazon Personalize의 다양한 기능을 온보딩하고 사용하는 방법에 대한 노트북 및 예제

## Amazon Personalize 사용 사례 예제

[core_use_cases/](core_use_cases/) 폴더에는 가장 일반적인 사용 사례의 자세한 예가 포함되어 있습니다.

## Amazon Personalize 배포 환경의 확장 가능한 작업 예제

[operations/](operations/) 폴더에는 다음 주제와 관련한 예제가 포함되어 있습니다.

* [기계 학습을 사용하여 개인화된 경험 유지](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)
    - 이 AWS 솔루션을 사용하면 데이터 세트 가져오기, 솔루션 및 솔루션 버전 생성, 캠페인 생성 및 업데이트, 필터 생성, 배치 추론 작업 실행 등, 전체 프로세스를 자동화할 수 있습니다. 이러한 프로세스는 온디맨드로 실행하거나, 사용자가 정의한 스케줄에 따라 트리거할 수 있습니다.

* MLOps(레거시)
    - 이 프로젝트는 AWS Step Functions를 사용하여 Personalize 캠페인을 완전 자동화된 방식으로 신속하게 구축하는 방법을 보여줍니다. 시작하려면 [ml_ops](operations/ml_ops/) 폴더로 이동하여 README 지침을 따릅니다. 이 예제는 [기계 학습을 사용하여 개인화된 경험 유지](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/) 솔루션으로 대체되었습니다.

* MLOps Data Science SDK
    - 이 프로젝트는 AWS Data Science SDK를 사용하여 Personalize 캠페인을 완전 자동화된 방식으로 신속하게 구축하는 방법을 보여줍니다. 시작하려면 [ml_ops_ds_sdk](operations/ml_ops_ds_sdk/) 폴더로 이동하여 README 지침을 따릅니다.

* [개인화 API](https://github.com/aws-samples/personalization-apis)
    - Amazon Personalize 같은 추천 시스템과 애플리케이션 사이에서 작동하며 대기 시간이 짧은 실시간 API 프레임워크입니다. 응답 캐싱, API Gateway 구성, [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html)를 사용한 A/B 테스트, 추론-시간 항목 메타데이터, 자동 상황별 추천 등의 구현 모범 사례를 제공합니다.

* 스트리밍 이벤트
    - 이 프로젝트는 Amazon Personalize 캠페인과 이벤트 트래커 엔드포인트의 전면에 API 계층을 신속하게 배포하는 방법을 보여줍니다. 시작하려면 [streaming_events](operations/streaming_events/) 폴더로 이동하여 README 지침을 따릅니다.

* Lambda 예제
    - 이 폴더는 S3에서 전송된 새 데이터를 처리하는 Lambda 함수를 사용하여 `put_events`를 Personalize 캠페인에 통합하는 기본 예제로 시작합니다. 시작하려면 [lambda_examples](operations/lambda_examples/) 폴더로 이동하여 README 지침을 따릅니다.

* 필터 교체
    - 이 [서버리스 애플리케이션](operations/filter_rotator/)에는 스케줄에 따라 실행되며. 시간 경과에 따라 변경되어야 하는 고정 값의 표현식을 사용하여 Personalize 필터를 교체하는 AWS Lambda 함수가 포함되어 있습니다. 예를 들어 연속된 시간대를 기준으로 항목을 포함/제외하도록 설계된 날짜 또는 시간 값을 기반으로 범위 연산자를 사용합니다.

* [Personalize 모니터](https://github.com/aws-samples/amazon-personalize-monitor)
    - 이 프로젝트는 AWS 환경 전반에 Amazon Personalize를 실행하기 위한 모니터링, 알림, 대시보드 및 최적화 도구를 추가합니다.

## 참조 아키텍처

다음 참조 아키텍처는 여러 업종에 걸쳐 Amazon Personalize를 적용하는 방법을 보여주는 예제를 제공합니다.

* 소매 - [소매 데모 스토어](https://github.com/aws-samples/retail-demo-store)는 웹 애플리케이션, 메시징 및 대화 AI 인터페이스에서 Personalize를 사용하여 개인화를 구현하는 풀 스택 웹 애플리케이션입니다. 실습 워크숍도 제공됩니다.
* 미디어 및 엔터테인먼트
* 여행 및 숙박

## 워크숍

[workshops/](workshops/) 폴더에는 다양한 최신 워크숍이 들어 있습니다.

* POC in a Box
* re:Invent 2019

## 데이터 과학 도구

[data_science/](data_science/) 폴더에는 입력 데이터 세트의 주요 속성을 시각화하는 방법을 보여주는 예제가 포함되어 있습니다.

살펴봐야 할 주요 구성 요소는 다음과 같습니다.
- 누락된 데이터, 중복된 이벤트 및 반복되는 항목 소비
- 범주형 필드의 멱승법 분포
- 콜드 스타트 적용을 위한 시간축성 드리프트 분석
- 사용자 세션 분포에 대한 분석

## 라이선스 요약

이 샘플 코드는 수정된 MIT 라이선스에 따라 사용할 수 있습니다. LICENSE 파일을 참조하세요.
