# Personalize POC 가이드

Amazon Personalize는 추천/개인화 모델을 효과적으로 빠르게 구축하고 확장할 수 있는 기계 학습 서비스입니다. 아래의 콘텐츠는 특정 사용 사례에 맞는 첫 번째 모델을 구축하는 데 도움이 되도록 제작되었으며, 데이터가 아직 Amazon Personalize에 사용하기에 적합한 형식이 아니라고 가정합니다.

이 리포지토리에서는 서비스에 대한 기본 지식이 있는 것으로 간주하므로, 아직 익숙하지 않은 경우 아래의 시작하기 자료를 참조하는 것이 좋습니다.

## Amazon Personalize 소개

Amazon Personalize에 익숙하지 않은 경우 다음 페이지에서 이 도구에 대해 자세히 알아볼 수 있습니다.

* [제품 페이지](https://aws.amazon.com/personalize/)
* [GitHub 샘플 노트북](https://github.com/aws-samples/amazon-personalize-samples)
* [제품 문서](https://docs.aws.amazon.com/personalize/latest/dg/what-is-personalize.html)

## 목표 

이 POC를 완료하면 다음 스킬을 습득할 수 있습니다.

1. 데이터 세트를 Amazon Personalize에 매핑하는 방법
1. 사용 사례에 적합한 모델 또는 레시피 선택
1. 프로그래밍 방식으로 모델을 구축하는 방법
1. 모델 지표를 해석하는 방법
1. 모델을 프로그래밍 방식으로 배포하는 방법
1. Personalize에서 결과를 얻는 방법

## 완료된 예

노트북은 사용하기 전에 모든 출력을 없앤 상태지만, 이 프로세스의 완료된 예를 보려면 `completed` 폴더에서 노트북을 찾아보세요.


## 프로세스:

1. 작업 환경 배포[아래 참조]
1. 사용자-항목-상호 작용 데이터 검증 및 가져오기 -
`01_Validating_and_Importing_User_Item_Interaction_Data.ipynb`
1. 항목-메타데이터 검증 및 가져오기 -
`02_Validating_and_Importing_Item_Metadata.ipynb`
1. 첫 번째 솔루션 생성 및 평가 -
`03_Creating_and_Evaluating_Solutions.ipynb`
1. 캠페인 및 필터 배포 -
`04_Deploying_Campaigns_and_Filters.ipynb`
1. 캠페인 및 필터 배포 -
`05_Interacting_with_Campaigns_and_Filters.ipynb`
1. AWS 계정의 리소스 정리 - `06_Clean_Up_Resources.ipynb`

이는 이 프로세스의 일반적인 순서를 보여주지만, 이 프로세스를 지원을 제공하는 2일 온사이트 POC로 운영하는 경우, 현장에 도착하기 전에 최소한 사용자-항목-상호 작용 및 항목-메타데이터 데이터를 가져오는 것이 좋습니다.


## 작업 환경 배포

위에서 언급한 바와 같이, 첫 단계는 초기 설정 작업의 대부분을 수행할 CloudFormation 템플릿을 배포하는 것입니다. 다른 브라우저 창이나 탭에서 AWS 계정에 로그인합니다. 그런 다음, 아래 링크를 새 탭에서 열고 CloudFormation을 통해 필요한 항목을 배포하는 프로세스를 시작합니다.

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=PersonalizePOC&templateURL=https://chriskingpartnershare.s3.amazonaws.com/PersonalizePOC.yaml)

스택을 배포하는 방법을 잘 모르겠으면, 아래의 스크린샷을 따르세요.

### CloudFormation 마법사

다음과 같이 하단에서 `Next`를 클릭하여 시작합니다.

![StackWizard](static/imgs/img1.png)

이 페이지에는 다음과 같은 몇 가지 작업이 있습니다.

1. 스택 이름을 다음과 같이 연관성이 있는 이름으로 변경합니다.`PersonalizePOC`
1. 노트북 이름 변경(선택 사항)
1. SageMaker EBS 볼륨의 볼륨 크기를 변경합니다. 기본값은 10GB입니다. 데이터 세트가 더 클 것으로 예상되면 그에 따라 볼륨 크기를 늘리세요.


작업을 마쳤으면 하단에서 `Next`를 클릭합니다.

![StackWizard2](static/imgs/img2.png)

이 페이지는 조금 길기 때문에 아래까지 스크롤하여 `Next`를 클릭하세요. 모든 기본값을 사용해도 POC를 충분히 완료할 수 있지만, 사용자 지정 요구 사항이 있는 경우 필요에 따라 변경합니다.

![StackWizard3](static/imgs/img3.png)


다시 하단으로 스크롤하고 템플릿을 사용하여 새 IAM 리소스를 생성할 수 있도록 확인란을 선택한 다음 `Create Stack`을 클릭합니다.

![StackWizard4](static/imgs/img4.png)

몇 분 동안 CloudFormation이 자동으로 위에서 설명하는 리소스를 생성합니다. 프로비저닝하는 동안 다음과 같이 표시됩니다.

![StackWizard5](static/imgs/img5.png)

이 작업이 완료되면 다음과 같은 녹색 텍스트가 나타나 작업이 완료되었음을 나타냅니다.

![StackWizard5](static/imgs/img6.png)

이제 환경이 생성되었으므로, 콘솔 상단의 `Services`를 클릭한 다음 `SageMaker`를 검색하고 해당 서비스를 클릭하여 SageMaker의 서비스 페이지로 이동합니다.


![StackWizard5](static/imgs/img7.png)

SageMaker 콘솔에서 현재 여러 노트북을 사용 중임을 나타내는 녹색 상자가 나타날 때까지 스크롤한 다음 그 상자를 클릭합니다.

![StackWizard5](static/imgs/img8.png)

이 페이지에는 실행 중인 SageMaker 노트북 목록이 표시됩니다. 새로 생성한 Personalize POC 노트북의 `Open JupyterLab` 링크를 클릭합니다.

![StackWizard5](static/imgs/img9.png)

이렇게 하면 POC를 위한 Jupyter 환경이 열립니다. Jupyter 환경이 익숙하지 않은 경우, 웹 기반 데이터 과학 IDE라고 생각하면 됩니다. `PersonalizePOC` 폴더가 자동으로 열립니다. 이 폴더가 열리지 않으면 화면 왼쪽의 브라우저에서 폴더 아이콘을 클릭하고 아래의 설명서에 따라 POC를 시작하세요.

## 사용자-항목-상호 작용 데이터 검증 및 가져오기

Amazon Personalize에서 지원되는 모든 알고리즘의 핵심 데이터는 사용자-항목-상호 작용 데이터입니다. 이 노트북은 이 데이터를 식별하고, 서비스에 맞게 데이터를 포맷하고, 스키마를 정의하고, 마지막으로 데이터를 가져오는 프로세스를 안내합니다.

`01_Validating_and_Importing_User_Item_Interaction_Data.ipynb`를 열고 거기서부터 진행합니다.

이 작업을 완료했으면 메타데이터 가져오기로 넘어갑니다.

## 항목-메타데이터 검증 및 가져오기

Amazon Personalize에는 메타데이터 없이 결과를 제공할 수 있는 몇 가지 알고리즘이 있습니다. 하지만 데이터 세트에 따라, 사용자 개인화 및 HRNN-메타데이터 알고리즘이 유용한 리소스가 될 수 있습니다.

`02_Validating_and_Importing_Item_Metadata.ipynb`를 열고 거기서부터 진행합니다.

이 작업을 완료하고 나면, 첫 번째 솔루션을 만들고 평가할 수 있습니다.

이는 사용자에 대한 프로세스와 유사하며, 두 데이터 유형 중 하나를 지원하는 알고리즘은 사용자 개인화 및 HRNN-메타데이터뿐입니다.

## 첫 번째 솔루션 생성 및 평가

Amazon Personalize에는 솔루션이라는 개념이 있습니다. 솔루션은 서비스에 제공한 데이터를 기반으로 훈련된 모델입니다. 모든 모델은 비공개이며 계정 간 또는 데이터 세트 그룹 간에도 데이터가 공유되지 않습니다. 이 노트북은 다음을 위한 솔루션을 구축하는 등의 모델 훈련 프로세스를 안내합니다.

* HRNN
* SIMS
* 개인별 순위

이러한 각각의 알고리즘이나 레시피가 서로 매우 상이한 문제를 해결한다는 것을 알 수 있습니다. 여기서 목표는 비교적 단순한 데이터 세트에서 수많은 문제를 해결하는 것들을 만들어내는 방법을 보여주는 것입니다.

이러한 솔루션을 구축하고 결과를 보려면 `03_Creating_and_Evaluating_Solutions.ipynb`를 열고 지시를 따르세요.

### 캠페인 및 필터 배포

일련의 훈련된 솔루션을 구축한 후에는 다음 단계로서 솔루션을 배포해야 합니다. 이는 내부적으로 이루어집니다.`04_Deploying_Campaigns_and_Filters.ipynb`

여기서 배울 내용은 다음과 같습니다.
1. 배포 및 용량 계획 수립
1. 항목 및 이벤트 필터를 생성하는 방법


### Personalize와 상호 작용하는 방법

일련의 훈련된 솔루션을 구축한 후에는 다음 단계로서 솔루션을 배포해야 합니다. 이는 `05_Interacting_with_Campaigns_and_Filters.ipynb`에서 내부적으로 이루어집니다. 여기서 배울 내용은 다음과 같습니다.

1. 배포된 솔루션과 상호 작용하는 방법(다양한 접근 방식)
1. 실시간 상호 작용
1. 캠페인에 필터 사용
1. 배치 내보내기


### 다음 단계

이러한 노트북을 따라 진행하다 보면, 고객을 위한 잘 작동하는 일련의 모델이 만들어집니다. 이제 고객이 현재 목표(전환, 클릭 등)와 비교하여 AB 테스트를 수행하기 위해 사용하는 방법을 활용한 후, 이러한 모델에 트래픽을 전송하고 지표를 모니터링하기 시작합니다. 시간이 지남에 따라 이 솔루션은 신뢰도가 높아지고 대규모 프로덕션 환경으로 전환할 수 있게 됩니다.

AB 테스트에 대한 추가 콘텐츠도 곧 제공될 예정입니다.

### 정리

POC가 끝났나요? 이들 노트북을 따라 진행하는 동안 AWS 계정에 생성된 모든 리소스를 삭제하려면 `06_Clean_Up_Resources.ipynb` 노트북을 참조하세요. 이 노트북은 계정에 배포된 모든 Personalize 리소스를 찾는 데 도움을 주고, 해당 리소스를 삭제하는 방법을 보여줍니다.