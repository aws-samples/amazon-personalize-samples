# Amazon Personalize 샘플

Amazon Personalize의 다양한 기능을 온보딩하고 사용하는 방법에 대한 노트북 및 예제

## Amazon Personalize 시작하기

[getting_started/](getting_started/) 폴더에는 Amazon Personalize를 사용하여 첫 번째 캠페인을 구축하는 데 필요한 모든 리소스를 배포할 CloudFormation 템플릿이 포함되어 있습니다.

제공된 노트북은 사용자가 고유한 데이터로 직접 모델을 구축하기 위한 템플릿으로 활용할 수도 있습니다. 이 리포지토리는 환경에 복제되므로 이 방법으로 보다 발전한 형태의 노트북을 살펴볼 수도 있습니다.

## Amazon Personalize 다음 단계

[next_steps/](next_steps/) 폴더에는 Amazon Personalize 여정에서 다음과 같은 일반적인 단계를 보여주는 자세한 예가 포함되어 있습니다. 이 폴더에는 다음과 같은 고급 콘텐츠가 포함되어 있습니다.

* 핵심 사용 사례
  - [사용자 개인화](next_steps/core_use_cases/user_personalization)
  - [개인별 순위](next_steps/core_use_cases/personalized_ranking)
  - [관련 항목](next_steps/core_use_cases/related_items)
  - [배치 추천](next_steps/core_use_cases/batch_recommendations)
  - [사용자 세분화](next_steps/core_use_cases/user_segmentation)

* Amazon Personalize 배포 환경의 확장 가능한 작업 예제
    - [기계 학습을 사용하여 개인화된 경험 유지](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)
        - 이 AWS 솔루션을 사용하면 데이터 세트 가져오기, 솔루션 및 솔루션 버전 생성, 캠페인 생성 및 업데이트, 필터 생성, 배치 추론 작업 실행 등, 전체 프로세스를 자동화할 수 있습니다. 이러한 프로세스는 온디맨드로 실행하거나, 사용자가 정의한 스케줄에 따라 트리거할 수 있습니다.
    - [MLOps Step Function](next_steps/operations/ml_ops)(레거시)
        - 이 프로젝트는 AWS Step Functions를 사용하여 Personalize 캠페인을 완전 자동화된 방식으로 신속하게 구축하는 방법을 보여줍니다. 시작하려면 [ml_ops](next_steps/operations/ml_ops) 폴더로 이동하여 README 지침을 따릅니다. 이 예제는 [기계 학습을 사용하여 개인화된 경험 유지](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/) 솔루션으로 대체되었습니다.
    - [MLOps Data Science SDK](next_steps/operations/ml_ops_ds_sdk)
        - 이 프로젝트는 AWS Data Science SDK를 사용하여 Personalize 캠페인을 완전 자동화된 방식으로 신속하게 구축하는 방법을 보여줍니다. 시작하려면 [ml_ops_ds_sdk](next_steps/operations/ml_ops_ds_sdk) 폴더로 이동하여 README 지침을 따릅니다.
    - [개인화 API](https://github.com/aws-samples/personalization-apis)
        - Amazon Personalize 같은 추천 시스템과 애플리케이션 사이에서 작동하며 대기 시간이 짧은 실시간 API 프레임워크입니다. 응답 캐싱, API Gateway 구성, [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html)를 사용한 A/B 테스트, 추론-시간 항목 메타데이터, 자동 상황별 추천 등의 구현 모범 사례를 제공합니다.
    - [Lambda 예제](next_steps/operations/lambda_examples)
        - 이 폴더는 S3에서 전송된 새 데이터를 처리하는 Lambda 함수를 사용하여 `put_events`를 Personalize 캠페인에 통합하는 기본 예제로 시작합니다. 시작하려면 [lambda_examples](next_steps/operations/lambda_examples) 폴더로 이동하여 README 지침을 따릅니다.
    - [Personalize 모니터](https://github.com/aws-samples/amazon-personalize-monitor)
        - 이 프로젝트는 AWS 환경 전반에 Amazon Personalize를 실행하기 위한 모니터링, 알림, 대시보드 및 최적화 도구를 추가합니다.
    - [스트리밍 이벤트](next_steps/operations/streaming_events)
        - 이 프로젝트는 Amazon Personalize 캠페인과 이벤트 트래커 엔드포인트의 전면에 API 계층을 신속하게 배포하는 방법을 보여줍니다. 시작하려면 [streaming_events](operations/streaming_events/) 폴더로 이동하여 README 지침을 따릅니다.
    - [필터 교체](next_steps/operations/filter_rotator)
        - 이 서버리스 애플리케이션에는 스케줄에 따라 실행되며. 시간 경과에 따라 변경되어야 하는 고정 값의 표현식을 사용하여 Personalize 필터를 교체하는 AWS Lambda 함수가 포함되어 있습니다. 예를 들어 연속된 시간대를 기준으로 항목을 포함/제외하도록 설계된 날짜 또는 시간 값을 기반으로 범위 연산자를 사용합니다.

* 워크숍
    - [Workshops/](next_steps/workshops/) 폴더에는 다양한 최신 워크숍이 들어 있습니다.
        - [POC in a Box](next_steps/workshops/POC_in_a_box)
        - [re:Invent 2019](next_steps/workshops/Reinvent_2019)
        - [Immersion Day](next_steps/workshops/Immersion_Day)
    - [파트너 통합](https://github.com/aws-samples/retail-demo-store#partner-integrations)
        - Amplitude, Braze, Optimizely, Segment 등의 파트너 솔루션과 함께 Personalize를 사용하는 방법을 보여주는 워크숍을 살펴보세요.

* 데이터 과학 도구
    - [data_science/](next_steps/data_science/) 폴더에는 입력 데이터 세트의 주요 속성을 시각화하는 방법을 보여주는 예제가 포함되어 있습니다.
        - 누락된 데이터, 중복된 이벤트 및 반복되는 항목 소비
        - 범주형 필드의 멱승법 분포
        - 콜드 스타트 적용을 위한 시간축성 드리프트 분석
        - 사용자 세션 분포에 대한 분석

* 데모/참조 아키텍처
    - [소매 데모 스토어](https://github.com/aws-samples/retail-demo-store)
        - Amazon Personalize를 사용하여 개인화된 옴니채널 고객 경험을 제공하는 방법을 보여주는 샘플 소매 웹 애플리케이션 및 워크숍 플랫폼입니다.

## 라이선스 요약

이 샘플 코드는 수정된 MIT 라이선스에 따라 사용할 수 있습니다. LICENSE 파일을 참조하세요.
