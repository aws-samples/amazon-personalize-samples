# Amazon Personalize 필터 교체

이 프로젝트에는 데이터를 기반으로 맞춤형 기계 학습 추천 시스템을 만들 수 있는 AWS의 AI 서비스인 [Amazon Personalize](https://aws.amazon.com/personalize/)에 자동 [필터](https://docs.aws.amazon.com/personalize/latest/dg/filter.html) 교체 기능을 제공하는 서버리스 애플리케이션을 배포하기 위한 소스 코드와 지원 파일이 포함되어 있습니다. 이 프로젝트의 주요 기능은 다음과 같습니다.

- 사용자가 제공하는 동적 필터 이름 지정 템플릿을 기반으로 필터 생성
- 사용자가 제공하는 동적 필터 표현식 템플릿을 기반으로 필터 표현식 구성
- 사용자가 제공하는 동적 매칭 표현식을 기준으로 필터 삭제(선택 사항)
- 필터가 생성되거나 삭제되면 [Amazon EventBridge](https://aws.amazon.com/eventbridge/)에 이벤트 게시(선택 사항)

## <a name='Whatarefilters'></a>필터란 무엇인가요?
Amazon Personalize 필터는 애플리케이션에 추천을 반환하기 전에, 비즈니스 규칙을 적용하는 데 유용한 수단입니다. 사용자의 상호 작용 기록, 항목 메타데이터 및 사용자 메타데이터를 고려하는 SQL 형식의 구문을 기반으로, 사용자에게 추천되는 항목을 포함하거나 제외하는 데 사용할 수 있습니다. 예를 들어 사용자가 과거에 시청했거나 즐겨 본 영화만 추천하여 ‘Watch again’ 위젯을 채웁니다.

```
INCLUDE ItemID WHERE Interactions.event_type IN ('watched','favorited')
```

또는 현재 품절된 제품을 추천 항목에서 제외합니다.

```
EXCLUDE ItemID WHERE Items.out_of_stock IN ('yes')
```

런타임에 필터 표현식 값이 지정된 경우에도 동적 필터를 사용할 수 있습니다. 예를 들어 특정 장르의 영화만 추천합니다.

```
INCLUDE ItemID WHERE Items.genre IN ($GENRES)
```

위의 필터를 사용하려면 [GetRecommendations API](https://docs.aws.amazon.com/personalize/latest/dg/API_RS_GetRecommendations.html)를 사용하여 추천을 가져올 때 `$GENRE` 변수에 적절한 값을 전달해야 합니다.

필터에 대한 자세한 내용은 [여기](https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/)와 [여기](https://aws.amazon.com/blogs/machine-learning/amazon-personalize-now-supports-dynamic-filters-for-applying-business-rules-to-your-recommendations-on-the-fly/)의 AWS Personalize 블로그 게시물을 참조하세요.

## <a name='Whyisfilterrotationnecessary'></a>필터는 왜 교체해야 하나요?
필터는 훌륭한 도구입니다. 하지만 몇 가지 제한 사항이 있습니다. 그러한 제한 사항 중 하나는 범위 쿼리(`<`, `<=`, `>`, `>=`)에 동적 값을 지정할 수 있다는 것입니다. 예를 들어 이전 롤링 포인트 이후 생성된 새 항목으로 추천을 제한하는 다음 필터는 지원되지 **않습니다**.

**지원되지 않음**
```
INCLUDE ItemID WHERE Items.creation_timestamp > $NEW_ITEM_THRESHOLD
```

이 제한 사항은 값이 하드 코딩된 필터 표현식을 범위 쿼리에 사용함으로써 해결할 수 있습니다.

**지원됨**
```
INCLUDE ItemID WHERE Items.creation_timestamp > 1633240824
```

하지만 시간이 지나도 정적 필터 표현식은 그에 따라 바뀌지 않기 때문에 유연하지 않고 유지 관리하기가 어렵습니다. 이 문제는 필터 표현식을 주기적으로 업데이트하여 롤링 기간을 유지함으로써 해결합니다. 아쉽게도, 필터를 업데이트할 수 없으므로 새 필터를 만들어야 하고, 애플리케이션에서 새 필터를 사용하도록 설정해야 하며, 그래야 이전 필터를 안전하게 삭제할 수 있습니다.

이 서버리스 애플리케이션의 목적은 필터 생성 및 삭제를 자동화하고 새 필터를 생성할 때 적절한 하드 코딩된 값으로 확인되는 동적 표현식을 제공함으로써 이 프로세스를 보다 손쉽게 유지 관리하는 것입니다.

## <a name='Hereshowitworks'></a>작동 방식

이 애플리케이션은 반복적으로 호출되는 AWS Lambda [함수](./src/filter_rotator_function/filter_rotator.py)를 배포합니다. 사용자는 [cron 또는 rate 표현식](https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html)으로 나타낼 수 있는 스케줄을 제어합니다. 이 함수는 현재 필터 이름 템플릿과 일치하는 필터가 아직 없는 경우에만 새 필터를 만들고 삭제 템플릿과 일치하는 기존 필터만 삭제합니다. 따라서 이 함수는 필요 이상으로 자주 실행해도 무방합니다(즉, 필터를 교체해야 할 예측 가능하고 일정한 시간을 알 수 없는 경우).

필터 교체 함수의 핵심은 현재 템플릿이 존재하는지, 그리고 기존 템플릿이 삭제 가능한지를 확인하는 데 사용되는 템플릿입니다. 함수가 실행될 때마다 템플릿이 확인되므로 확인된 값은 시간이 지남에 따라 변경될 수 있습니다. 예를 몇 개 살펴보겠습니다. 이 애플리케이션을 배포할 때 이러한 템플릿 값을 CloudFormation 파라미터로 제공합니다.

### <a name="Currentfilternametemplate"></a>현재 필터 이름 템플릿

최근에 생성된 항목만 추천하는 필터를 사용하고자 한다고 가정합니다. 항목 데이터 세트의 `CREATION_TIMESTAMP` 열은 이 용도로 사용할 수 있는 편리한 필드입니다. 이 열 이름은 예약되어 있으며 `aws-user-personalization` 레시피의 콜드 항목 탐색 기능을 지원하는 데 사용됩니다. 이 열의 값은 `long`이라는 Unix 타임스탬프 형식으로 표현되어야 합니다(즉, Epoch 이후 경과 시간(초)). 다음 필터 표현식은 지난 달에 생성된 항목을 제한합니다(`1633240824`는 이 문서 작성 시점을 기준으로 1개월 전의 UNIX 타임스탬프).

```
INCLUDE ItemID WHERE Items.creation_timestamp > 1633240824
```

또는 보다 투박한 형식 및/또는 사람이 읽을 수 있는 형식을 사용하지만 `YYYYMMDD`와 같은 범위 쿼리와 유사한 사용자 지정 메타데이터 열을 필터에 사용할 수 있습니다.

```
INCLUDE ItemID WHERE Items.published_date > 20211001
```

앞서 설명한 대로 필터는 업데이트할 수 없습니다. 따라서 필터의 필터 표현식만 변경할 수는 없습니다. 대신 새 표현식을 사용하여 새 필터를 만들고 애플리케이션에서 새 필터를 사용하도록 전환한 다음 이전 필터를 삭제해야 합니다. 이렇게 하려면 애플리케이션이 코딩 변경 없이 새 필터를 사용하도록 자동으로 전환될 수 있게 필터에 예측 가능한 명명 표준을 사용해야 합니다. 계속해서, 생성 타임스탬프 테마를 사용하면 필터 이름이 다음과 같이 설정됩니다.

```
filter-include-recent-items-20211101
```

이 필터를 매일 교체한다고 가정하면, 다음 날의 필터 이름은 `filter-include-recent-items-20211004`가 되고, 다음 날의 필터 이름은 `filter-include-recent-items-20211005`가 되는 식으로 시간이 지남에 따라 변경됩니다. 한 번에 사용할 수 있는 활성 필터 수가 제한되므로, 많은 수의 필터를 미리 생성할 수 없습니다. 대신, 이 애플리케이션은 필요에 따라 동적으로 새 필터를 만들고 적절한 경우 이전 필터를 삭제합니다. 이를 지원하는 것이 바로 필터 이름 및 표현식에 대해 정의한 템플릿이며, 템플릿은 런타임 시 확인됩니다. 다음은 위에서 설명하는 스키마와 일치하는 필터 이름 템플릿의 예입니다.

```
filter-include-recent-items-{{datetime_format(now,'%Y%m%d')}}
```

위의 필터 이름 템플릿은 런타임에 `{{` 및 `}}` 문자(핸들바 또는 머스테시) 내의 표현식을 확인하고 교체합니다. 이 예에서는 `%Y%m%d` 날짜 형식 표현식을 사용하여 `now`로 표현된 현재 시간의 형식을 지정합니다. 결과(오늘 날짜 기준)는 `20211102`입니다. 교체 함수가 이 이름의 기존 필터를 찾을 경우 새 필터를 만들 필요가 없습니다. 새 필터를 만들 경우 `filter-include-recent-items-20211102`라는 이름으로 새 필터가 생성됩니다.

`PersonalizeCurrentFilterNameTemplate` CloudFormation 템플릿 파라미터는 사용자 지정 필터 이름 템플릿을 지정하는 데 사용됩니다.

템플릿 구문에 사용할 수 있는 함수와 연산자는 아래에서 설명합니다.

### <a name="Currentfilterexpressiontemplate"></a>현재 필터 표현식 템플릿

새 필터를 교체하고 생성할 때 실제 필터 표현식을 동적으로 확인해야 할 수도 있습니다. 여기에 `PersonalizeCurrentFilterExpressionTemplate` CloudFormation 파라미터를 사용할 수 있습니다. 몇 가지 예를 살펴보겠습니다.

```
INCLUDE ItemID WHERE Items.CREATION_TIMESTAMP > {{int(unixtime(now - timedelta_days(30)))}}
```

```
INCLUDE ItemID WHERE Items.published_date > {{datetime_format(now - timedelta_days(30),'%Y%m%d')}}
```

위의 템플릿은 확인 시점의 현재 시간을 기준으로 하드 코딩된 필터 표현식으로 확인됩니다. 첫 번째는 30일 전의 Unix 타임스탬프(Personalize에서 `CREATION_TIMESTAMP`에 요구되는 초 단위로 표시)를 생성합니다. 두 번째 템플릿은 30일 전의 날짜를 `YYYYMMDD` 형식으로 나타내는 정수를 생성합니다.

### <a name="Deletefiltermatchtemplate"></a>필터 삭제 매칭 템플릿

마지막으로 새 버전의 필터로 전환한 후 이전 필터를 정리해야 합니다. 그렇지 않으면 결국 한도에 도달하게 될 것입니다. 필터 이름 매칭 템플릿을 여기에 사용할 수 있으며, 이 템플릿은 새 필터가 생성된 후 한동안 삭제를 지연시키는 방식으로 작성할 수 있습니다. 이렇게 하면 애플리케이션이 이전 필터를 삭제하기 전에 이전 필터에서 새 필터로 전환할 수 있습니다. `PersonalizeDeleteFilterMatchTemplate` CloudFormation 템플릿 파라미터에 필터 삭제 매칭 템플릿을 지정합니다.

다음 필터 삭제 매칭 템플릿은 필터 이름이 `filter-include-recent-items-`로 시작하고 접미사가 오늘보다 하루 이상 경과된 날짜인 필터를 찾습니다. 즉, 이전 필터가 삭제되기 전에 클라이언트 애플리케이션에서 새 필터로 전환할 여유 시간이 하루 있는 것입니다. 이를 애플리케이션에 맞게 사용자 지정할 수 있습니다.

```
starts_with(filter.name,'filter-include-recent-items-') and int(end(filter.name,8)) < int(datetime_format(now - timedelta_days(1),'%Y%m%d'))
```

이 템플릿이 `true`로 확인되도록 하는 필터가 모두 삭제됩니다. 다른 필터는 모두 그대로 남습니다. [ListFilters API](https://docs.aws.amazon.com/personalize/latest/dg/API_ListFilters.html) 응답의 [FilterSummary](https://docs.aws.amazon.com/personalize/latest/dg/API_FilterSummary.html)에서 사용 가능한 모든 필드는 이 템플릿에서 사용할 수 있습니다. 예를 들어 위의 템플릿은 `filter.name`을 매칭합니다. `filter.status`, `filter.creationDateTime` 및 `filter.lastUpdatedDateTime`과 같은 다른 필터 요약 필드도 템플릿의 로직에서 살펴볼 수 있습니다.

## <a name='Filterevents'></a>필터 이벤트

애플리케이션의 구성을 동기화하거나, 필터가 생성 또는 삭제될 때 알림을 받으려면 선택적으로 rotator 함수를 구성하여 이벤트를 [Amazon EventBridge](https://aws.amazon.com/eventbridge/)에 게시할 수 있습니다. 이벤트를 활성화하면 `PersonalizeFilterCreated`, `PersonalizeFilterCreateFailed`, `PersonalizeFilterDeleted` 등 세 가지 이벤트 세부 정보가 rotator 함수에 의해 게시됩니다. 이들 각각에는 `personalize.filter.rotator`라는 이벤트 `Source`가 있고, 생성되거나 삭제된 필터에 대한 세부 정보가 포함되어 있습니다. 이 정보를 사요하여 원하는 대로 이벤트를 처리하도록 EventBridge 규칙을 설정할 수 있습니다. 예를 들어 새 필터가 생성되면 Lambda 함수에서 `PersonalizeFilterCreated` 이벤트를 처리하여 추론 호출에서 새 필터를 사용하는 것으로 전환하도록 애플리케이션의 구성을 업데이트할 수 있습니다.
## <a name='Filtertemplatesyntax'></a>필터 템플릿 구문

[Simple Eval](https://github.com/danthedeckie/simpleeval) 라이브러리가 템플릿 구문의 기반으로 사용됩니다. 이 라이브러리는 Python의 [eval](https://docs.python.org/3/library/functions.html#eval) 함수를 사용하는 것보다 안전하고 샌드박스화된 방식을 제공합니다. 사용 가능한 기능에 대한 자세한 내용과 예제는 Simple Eval 라이브러리 설명서를 참조하세요.

필터 교체를 위한 템플릿을 쉽게 작성할 수 있도록 다음 추가 함수가 이 애플리케이션의 일부로 추가되었습니다.

- `unixtime(value)`: 문자열, 일시, 날짜 또는 시간이 지정된 Unix 타임스탬프 값을 반환합니다. 문자열이 제공된 경우 먼저 날짜/시간으로 구문 분석됩니다.
- `datetime_format(date, pattern)`: 지정된 패턴을 사용하여 일시, 날짜 또는 시간의 형식을 지정합니다.
- `timedelta_days(int)`: 일 수의 시간 델타를 반환합니다. 날짜 계산에 사용할 수 있습니다.
- `timedelta_hours(int)`: 시간 수의 시간 델타를 반환합니다. 날짜 계산에 사용할 수 있습니다.
- `timedelta_minutes(int)`: 분 수의 시간 델타를 반환합니다. 날짜 계산에 사용할 수 있습니다.
- `timedelta_seconds(int)`: 초 수의 시간 델타를 반환합니다. 날짜 계산에 사용할 수 있습니다.
- `starts_with(str, prefix)`: 문자열 값이 접두사로 시작하는 경우 True를 반환합니다.
- `ends_with(str, suffix)`: 문자열 값이 접미사로 끝나는 경우 True를 반환합니다.
- `start(str, num)`: 문자열 값의 첫 번째 숫자 문자를 반환합니다.
- `end(str, num)`: 문자열 값의 마지막 숫자 문자를 반환합니다.
- `now`: 현재 일시입니다.

## <a name='Installingtheapplication'></a>애플리케이션 설치

**중요 참고 사항:** AWS 계정에 이 애플리케이션을 배포하면 AWS 리소스가 생성되고 소비되므로 비용이 발생합니다. 이 Lambda 함수는 사용자가 제공한 스케줄에 따라 호출되지만 일반적으로 시간당 1회 이상 호출할 필요는 없습니다. Personalize는 필터에 대해 요금을 부과하지 않지만 계정에는 동시에 적용할 수 있는 필터 수에 제한이 있습니다. 또한 동시에 보류 중이거나 진행 중인 상태로 있을 수 있는 필터 수도 제한됩니다. 따라서 이 애플리케이션을 설치한 후 솔루션의 일부로 사용하지 않으려는 경우, 계속 요금이 부과되지 않도록 다음 절의 제거 지침을 따르고 모든 데이터를 정리하세요.

이 애플리케이션은 AWS [Serverless Application Model](https://aws.amazon.com/serverless/sam/)(SAM)을 사용하여 AWS 계정에 리소스를 구축하고 배포합니다.

SAM CLI를 사용하려면 다음 도구를 로컬로 설치해야 합니다.

* SAM CLI - [SAM CLI 설치](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 설치됨](https://www.python.org/downloads/)
* Docker - [Docker 커뮤니티 에디션 설치](https://hub.docker.com/search/?type=edition&offering=community)

애플리케이션을 처음으로 빌드하고 배포하려면 셸에서 다음을 실행합니다.

```bash
sam build --use-container --cached
sam deploy --guided
```

첫 번째 명령을 실행할 때, `public.ecr.aws`에서 Docker 이미지를 다운로드할 수 없다는 오류가 표시되면 로그인해야 할 수 있습니다. 다음 명령을 실행하고 위의 두 명령을 다시 시도합니다.

```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
```

첫 번째 명령은 애플리케이션의 소스를 만듭니다. 두 번째 명령은 다음과 같은 일련의 프롬프트를 통해 애플리케이션을 AWS 계정에 패키징하고 배포합니다.

| 프롬프트/파라미터 | 설명 | 기본값 |
| --- | --- | --- |
| 스택 이름 | CloudFormation에 배포할 스택의 이름입니다. 계정 및 리전별로 고유해야 합니다. | `personalize-filter-rotator` |
| AWS 리전 | 이 애플리케이션을 배포할 AWS 리전입니다. | 현재 리전 |
| PersonalizeDatasetGroupArn 파라미터 | 내부에서 필터를 교체할 Amazon Personalize 데이터 세트 그룹의 ARN입니다. | |
| PersonalizeCurrentFilterNameTemplate 파라미터 | 현재 필터를 확인하고 생성할 때 사용할 템플릿입니다. | |
| PersonalizeCurrentFilterExpressionTemplate 파라미터 | 현재 필터를 만들 때 필터 표현식을 작성하는 데 사용할 템플릿입니다. | |
| PersonalizeDeleteFilterMatchTemplate 파라미터(선택 사항) | 삭제해야 하는 기존 필터를 매칭하는 데 사용할 템플릿입니다. | |
| RotationSchedule 파라미터 | rotation 함수를 호출하는 빈도를 제어하는 cron 또는 rate 표현식입니다. | `rate(1 day)` |
| Timezone 파라미터 | Rotator 함수의 Lambda 환경 표준 시간대를 사용자의 표준 시간대와 일치하도록 설정합니다. | `UTC` |
| PublishFilterEvents 파라미터 | 필터를 생성하고 삭제할 때 기본 EventBridge 버스에 이벤트를 게시할지 여부를 나타냅니다. | `Yes` |
| 배포 전에 변경 사항 확인(Confirm changes before deploy) | 예(yes)로 설정하면 CloudFormation 변경 세트가 실행 전에 수동으로 검토할 수 있도록 표시됩니다. 아니요(no)로 설정하면 AWS SAM CLI가 자동으로 애플리케이션 변경 사항을 배포합니다. | |
| SAM CLI IAM 역할 생성 허용 | 이 애플리케이션은 Lambda 함수가 AWS 서비스에 액세스할 수 있도록 IAM 역할을 생성하므로, 이 설정은 `Yes`여야 합니다. | |
| samconfig.toml에 인수 저장(Save arguments to samconfig.toml) | 예(yes)로 설정하면 선택한 내용이 애플리케이션 내부의 구성 파일에 저장되므로, 나중에 파라미터 없이 `sam deploy`를 다시 실행하여 애플리케이션에 변경 사항을 배포할 수 있습니다. | |

**팁**: SAM 명령줄 도구는 파라미터 값을 로컬 파일(`samconfig.toml`)에 저장하는 옵션을 제공하므로, 저장된 값을 다음에 앱을 배포할 때 기본값으로 사용할 수 있습니다. 단, SAM은 파라미터 값을 큰따옴표로 묶습니다. 따라서 템플릿 파라미터 값에 포함된 문자열 값(예: 위의 예에 나와 있는 날짜 형식 표현식)이 있는 경우 이러한 포함된 값에는 작은따옴표를 사용해야 합니다. 그렇지 않으면 파라미터 값이 제대로 보존되지 않습니다.

## <a name='Uninstallingtheapplication'></a>애플리케이션 제거

AWS 계정에서 이 애플리케이션이 생성한 리소스를 제거하려면 AWS CLI를 사용합니다. 스택 이름(`personalize-filter-rotator`)에 기본 애플리케이션 이름을 사용했다고 가정하면 다음을 실행하면 됩니다.

```bash
aws cloudformation delete-stack --stack-name personalize-filter-rotator
```

또는 AWS 콘솔의 CloudFormation에서 스택을 삭제할 수 있습니다.

## <a name='FAQs'></a>FAQ

***Q:*** **이 솔루션을 배포한 후 rotator 스크립트가 실행되는 빈도를 변경하려면 어떻게 해야 하나요?**

***A:*** 두 가지 방법이 있습니다. 다른 빈도로 설정하여 이 솔루션을 다시 배포합니다. 그러면 EventBridge 규칙만 새 빈도로 업데이트하는 변경 세트가 생성됩니다. 아니면 이 솔루션에 의해 생성된 EventBridge 규칙을 AWS 계정에서 직접 편집할 수도 있습니다.

***Q:*** **서로 다른 템플릿과 업데이트 빈도를 사용하는 여러 필터를 이 솔루션을 사용해 교체하려면 어떻게 해야 하나요?**

***A:*** 이 솔루션을 배포한 후에는 다른 입력 값으로 rotator 함수를 호출하는 추가 EventBridge 규칙을 생성할 수 있습니다. 규칙 대상으로 rotator 함수를 선택하고, 상수 JSON인 입력 값을 다음과 같은 형식으로 지정합니다.

```javascript
{
    "datasetGroupArn": "[INSERT_PERSONALIZE_DATASET_GROUP_ARN]",
    "currentFilterNameTemplate": "[INSERT_CURRENT_FILTER_NAME_TEMPLATE]",
    "currentFilterExpressionTemplate": "[INSERT_CURRENT_FILTER_EXPRESSION_TEMPLATE]",
    "deleteFilterMatchTemplate": "[INSERT_DELETE_FILTER_MATCH_TEMPLATE]"
}
```

## <a name='Licensesummary'></a>라이선스 요약

이 샘플 코드는 수정된 MIT 라이선스에 따라 사용할 수 있습니다. LICENSE 파일을 참조하세요.
