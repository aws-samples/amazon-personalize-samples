# Lambda 예제

이 폴더는 S3에서 전송된 새 데이터를 처리하는 Lambda 함수를 사용하여 `put_events`를 Personalize 캠페인에 통합하는 기본 예제로 시작합니다.

여기서 시작하려면 먼저 초기 이벤트 트래커를 생성하는 두 번째 노트북을 비롯하여, `getting_started` 노트북 컬렉션을 완료합니다.


## S3로 이벤트 전송

이 폴더에는 일련의 메시지를 S3 버킷으로 전송하기 위한 보일러 플레이트 코드가 포함된 `Sending_Events_to_S3.ipynb`라는 노트북이 있습니다.

이 노트북은 메시지를 다시 Personalize로 전송하는 Lambda 함수를 사용하는 데 중요한 역할을 합니다.

## Lambda 함수

이제 노트북이 S3 버킷에 파일을 안정적으로 씁니다. 다음 작업은 S3 트리거 발생 시 호출할 Lambda 함수를 구축하는 것입니다. Lambda의 코드는 내부에 있습니다.`event_processor.py`


먼저 Lambda 콘솔로 이동한 다음 `Create Function`을 클릭하고 원하는 이름을 지정한 후 런타임으로 Python 3.6을 선택합니다.

이 Lambda 함수를 사용하려면 새 IAM 역할이 필요합니다. 먼저 기본 역할을 허용합니다. 나중에 Personalize 및 S3와 함께 작동하도록 업데이트됩니다. 다음 검색 결과 `Create function`


이제 `+ Add trigger`를 클릭하고 S3를 검색한 다음 버킷을 선택하고 데모용으로 `All object create events`를 선택한 후, 접미사로 `.json`을 추가합니다. 마지막으로 이 페이지에서 다음을 클릭합니다.`Add`

그런 다음 Lamda 함수의 아이콘을 클릭합니다. 아래에 편집기가 나타나면 `event_processor.py`의 콘텐츠를 편집기에 복사하여 저장합니다. 기존 콘텐츠를 모두 바꿉니다.

편집기에서 아래로 스크롤하여 `Environment Variables`에 `trackingId`를 키로 입력하고, 두 번째 노트북의 추적 ID를 값으로 입력합니다.

이제 준비가 거의 끝났습니다. 마지막으로 구성해야 할 것은 IAM 처리 방법입니다. 아래로 스크롤하여 하단에 `Execution role`이 나타나면 링크를 마우스 오른쪽 단추로 클릭한 `View the ....` 다음 새 탭에서 엽니다.

`Attach policies`를 클릭하고 `AmazonS3FullAccess`와 `AmazonPersonalizeFullAccess`를 모두 추가한 후 `Attach policy`를 클릭합니다. 이 구성은 보안상 적합하지 않지만 요점을 보여주기 위한 것입니다. 프로덕션 워크로드의 경우 작업 중인 리소스에 맞게 사용자 지정 정책을 명시적으로 생성합니다.

연결되면 탭을 닫고 열어 둔 Lambda 콘솔 페이지로 돌아갑니다. 오른쪽 상단에서 `Save`를 클릭합니다.

맨 위로 다시 스크롤하여 `Monitoring`을 선택한 다음, 이벤트를 시뮬레이션하는 노트북으로 돌아가서 해당 셀을 다시 실행하여 새 파일을 작성하고 Lambda 함수를 실행합니다.

몇 초 후 페이지를 새로 고치면 호출이 성공했음을 확인할 수 있습니다.
