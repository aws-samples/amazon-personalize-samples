**이 예제는 [기계 학습을 사용하여 개인화된 경험 유지](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/) 예제로 대체되었습니다.** **이 솔루션을 사용하면 데이터 세트 가져오기, 솔루션 및 솔루션 버전 생성, 캠페인 생성 및 업데이트, 필터 생성, 배치 추론 작업 실행 등, 전체 프로세스를 자동화할 수 있습니다.** **이러한 프로세스는 온디맨드로 실행하거나, 사용자가 정의한 스케줄에 따라 트리거할 수 있습니다.**

# 시작하기

MLOps가 큰 인기를 얻고 있습니다. 이 예제는 자동화 파이프라인을 구성하는 데 사용할 수 있는 핵심 요소를 보여줍니다. 다음 아키텍처 다이어그램에서 보듯이 Amazon S3, Amazon Personalize 및 Amazon SNS API를 호출하는 AWS Lambda 함수를 포함한 AWS Step Function 워크플로를 배포하게 됩니다.

이 패키지에는 **Amazon Personalize** 내에서 다음을 비롯한 여러 작업을 수행할 수 있는 Step Functions 파이프라인의 소스 코드가 포함되어 있습니다.

- 데이터 세트 그룹 생성
- 데이터 세트 생성 및 가져오기
- 솔루션 생성
- 솔루션 버전 생성
- 캠페인 생성

단계가 완료되면, Step Functions가 SNS 주제를 사용하여
 완료되었음을 사용자에게 알립니다.

아래의 다이어그램에서는 솔루션의 아키텍처를 설명합니다.

![Architecture Diagram](images/architecture.png)

아래의 다이어그램은 Step Function 워크플로 정의를 보여줍니다.

![stepfunction definition](images/stepfunctions.png)

## 사전 요구 사항

### AWS SAM 설치

AWS Serverless Application Model(SAM)은 서버리스 애플리케이션을 구축하기 위한 오픈 소스 프레임워크로, 함수, API, 데이터베이스 및 이벤트 소스 매핑을 나타내는 단축 구문을 제공합니다. 리소스 하나당 코드 몇 줄로 원하는 애플리케이션을 정의하고 YAML을 사용하여 모델링할 수 있습니다. 배포 중에 SAM은 SAM 구문을 AWS CloudFormation 구문으로 변환 및 확장하여 서버리스 애플리케이션을 더 빨리 구축할 수 있도록 합니다.

[AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)를 **설치**합니다. 
그러면 프로젝트를 빌드하고, 배포하고. 로컬로 테스트하는 데 필요한 도구가 설치됩니다. 이 예에서는 빌드하고 배포하는 데에만 AWS SAM을 사용합니다. 자세한 내용은 [설명서](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)를 참조하세요.

## 빌드 및 배포

프로젝트를 배포하려면 다음 명령을 실행해야 합니다.

1. Amazon Personalize 샘플 리포지토리 복제
    - `git clone https://github.com/aws-samples/amazon-personalize-samples.git`
2. next_steps/operations/ml_ops/personalize-step-functions 디렉터리로 이동합니다.
    - `cd next_steps/operations/ml_ops/personalize-step-functions`
3. SAM 프로젝트를 빌드합니다. [설치 지침](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
    - `sam build`
4. 프로젝트를 배포합니다. SAM은 안내에 따라 배포할 수 있는 배포 옵션을 제공합니다. 알림을 받으려면 이메일 주소를 파라미터로 제공해야 합니다.
    - `sam deploy --guided`
5. 이메일 받은 편지함으로 이동하여 SNS 주제를 구독하고 있는지 확인합니다.

이 파이프라인에서는 파라미터 파일의 기본 이름과 이메일을 묻습니다.

배포가 완료되면 CloudFormation 스택 출력에서 확인할 수 있는 **InputBucket**이 생성됩니다. 이 버킷을 사용하여 다음 구조로 데이터 세트를
업로드할 수 있습니다.

```bash
Users/              # Users dataset(s) folder
Items/              # Items dataset(s) folder
Interactions/       # Interaction dataset(s) folder
```

데이터 세트가 제출되고 나면 **루트 디렉터리**에 파라미터 파일을 업로드합니다. 이 단계를 수행하면
 Step Functions 워크플로가 시작됩니다.

## 구성

이 배포를 사용하려면 **파라미터 파일**을 올바르게 설정해야 합니다. 파라미터 파일에는
Amazon Personalize에서 리소스를 생성하는 데 필요한 모든 정보가 들어 있습니다. [boto3 personalize 클라이언트](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/personalize.html)를
사용하여 파라미터를 가져옵니다.

이 파일에는 다음 섹션이 포함되어야 하며, **모두 필수**입니다.
- `datasetGroup`
- `datasets`
- `solution`
- `campaign`

<details><summary>파라미터 파일의 샘플 참조</summary>
<p>

```json
{
    "datasetGroup": {
        "name":"DatasetGroup"
    },
    "datasets": {
        "Interactions": {
            "name":"InteractionsDataset",
            "schema": {
              "type": "record",
              "name": "Interactions",
              "namespace": "com.amazonaws.personalize.schema",
              "fields": [
                {
                  "name": "USER_ID",
                  "type": "string"
                },
                {
                  "name": "ITEM_ID",
                  "type": "string"
                },
                {
                  "name": "TIMESTAMP",
                  "type": "long"
                }
              ],
              "version": "1.0"
            }
        },
        "Users": {
            "name": "UsersDataset",
                "schema": {
                "type": "record",
                "name": "Users",
                "namespace": "com.amazonaws.personalize.schema",
                "fields": [
                    {
                        "name": "USER_ID",
                        "type": "string"
                    },
                    {
                        "name": "GENDER",
                        "type": "string",
                        "categorical": true
                    },
                    {
                        "name": "AGE",
                        "type": "int"
                    }
                ],
                "version": "1.0"
            }
        }
    },
    "solution": {
        "name": "Solution",
        "performAutoML": true
    },
    "campaign": {
        "name": "Campaign",
        "minProvisionedTPS": 1
    }
}
```
</p>
</details>

### 파라미터 파일 구조

파라미터 파일을 만드는 방법은 [이 예제](./example/params.json)를 참조하세요. 
각 섹션은 특정 API 호출에 해당합니다.

### 스키마를 정의하는 방법

https://docs.aws.amazon.com/personalize/latest/dg/how-it-works-dataset-schema.html


## 테스트 예제

배포를 테스트하려면 **ml_ops 폴더** 내에서 다음 명령을 실행합니다.


```bash
aws s3 sync ./example/data s3://{YOURBUCKETNAME}

aws s3 cp ./example/params.json s3://{YOURBUCKETNAME}
```

그러면 Step Functions 워크플로의 실행이 시작됩니다. 실행 과정을 추적하려면
AWS 콘솔의 Step Functions 섹션으로 이동하여 **DeployStateMachine-xxx** 상태 시스템을 클릭합니다.

> 이전에 만든 올바른 S3 버킷 이름을 지정해야 합니다. 파라미터 파일이
> S3 버킷에 제출되면 상태 시스템이 시작됩니다.

## 다음 단계

축하합니다! Personalize 모델을 훈련하고 캠페인을 만들었습니다. 캠페인 ARN을 활용하거나, [Amazon Personalize 콘솔](https://console.aws.amazon.com/personalize/home?region=us-east-1#datasetGroups) 데이터 세트 그룹 캠페인 섹션을 방문하여 추천을 받을 수 있습니다.

추천을 받는 방법에 대한 자세한 내용은 [설명서](https://docs.aws.amazon.com/personalize/latest/dg/getting-recommendations.html) 또는 [노트북 예제](https://github.com/aws-samples/amazon-personalize-samples/blob/master/personalize_sample_notebook.ipynb) 안내서를 참조하세요.
