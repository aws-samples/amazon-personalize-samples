# 시작하기

이 튜토리얼에서는 Amazon Personalize를 사용하는 방법을 설명합니다.

1. 작업 환경 구축합(아래의 단계 참조)
2. VOD 및 전자 상거래에 최적화된 첫 번째 사용 사례 추천 시스템 구축
3. 첫 번째 사용자 지정 데이터 세트, 모델 및 추천 캠페인 구축

## 환경 사전 요구 사항

이 콘텐츠는 CloudFormation 템플릿을 사용하여 배포하는 경우에만 적용됩니다. 그 외의 경우에는 특정 작업에 필요한 IAM 권한을 참조하세요.

1. AWS 계정
2. AWS 계정에 대한 관리자 권한이 있는 사용자

## 환경 구축

첫 단계는 초기 설정 작업의 대부분을 수행할 CloudFormation 템플릿을 배포하는 것입니다. 다른 브라우저 창에서 AWS 계정에 로그인합니다. 그런 다음, 아래 링크를 새 탭에서 열고 CloudFormation을 통해 필요한 항목을 배포하는 프로세스를 시작합니다.

[![Launch Stack](https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=PersonalizeDemo&templateURL=https://amazon-personalize-github-samples.s3.amazonaws.com/PersonalizeDemo.yaml)

이 단계를 잘 모르겠으면, 스크린샷을 따르세요.

<details>
  <summary>지침을 펼쳐 보려면 클릭하세요.</summary>
  
### CloudFormation 마법사

아래 나와 있는 것처럼 다음(`Next`)을 클릭하여 시작합니다. ![StackWizard](static/imgs/img1.png)

다음 페이지에서는 파일 스토리지에 고유한 S3 버킷 이름을 지정해야 합니다. 아래에 나와 있는 기본 옵션의 끝에 사용자의 이름과 성을 추가하는 것이 좋습니다. 업데이트한 후 다음(`Next`)을 다시 클릭합니다. ![StackWizard2](static/imgs/img3.png)

이 페이지는 조금 길기 때문에 아래까지 스크롤하여 다음(`Next`)을 클릭하세요. ![StackWizard3](static/imgs/img4.png)

다시 하단으로 스크롤하고 템플릿을 사용하여 새 IAM 리소스를 생성할 수 있도록 확인란을 선택한 다음 스택 생성(`Create Stack`)을 클릭합니다. ![StackWizard4](static/imgs/img5.png)

몇 분 동안 CloudFormation이 자동으로 위에서 설명하는 리소스를 생성합니다. 프로비저닝하는 동안 다음과 같이 표시됩니다. ![StackWizard5](static/imgs/img6.png)

이 작업이 완료되면 다음과 같은 녹색 텍스트가 나타나 작업이 완료되었음을 나타냅니다. ![StackWizard5](static/imgs/img7.png)

이제 환경을 만들었으므로 나중에 사용할 수 있도록 S3 버킷의 이름을 저장해야 합니다. S3 버킷의 이름은 출력(`Outputs`) 탭을 클릭하고 `S3Bucket`이라는 리소스틀 찾으면 확인할 수 있습니다. S3 버킷의 이름을 찾으면 복사해서 텍스트 파일에 붙여 넣어 둡니다.


</details>


## 노트북 사용

먼저 Amazon SageMaker 랜딩 [페이지](https://console.aws.amazon.com/sagemaker/home)로 이동합니다. 서비스 페이지에서 맨 왼쪽 메뉴 표시줄의 `Notebook Instances` 링크를 클릭합니다.

![StackWizard5](static/imgs/img10.png)

Jupyter 인터페이스로 이동하려면 노트북 인스턴스 옆의 맨 오른쪽에 있는 `Open JupyterLab`을 클릭합니다.

![StackWizard5](static/imgs/img11.png)

열려 있는 링크를 클릭하면 Jupyter 시스템으로 리디렉션되는 데 몇 초가 걸립니다. 이 시스템에 연결되면 왼쪽에 파일 모음이 표시됩니다.

시작하려면 [도메인 데이터 세트 그룹 및 사용 사례에 최적화된 추천](https://docs.aws.amazon.com/personalize/latest/dg/create-domain-dataset-group.html)을 사용하여 첫 번째 노트북으로 이동합니다.

`amazon-personalize-samples/getting_started/notebooks/Building_Your_First_Recommender_Video_On_Demand.ipynb`

`amazon-personalize-samples/getting_started/notebooks/Building_Your_First_Recommender_Ecommerce.ipynb`

또는 [사용자 지정 데이터 세트 그룹](https://docs.aws.amazon.com/personalize/latest/dg/custom-dataset-groups.html) 사용:

`amazon-personalize-samples/getting_started/notebooks/1.Building_Your_First_Campaign.ipynb`

실습의 나머지 부분은 Jupyter 노트북을 통해 진행되며, 각 블록을 읽고 실행한 후 다음 블록으로 넘어갑니다. 노트북 사용 방법과 관련해 궁금한 점이 있으면 강사에게 문의하거나, 혼자 작업하는 경우에는 다음 동영상을 참조하여 시작할 수 있습니다.

https://www.youtube.com/watch?v=Gzun8PpyBCo

## 노트북 완료 후

노트북의 모든 작업을 완료하고 정리 단계도 완료했으면, 마지막으로 CloudFormation으로 만든 스택을 삭제합니다. 그러려면 AWS 콘솔에서 상단의 `Services` 링크를 다시 클릭하고, 이번에는 `CloudFormation`로 이동해 해당 서비스 링크를 클릭합니다.

![StackWizard5](static/imgs/img9.png)

생성한 데모 스택에서 `Delete` 버튼을 클릭합니다.

![StackWizard5](static/imgs/img13.png)

마지막으로 팝업에 표시되는 `Delete Stack` 버튼을 클릭합니다.

![StackWizard5](static/imgs/img14.png)

이제 스택이 삭제되는 중임을 알 수 있습니다. `Delete Completed`라고 표시되면 모든 항목이 삭제되고 이 실습이 100% 완료되었음을 알 수 있습니다.


