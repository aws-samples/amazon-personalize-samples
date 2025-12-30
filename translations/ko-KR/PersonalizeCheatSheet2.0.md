# Amazon Personalize 치트 시트

## Amazon Personalize가 적합한 솔루션일까요?

Amazon Personalize는 AWS에서 대규모로 추천 시스템을 운영하기에 훌륭한 플랫폼이지만, 모든 개인화 또는 추천 시나리오에 적합한 것은 아닙니다. 아래 차트는 적합한 시나리오와 적합하지 않은 시나리오에 대한 대략적인 지침입니다.

|적합	|적합하지 않음	|
|---	|---	|
|알려진 사용자에게 항목을 추천합니다. 시청 기록을 기반으로 사용자에게 영화를 추천합니다.	|명시적 메타데이터 플래그를 기반으로 추천합니다. 새 사용자가 선호도 질문에 답하여 추천의 방향을 제시하는 경우입니다.	|
|알려진 사용자에게 새 항목을 추천합니다. 기존 사용자에게 판매할 새 항목을 추가하는 소매 사이트입니다.	|사용자, 항목 및 상호 작용을 위한 데이터 볼륨이 낮습니다(아래 차트 참조).	|
|새 사용자에게 항목을 추천합니다. 방금 가입한 사용자가 신속하게 추천을 받을 수 있습니다.	|대부분 확인되지 않은 사용자입니다. 사용자가 활동 기록 레코드를 가지고 있지 않은 애플리케이션입니다.	|
|새 사용자에게 새 항목을 추천합니다. 새 사용자에게 새 항목을 추천하는 소매 사이트입니다.	|**차선의 조치 워크로드 -** Personalize는 유망한 항목을 추천하며, 적절한 워크플로와 시퀀스를 이해하지 못합니다.	|

### 최소 제안 데이터 볼륨

1. 50명 이상의 사용자.
2. 50개 이상의 항목.
3. 1,500건 이상의 상호 작용.

데이터 세트가 여기에 매핑되지 않으면 Amazon Personalize가 너무 빠릅니다.


## 레시피별 사용 사례

어떤 종류의 사용 사례를 어떻게 해결할 수 있나요?

1. **개인별 추천** `User-Personalization`:
    1. 이는 Amazon Personalize의 주요 사용 사례로, 사용자 항목 상호 작용 데이터를 사용하여 각 사용자를 직접 대상으로 하는 추천 모델을 구축하고, 재훈련 없이 PutEvents를 통해 즉시 새 사용자를 추가할 수 있습니다. 또한 PutEvents를 통해 사용자는 최신 동작에 기반한 추천을 볼 수 있으므로 추가 정보를 놓치지 않습니다. 또한 디바이스 유형 또는 위치와 같은 컨텍스트별 구성 요소를 사용하여 결과를 개선할 수 있습니다.
    2. 또한 모델을 더욱 풍부하게 하거나 특성별로 추천을 필터링하기 위해 항목 및 사용자 메타데이터를 추가할 수 있습니다.
    3. VOD 및 Retail 사용 사례의 경우 도메인 추천인 ‘Top picks for you’ (고객님을 위한 탑 픽)및 ‘Recommended for you’ (고객님을 위한 추천 상품)를 사용하여 운영 오버헤드를 줄이고 신속하게 작업을 시작할 수 있습니다.
2. **새 사용자에게 항목 추천**`User-Personalization`:
    1. PutEvents 기능을 활용하여 기존 사용자 개인화 솔루션에 새 사용자(콜드 사용자)를 추가할 수 있습니다. 각 새 사용자는 인기 있는 항목을 반환하는 서비스의 표현으로 시작합니다. 이 표현은 사용자의 행동에 의해 이동됩니다. 애플리케이션 내의 콘텐츠와 상호 작용하고 이벤트가 애플리케이션에서 Personalize로 전송되면 모델을 재훈련할 필요 없이 추천이 업데이트됩니다. 이를 통해 지속적인 재훈련 없이 최신 개인화 데이터를 제공합니다.
3. **새 항목 추천** `User-Personalization`:
    1. 이 기능은 고객이 새로운 항목(일명 콜드 항목)을 사용자에게 개인화의 형태로 보여줘야 하는 경우 매우 유용합니다. 이를 통해 메타데이터 요인에 따라 과거 전례 없이 항목을 추천할 수 있습니다.
    2. 또한 데이터 세트의 증분 훈련 및 업데이트와 함께 사용하여 새 항목을 보다 쉽게 콜드 스타트할 수 있습니다.
    3. 마지막으로 이 접근 방식은 탐색 기능과 같은 밴디트를 활용하여 어떤 결과가 타당하고 어떤 결과가 추천에 부합하지 않는지 신속하게 판단할 수 있도록 지원합니다. 이는 단순히 새로운 콘텐츠를 무작정 푸시하는 것보다 훨씬 나은 방법입니다.
4. **연관성에 따른 순서 조정**`Personalized-Ranking`:
    1. 사용자 개인화와 동일한 HRNN 알고리즘을 사용하지만, 사용자와 항목 컬렉션을 사용합니다. 그런 다음 항목 컬렉션을 살펴보고 사용자에게 가장 관련성이 낮은 순으로 순위를 매깁니다. 이것은 미리 선택된 항목 모음을 홍보하고 특정 사용자에게 홍보해야 할 올바른 것이 무엇인지 아는 데 유용합니다.
5. **관련 항목** `Similar-Items`/`SIMS`:
    1. `Similar-Items`: 상호 작용 기록 및 항목 메타데이터 유사성을 기반으로 관련 항목 추천의 균형을 맞추기 위해 상호 작용 데이터와 항목 메타데이터를 모두 고려하는 딥 러닝 모델입니다. 상호 작용 데이터가 적지만 양질의 항목 메타데이터가 있거나 콜드/신규 항목을 자주 도입할 때 유용합니다.
    2. `SIMS`: 항목별 협업 필터링을 통해 구현되는 매우 간단한 아이디어이지만 기본적으로 사람들이 특정 항목과 상호 작용하는 방식을 살펴본 다음 상호 작용 데이터를 기반으로 글로벌 수준에서 항목이 얼마나 유사한지 결정합니다. 항목 또는 사용자 메타데이터를 고려하지 않으며 각 사용자에게 개인화되지 않습니다. 관련 상호 작용 데이터가 많거나, 콜드 항목이 많지 않거나(카탈로그 변경) 항목 메타데이터가 부족한 경우에 유용합니다.
    3. VOD 및 소매 사용 사례의 경우 도메인 추천 시스템 ‘Because you watched X’ (X와 유사한 상품), ‘More like X’ (X와 유사한 다른 상품), ‘Frequently bought together’ (함께 많이 구매한 상품) 및 ‘Customers who viewed X also viewed’를 사용하면 운영 오버헤드를 줄이면서 빠르게 시작하고 진행할 수 있습니다.
6. **Frequently Bought Together (함께 많이 구매한 상품)** `Similar-Items`/`SIMS`:
    1. 핵심은 Personalize에서 모델을 훈련하는 데 사용되는 올바른 데이터를 준비하고 올바른 레시피를 선택하는 것입니다. 예를 들어 구매 데이터에 대해서만 SIMS 모델을 훈련하고, 가능하면 고객이 여러 항목을 구매하거나 여러 범주에 걸쳐 구매한 데이터에 대해서만 훈련합니다. 이렇게 하면 모델에 원하는 동작이 적용되고 추천이 다양해집니다(이 사용 사례에서 원하는 대로).
    2. 또한 SIMS를 Personalized-Ranking과 결합하여 사용자에게 추천하기 전에 SIMS의 추천을 다시 정렬할 수 있습니다. 이렇게 하면 함께 자주 구입하는 품목의 맞춤 주문이 제공됩니다.
    3. 도메인 추천 시스템 ‘Frequently buy together’ (함께 많이 구매한 상품)를 사용하면 운영 오버헤드를 줄이면서 빠르게 시작하고 진행할 수 있습니다.
7. **전반적으로 가장 인기 있는 항목** `Popularity-Count`:
    1. 기계 학습이 아니라 항목과 가장 일반적으로 상호 작용하는 항목을 세는 기준선에 불과합니다. 이 레시피는 인기 있는 항목 추천이나 오프라인 지표의 기준을 만드는 데 유용하며, 이 기준은 동일한 데이터 세트에 다른 사용자 개인화 레시피를 사용하여 만든 솔루션 버전과 비교하는 데 활용할 수 있습니다.
    2. 주문형 비디오 및 소매 사용 사례의 경우 "가장 인기 있는", "가장 많이 본" 및 "베스트 셀러" 도메인 추천을 통해 운영 오버헤드를 줄이고 신속하게 시작하고 진행할 수 있습니다.
8. **사용자 세분화** `Item-Affinity`/`Item-Attribute-Affinity`:
    1. 카탈로그의 특정 항목에 대한 선호도 또는 항목 속성에 대한 선호도를 기준으로 사용자 세그먼트를 생성합니다. 홍보하고자 하는 특정 항목 또는 기존 항목과 유사한 항목에 관심을 가질 사용자를 대상으로 하는 마케팅 캠페인과의 완벽한 매치입니다.

## 킬러 기능:

1. [도메인 데이터 세트 그룹](https://docs.aws.amazon.com/personalize/latest/dg/domain-dataset-groups.html): VOD 및 소매 사용 사례를 위한 추천 시스템입니다.
    1. 도메인 데이터 세트 그룹은 데이터 세트, 추천 시스템 및 필터를 포함하여 미리 구성된 도메인별 리소스를 위한 Amazon Personalize 컨테이너입니다. 스트리밍 비디오 또는 전자 상거래 애플리케이션이 있고 Amazon Personalize가 추천 시스템에 가장 적합한 구성을 찾도록 하려면 도메인 데이터 세트 그룹을 사용합니다.
2. 상황별 추천
    1. 사용자나 항목에 따라 달라지는 것이 아니라 상호 작용에 따라 달라지는 추천의 범위를 지정할 수 있습니다. 사용자의 현재 위치, 사용 중인 장치/채널, 시간, 요일 등을 생각해 보세요.
    2. 자세한 예는 다음 블로그 게시물을 참조하세요. https://aws.amazon.com/blogs/machine-learning/increasing-the-relevance-of-your-amazon-personalize-recommendations-by-leveraging-contextual-information/
3. 상호 작용 및 메타데이터 필터링
    1. 사용자의 상호 작용 기록 또는 항목 또는 현재 사용자의 메타데이터 속성을 기준으로 추천을 필터링합니다. 거의 모든 미디어 또는 소매 작업 부하에서 매우 유용합니다. 예를 들어 최근에 구매한 항목이나 품절된 항목을 제외하거나 범주 또는 장르를 기준으로 추천을 포함/제외합니다.
    2. 자세한 내용은 다음 블로그 게시물을 참조하세요. https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/
4. 배치 추론
    1. 캐싱, 이메일 캠페인 또는 일반 탐색을 위해 많은 양의 추천을 파일로 내보내는 데 적합합니다.
5. AutoScaling 캠페인
    1. 특정 캠페인이 초과 구독될 경우 트래픽 수요에 맞게 서비스가 자동으로 확장됩니다. 그런 다음 트래픽 볼륨이 줄어들면 요청된 최소 용량으로 줄어듭니다.
6. 항목 메타데이터로서의 비정형 텍스트
    1. 제품 설명, 비디오 플롯 개요 또는 기사 내용을 항목 메타데이터 필드로 추가하고 Personalize가 자연어 처리(NLP)를 사용하여 텍스트에서 숨겨진 특성을 추출함으로써 추천의 연관성을 높이도록 합니다.
7. Put Events
    1. 애플리케이션이 사용자 동작의 의도를 변경하여 Personalize를 실시간으로 업데이트할 수 있습니다. 이는 각 후속 요청이 재훈련 없이 해당 의도에 적응할 수 있음을 의미합니다.
8. Put Items/Put Users
    1. 애플리케이션이 전체 항목 및 사용자 데이터 세트를 업로드하지 않고도 항목 또는 사용자의 개별 또는 미니 배치를 추가/업데이트할 수 있습니다.
    2. 자세한 내용은 아래의 FAQ를 참조하세요.
9. KMS 통합
    1. 고객 관리 키를 사용하여 모든 데이터를 암호화할 수 있으며, 모든 데이터는 암호화됩니다.
10. 정보가 공유되지 않음
    1. 모든 고객 데이터는 완전히 격리되어 있으며 Amazon 또는 다른 당사자의 추천을 개선하기 위해 활용되지 않습니다.
    2. 모델은 고객의 AWS 계정에 비공개로 제공됩니다.

## 동영상 시리즈:

1. Amazon Personalize 소개: https://www.youtube.com/c/amazonwebservices/videos
2. Amazon Personalize로 데이터 이해하기: https://www.youtube.com/watch?v=TEioktJD1GE
3. Amazon Personalize로 실제 사용 사례 해결: https://www.youtube.com/watch?v=9N7s_dVVWBE
4. 사용자에게 Amazon Personalize 추천 제공하기: https://www.youtube.com/watch?v=oeVYCOFNFMI
5. Amazon Personalize POC를 프로덕션에 적용하기: https://www.youtube.com/watch?v=3YawVCO6H14

## FAQ:

1. 얼마나 자주 재훈련해야 하나요?
    1. 재훈련 빈도는 비즈니스 요구 사항에 따라 결정됩니다. 얼마나 자주 사용자 및 항목에 대한 사용자의 행동에 대해 글로벌하게 학습해야 하나요? 새 항목을 얼마나 자주 포함해야 하나요? 이 대답에 따라 얼마나 자주 훈련해야 하는지 결정됩니다. 일반적으로 대부분의 고객은 매주 재훈련합니다. 자세한 지침은 아래를 참조하세요.
    2. "aws-user-personalization" 레시피를 사용하는 경우 서비스는 2시간마다(추가 비용 없이) 백그라운드에서 솔루션 버전을 자동으로 업데이트합니다. 이 자동 업데이트 프로세스에서는 마지막 업데이트 이후에 추가된 새 항목(예: 콜드 스타트 항목)을 사용자에게 추천하기 시작합니다. 이 작업은 explorationWeight 파라미터와 함께 작동합니다. 이는 새 항목/콜드 항목과 관련 항목(탐색/이용)에 대한 가중치를 제어하기 위해 캠페인에 설정되는 가중치 파라미터입니다.
    3. 2시간 자동 업데이트가 새 항목을 소개할 만큼 자주 수행되지 않는 경우 trainingMode=UPDATE를 사용하여 새 솔루션 버전을 수동으로 생성하고 캠페인을 더 자주(즉, 매시간) 업데이트할 수 있습니다. 이는 기본적으로 고객이 정의한 빈도로 자동 업데이트와 동일한 작업을 수행합니다. 하지만 이 작업을 수동으로 수행하는 데는 훈련 시간이 소요됩니다.
    4. 수행한 자동 업데이트 모드 또는 수동 업데이트 모드 프로세스에 관계없이 모델을 완전히 재훈련하지는 않습니다. 고객은 여전히 경우에 따라 모델을 완전히 재훈련하기 위해 trainingMode=FULL을 사용하여 새 솔루션 버전을 만들어야 합니다. 경우에 따라 모든 데이터를 기반으로 모델 전반의 가중치를 재계산하기 위해 이를 수행해야 하지만, 자동 업데이트 프로세스를 통해 필요한 전체 재훈련의 빈도가 줄어듭니다. 이것이 주간 지침이 되는 부분입니다. 따라서 자동 업데이트를 일주일 내내 실행하고 일주일에 한 번 전체 재훈련을 실시합니다.
    5. 재훈련 빈도를 더 정확하게 하기 위해, 온라인 측정 기준을 모니터링할 수도 있습니다. 그들이 (모델 드리프트와 같이) 서서히 사라지기 시작하면, 이제 다시 훈련해야 할 때입니다.
2. 새 사용자를 추가하려면 어떻게 해야 하나요?
    1. PutEvents API를 사용하는 경우 첫 번째 작업을 기록하는 즉시 새 사용자가 존재합니다. 이를 활용하지 않는 경우 상호 작용 데이터 세트에 해당 동작이 포함된 모델을 재훈련하는 즉시 사용자가 시스템에 존재하게 됩니다.
    2. 사용자를 알 수 없는 경우에도(등록하기 전에 새 익명 사용자) 콜드 스타트 작업을 수행할 수 있습니다. 사용자 및 세션에 새 UUID를 할당할 수 있습니다.즉시 ID를 지정한 후 위에서 정의한 프로세스를 계속하여 사용자를 콜드 스타트시킬 수 있습니다.
    3. 이 경로가 작동하지 않는 경우에도 sessionID의 새 UUID를 생성하고, userID 없이 PutEvents를 호출하고, 그런 다음 유효한 userID가 생성된 후에도 계속 동일한 sessionID를 지정할 수 있습니다. 재훈련 시 Personalize는 기록 데이터와 PutEvents 데이터를 결합하고 일치하는 sessionID가 있으면 이전의 모든 익명 상호 작용을 사용자의 비익명 상호 작용과 결합합니다. 이를 통해 유효한 내부 userID가 존재하기 전의 기록을 지정할 수 있습니다.
    4. PutUsers API를 사용하여 개별적으로 또는 미니 배치로 사용자를 추가/업데이트할 수 있습니다. 하지만 상호 작용이 있는 사용자만 (재)훈련 후에 또는 PutEvents API로 콜드가 시작되면 개인별 추천을 받게 됩니다.
3. 새 항목을 추가하려면 어떻게 해야 하나요?
    1. 항목 데이터 세트에 항목을 추가하는 방법은 두 가지가 있습니다. 1/ 데이터 세트 가져오기 작업을 통해 전체 데이터 세트를 업로드하여 항목 데이터 세트에 새 항목을 추가하거나, PutItems API를 사용하여 항목을 개별적으로 또는 미니 배치로 추가합니다.
    2. 솔루션이 업데이트된 후 상호 작용이 있거나 상호 작용이 없는 경우(모든 레시피) 또는 콜드 스타트되는 새 항목 추천이 있는 경우(trainingMode = FULL/UPDATE, aws-user-personalization 및 HRNN-Coldstart에만 해당) 새 항목이 추천에 통합됩니다.
    3. 예를 들어 새 릴리스에 대한 배너를 배치하여 새 항목을 기록 데이터 세트에 유기적으로 스트리밍할 수 있습니다. 사용자가 새 항목과 상호 작용하고 해당 작업을 기록하도록 하는 모든 작업은 다음 훈련 후의 추천을 개선할 수 있습니다.
4. 특정 조건에 대한 결과를 필터링하려면 어떻게 해야 하나요?
    1. 상호 작용(https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/) 또는 메타데이터 정보(https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/) 에 필터 기능을 사용합니다.
    2. 상호 작용 기록에 기반한 필터링은 현재 재훈련 시 데이터 세트에서 가장 최근의 실시간 상호 작용 100건(PutEvents API)과 가장 최근의 과거 상호 작용 200건만 고려합니다. 모든 이벤트 유형은 100/200 제한에 포함됩니다.
5. 롤링 날짜 값을 기준으로 항목을 필터링해야 하지만 필터는 범위 연산자에 대한 동적 값을 지원하지 않습니다. 제가 할 수 있는 일이 뭐죠?
    1. 범위 연산자는 현재 동적 값과 함께 사용할 수 없으므로 고정 값으로 필터 식을 만든 다음 필터를 주기적으로 회전하여 고정 값을 업데이트해야 합니다. [필터 교체기](https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/filter_rotator) 솔루션을 사용하여 교체 프로세스를 자동화할 수 있습니다.
6. 사용자 지정 솔루션보다 Amazon Personalize를 사용해야 하는 이유는 무엇인가요?
    1. 데이터와 사용 사례가 일치한다고 가정할 때, 이는 최종 사용자 앞에서 동급 최고의 모델을 더 빨리 얻을 수 있는 좋은 방법입니다. Personalize는 추천 시스템을 대규모로 실행해야 하는 운영 부담을 해소하는 동시에 기능 엔지니어링, 데이터 수집, 사용자 경험 또는 기타 문제를 해결할 수 있도록 지원합니다.
7. 고객이 카탈로그에 있는 항목을 자주 구매하거나(예: 자동차 구입) 상호 작용하는 사용 사례가 있습니다. 이 경우에도 Personalize가 적합한 솔루션인가요?
    1. 예, Personalize를 이러한 유형의 사용 사례에 효과적으로 사용할 수 있습니다. 예를 들어 검색 또는 구매 내역(온라인 및/또는 오프라인)과 같은 모든 사용자 활동을 기반으로 SIMS 모델을 훈련한 다음 항목 세부 정보 페이지에서 유사한 항목 추천에 사용할 수 있습니다. 이를 통해 모든 활성 사용자에 대한 최근 활동을 활용하여 반환 사용자에게 적절한 추천을 제공할 수 있습니다.
    2. 또한 Personalize는 사용자의 현재 관심사로부터 학습하고 추천을 빠르게 적용할 수 있으므로 실시간 추천도 효과적입니다. 예를 들어 처음에 인기 있는 항목을 추천한 다음 PutEvents API를 사용하여 몇 가지 상호 작용이 스트리밍된 후 추천을 빠르게 개인화합니다.
8. AutoML을 사용해야 하나요?
    1. 아니요, 레시피는 다양한 사용 사례를 해결합니다. 시간을 내어 사용 사례에 가장 적합한 레시피를 선택하고 이 기능을 생략하세요.
9. HPO를 얼마나 자주 사용해야 하나요?
    1. 자주 사용하지 않습니다. 특정 HPO 작업의 결과를 가져와서 여러 번의 재훈련을 위해 솔루션 구성에서 명시적으로 사용합니다. 그런 다음 HPO를 다시 실행하고 반복합니다. 현실적으로 조정된 파라미터는 훈련 작업 간에 크게 변동되지 않아야 합니다. 이 접근 방식을 사용하면 모델 정확도를 저하시키지 않으면서, 모든 훈련 작업에 대해 HPO를 실행하는 경우보다 훈련 시간 및 비용을 절감할 수 있습니다.
10. 훈련에 따른 요금을 어떻게 예측할 수 있나요?
    1. 불행히도 이것을 미리 알 수 있는 좋은 방법은 없습니다. 우리는 MovieLens 데이터 세트에 대해 몇 가지 테스트를 수행했습니다. 예를 들어 `User-Personalization`을 사용할 경우 2,500만 건의 상호 작용에 대한 훈련에 6시간 정도 걸리지만 100,000건의 상호 작용에 대한 훈련에는 1시간도 걸리지 않습니다. 훈련은 여러 호스트에 분산되기 때문에 실제 시간은 5천만 건의 경우 53.9시간, 100,000건의 경우 2.135시간입니다. 계산은 사람이 아닌 실제 시간에 이루어집니다.
11. TPS 시간이란 무엇이며 가격/사용성과 어떤 관련이 있나요?
    1. Amazon Personalize는 예상되는 최소 처리량 요구 사항(초당 트랜잭션 수 또는 TPS)을 충족하기 위해 프로비저닝된 상태로 유지되는 전용 컴퓨팅 리소스를 스핀업합니다. 이러한 리소스는 할당된 시간(TPS 시간)으로 청구됩니다. 1 TPS-Hour는 1시간 동안 초당 1개의 추천을 제공하는 데 필요한 컴퓨팅 용량입니다.
    2. 평균 요청 수 및 각 증분에서 프로비저닝된 최소 처리량의 최대값이 TPS 시간 값으로 사용되는 경우 사용량은 5분 단위로 측정됩니다. 따라서 서비스가 최소 프로비저닝된 TPS 이상으로 확장되면 고객은 실제 사용된 용량에 대해서만 청구됩니다. 모든 5분 증분에 대한 TPS-Hours는 청구 기간 동안 합산되어 청구 계산의 총 TPS-Hours를 결정합니다.
    3. 이 서비스는 트래픽이 캠페인에서 프로비저닝된 최소 TPS를 초과할 경우 자동으로 스케일업되며, 많은 고객에게 유용한 도구임이 입증되었습니다. 용량 버퍼가 프로비저닝된 최소 TPS보다 높게 할당되어 서비스가 스케일아웃하는 동안 요청 로드의 증가를 흡수할 수 있습니다.
    4. 고객이 플래시 세일이나 프로모션 이벤트와 같은 활동이 급증할 것을 알고 있다면, 일부 자동화된 프로세스를 사용하여 프로비저닝된 용량을 업데이트하도록 한 다음, 서비스가 자동 확장될 때까지 5-10분 정도 기다릴 수 없는 경우 나중에 속도를 줄이세요.
    5. Amazon Personalize Monitor 프로젝트는 Personalize 캠페인을 위한 CloudWatch 대시보드, 사용자 지정 메트릭, 활용률 경보 및 비용 최적화 기능을 제공합니다. https://github.com/aws-samples/amazon-personalize-monitor
12. Personalize 모델이 고품질 추천을 제공하는지 어떻게 알 수 있나요?
    1. Personalize는 상호 작용 데이터 세트의 보류된 데이터에 대해 모델의 예측 정확도를 측정할 수 있도록 각 솔루션 버전에 대한 오프라인 지표를 제공합니다. 이 메트릭을 사용하여 다른 버전에 대한 솔루션 버전의 품질에 대한 방향성을 제공합니다.
    2. 온라인 테스트(즉, A/B 테스트)는 항상 모델이 비즈니스 메트릭에 미치는 영향을 측정하는 가장 좋은 방법입니다.
    3. 기존 추천 시스템과 Personalize 모델을 비교할 때 모든 기록 데이터는 처음에는 기존 접근 방식에 치우쳐 있습니다. 종종 오프라인 메트릭은 사용자가 다른 무언가에 노출되었을 때 수행할 수 있는 작업을 반영하지 않습니다(어떻게 데이터가 이를 반영하지 않을 수 있습니까). 따라서 이러한 효과에 주목할 필요가 있으며, 밴디트 기반 탐색 Personalize는 사용자로부터 유기적으로 더 잘 배울 수 있습니다. 따라서 결과를 측정하기 위해 실제로 테스트를 시작하기 **전에** 몇 주 동안 온라인 테스트를 실행하는 것이 좋습니다.
    4. 자세한 내용은 다음 블로그 게시물을 참조하세요. https://aws.amazon.com/blogs/machine-learning/using-a-b-testing-to-measure-the-efficacy-of-recommendations-generated-by-amazon-personalize/
13. 비용을 최적화하려면 어떻게 해야 하나요?
    1. AUTOML을 사용하지 마세요!
    2. HPO로 시작하지 마세요. 먼저 작동하는 모델을 구축하고 마지막으로 최적화합니다.
    3. 비즈니스 요구 사항에만 따라 재훈련합니다. 자세한 내용은 FAQ 질문을 참조하세요.
    4. 처리량/지연 목표에 부정적인 영향을 미치지 않는 한 프로비저닝된 최소 TPS를 낮게 설정하여 자동 확장에 크게 의존합니다.
    5. 사용 사례가 이메일 마케팅과 같은 다운스트림 배치 프로세스와 부합할 경우 배치 추천을 사용하는 것을 고려하세요. 배치 추천은 솔루션 버전에 대해 실행되므로 캠페인이 필요하지 않습니다.
    6. Amazon Personalize Monitor 프로젝트는 캠페인 프로비저닝을 최적화하고 유휴/유휴 캠페인에 대한 경고 및 삭제를 위한 몇 가지 비용 최적화 기능을 제공합니다.
14. Amazon Personalize에서 캐시를 사용하는 가장 좋은 방법은 무엇인가요? Personalize를 기존 애플리케이션과 어떻게 통합해야 하나요?
    1. [Personalization APIs](_https://github.com/aws-samples/personalization-apis_) 솔루션을 확인하세요. Amazon Personalize 같은 추천 시스템과 애플리케이션 사이에서 작동하며 대기 시간이 짧은 실시간 API 프레임워크입니다. 응답 캐싱, API Gateway 구성, [Amazon CloudWatch Evidently](_https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html_)를 사용한 A/B 테스트, 추론-시간 항목 메타데이터, 자동 상황별 추천 등의 구현 모범 사례를 제공합니다.
15. Personalize를 기존 사용자 환경 또는 다른 추천 시스템과 비교하는 가장 좋은 방법은 무엇인가요?
    1. A/B 테스트는 온라인 메트릭과 비교하여 개인화의 효과를 평가하는 가장 일반적인 기술입니다. [Amazon CloudWatch Evidently]([_https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html_](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html))는 AWS의 A/B 테스트 도구로서 Personalize와 함께 사용할 수 있습니다. [Personalization APIs]([_https://github.com/aws-samples/personalization-apis_](https://github.com/aws-samples/personalization-apis)) 프로젝트는 배포 가능한 솔루션 및 참조 아키텍처를 제공합니다.
16. 증분 레코드는 현재 사용자의 추천에 어떤 영향을 미치나요?
    1. Amazon Personalize를 사용하면  [상호 작용](https://docs.aws.amazon.com/personalize/latest/dg/importing-interactions.html), [사용자](https://docs.aws.amazon.com/personalize/latest/dg/importing-users.html) 및 [항목](https://docs.aws.amazon.com/personalize/latest/dg/importing-items.html)을 점진적으로 가져올 수 있습니다. 이는 새 솔루션 버전이 훈련되었는지 여부와 사용된 훈련 모드 유형에 따라 현재 사용자에 대한 추천에 다양한 방식으로 영향을 미칠 수 있습니다.

|증분	|레시피	|사용 중지되지 않음	|trainingMode=UPDATE 사용 중지	|trainingMode=FULL 사용 중지	|댓글	|
|---	|---	|---	|---	|---	|---	|
|새 사용자 putEvent	|사용자 개인화	|개인화는 1개의 이벤트 후에 시작되지만, 각 이벤트가 기록된 후 PutEvents 호출 후 1~2초 지연된 ~2-5개의 이벤트 후에 더 잘 표시됩니다.	|'재훈련하지 않는 경우'에서 설명하는 효과 이외의 추가 효과는 없습니다.	|개인별 추천	|더 많은 이벤트가 스트리밍될수록 레코드는 더 개인화됩니다. 새 사용자 레코드에 노출 데이터가 포함된 경우 인상 할인은 콜드 스타트 항목에 대해 발생합니다.	|
|새 사용자 putEvent	|개인별 순위	|개인화는 1개의 이벤트 후에 시작되지만, 각 이벤트가 기록된 후 PutEvents 호출 후 1~2초 지연된 ~2-5개의 이벤트 후에 더 잘 표시됩니다.	|-	|개인별 추천	|개인별 순위를 사용하면 고객이 제공한 큐레이션된 리스트에 다시 순위가 매겨질 때(학습된 모델 행동/메타데이터 기능 및 사용자 상호 작용을 기반으로 카탈로그에 있는 항목의 전체 어휘에서 추천이 생성되는 사용자 개인화에 비해) putEvent 레코드의 직접적인 영향을 확인하기가 더 어렵습니다.	|
|새 사용자 putEvent	|SIMS	|-	|-	|추천을 생성하는 모델에 포함	|SIMS는 실제로 개인화를 수행하지 않으므로 PutEvents를 사용하여 새 사용자가 추가되는 상황에서 새 사용자의 이벤트는 재훈련 후에만 유사한 항목 기록에서 고려됩니다.	|
|putUser	|사용자 개인화	|-	|-	|개인별 추천	|putUser를 통해 추가된 사용자는 알려진 상호 작용 기록과 다음 전체 재훈련 후 userID의 조합에 따라 웜 사용자가 됩니다.	|
|putUser	|개인별 순위	|-	|-	|개인별 추천	|putUser를 통해 추가된 사용자는 알려진 상호 작용 기록과 다음 전체 재훈련 후 userID의 조합에 따라 웜 사용자가 됩니다.	|
|putUser	|SIMS	|-	|-	|효과 없음	|SIMS는 실제로 개인화를 수행하지 않으므로 PutUsers를 사용하여 새 사용자가 추가되는 상황에서 새 사용자의 이벤트는 재훈련 후에만 유사한 항목 기록에서 고려됩니다.	|
|putItem	|사용자 개인화	|-	|탐색이 활성화된 경우 탐사용 기간 컷오프를 기준으로 적합한 콜드 스타트 항목으로 나타납니다.	|개인별 추천	|신규/콜드 스타트 항목의 경우 사용자의 상호 작용 기록 및 신규/콜드 스타트 항목의 항목 메타데이터를 기준으로 추천이 개인화됩니다. 콜드 스타트 항목(탐사가 활성화된 경우 탐색 연령 컷오프를 기준으로 적용 가능)은 다음 업데이트 중에 포함됩니다. 콜드 스타트 항목은 탐색 중에 생성된 상호 작용으로 인한 인상 차감을 기반으로 자동으로 업데이트됩니다. 이 가중치는 메타데이터 기반 기능과 비선형적이지만 덜 인기 있는 콜드 스타트 항목과 결합됩니다(인상 필드에 putEvents를 통해 제공됨). 시간이 지남에 따라 탐색 가중치가 줄어듭니다.	|
|putItem	|개인별 순위	|-	|-	|일부 상호 작용 후에만 개인화됩니다.	|-	|
|putItem	|SIMS	|-	|-	|새로운 상호 작용이 모델에 포함되어 공존을 기반으로 유사한 항목 추천을 생성합니다.	|SIMS는 실제로 개인화를 수행하지 않으므로 PutEvents를 사용하여 새 사용자가 추가되는 상황에서 새 사용자의 이벤트는 재훈련 후에만 유사한 항목 기록에서 고려됩니다.	|

## 기술 지원 링크:

1. 전체 샘플: https://github.com/aws-samples/amazon-personalize-samples
2. 시작하기: https://github.com/aws-samples/amazon-personalize-samples/tree/master/getting_started
3. Box 2.0의 POC: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/workshops/POC_in_a_box
4. 사용 사례 기반 노트북: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/core_use_cases
5. 데이터 과학 도구: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/data_science
6. Personalize용 MLOps: https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/ml_ops
7. 모니터링/알림/비용 최적화: https://github.com/aws-samples/amazon-personalize-monitor

## 데모/워크숍:

* 미디어 및 엔터테인먼트
    * Unicorn Flix
        * 인스턴스 실행: [https://unicornflix.amplify-video.com](https://unicornflix.amplify-video.com/)
* 소매
    * 소매 데모 스토어
        * 소스: https://github.com/aws-samples/retail-demo-store
        * 워크숍: https://github.com/aws-samples/retail-demo-store#hands-on-workshops
        * 인스턴스 실행: [http://retaildemostore.jory.cloud/](http://retaildemostore.jory.cloud/#/)

## 기술 파트너:

Personalize를 통해 고객이 프로덕션 환경으로 신속하게 전환하거나 Personalize를 통해 개인화 구현에 대한 ROI를 향상시킬 수 있는 Personalize의 보완 기능을 제공하는 여러 기술 파트너가 있습니다.

### 고객 데이터 플랫폼 - 이벤트 수집/활성화 추천

**Segment**는 [고객 데이터 플랫폼](https://en.wikipedia.org/wiki/Customer_data_platform)입니다. AWS 고급 기술 파트너이며 [디지털 고객 경험](https://aws.amazon.com/advertising-marketing/partner-solutions/)(DCX) 및 [소매](https://aws.amazon.com/retail/partner-solutions/) 컴피턴시를 보유하고 있습니다.

Segment는 다음과 같은 방법으로 Personalize를 지원합니다.

* 이벤트 수집 - Segment의 핵심 기능입니다. 고객은 Segment를 사용하여 웹 앱, 모바일 앱 및 기타 통합 환경에서 클릭스트림 이벤트를 수집합니다. 이러한 이벤트는 수집, 검증 및 고객이 구성한 다운스트림 대상으로 팬아웃됩니다. 이러한 목적지 중 하나는 Amazon Personalize입니다.
* 고객/사용자 프로파일 ID 확인 - Segment는 고객의 사용자에 대한 모든 채널의 이벤트를 보기 때문에 통합된 고객 프로파일을 만들 수 있습니다. 이러한 프로필/정체성은 옴니채널 개인화를 제공할 수 있는 핵심 요소입니다.
* 조직의 다른 마케팅 도구에 걸친 활성화 - 고객이 Segment를 통해 다른 마케팅 도구에 대한 연결을 만들 수 있기 때문에, Segment의 프로필에 개인별 추천을 연결하면 고객과 다운스트림 파트너가 해당 추천을 도구에서 활용할 수 있습니다.

**리소스**

* Segment CTO 동영상: https://www.youtube.com/watch?v=LQSGz8ryvXU
* 블로그 게시물: https://segment.com/blog/introducing-amazon-personalize/
* AWS/Segment 워크숍
    * 실시간 개인화 이벤트: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/1-Personalization/Lab-5-Real-time-events-Segment.ipynb
    * 고객 데이터 플랫폼과 Personalize: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/6-CustomerDataPlatforms/6.1-Segment.ipynb
    * Segment/Personalize(레거시 워크숍): https://github.com/james-jory/segment-personalize-workshop
* 설명서: https://segment.com/docs/connections/destinations/catalog/amazon-personalize/

**mParticle**은 고객 데이터 플랫폼입니다. AWS 고급 기술 파트너이며 [디지털 고객 경험](https://aws.amazon.com/advertising-marketing/partner-solutions/)(DCX) 및 [소매](https://aws.amazon.com/retail/partner-solutions/) 컴피턴시를 보유하고 있습니다.

mParticle은 다음과 같은 방법으로 Personalize를 지원합니다.

* 이벤트 수집 - mParticle의 핵심 기능입니다. 고객은 mParticle을 사용하여 웹 앱, 모바일 앱 및 기타 통합 환경에서 클릭스트림 이벤트를 수집합니다. 이러한 이벤트는 수집, 검증 및 고객이 구성한 다운스트림 대상으로 팬아웃됩니다.
* 고객/사용자 프로파일 ID 확인 - mParticle은 고객의 사용자에 대한 모든 채널의 이벤트를 보기 때문에 통합된 고객 프로파일을 만들 수 있습니다. 이러한 프로필/정체성은 옴니채널 개인화를 제공할 수 있는 핵심 요소입니다.
* 조직의 다른 마케팅 도구에 걸친 활성화 - 고객이 mParticle을 통해 다른 마케팅 도구에 대한 연결을 만들 수 있기 때문에, mParticle의 프로필에 개인화된 권장 사항을 첨부하면 고객과 다운스트림 파트너가 해당 권장 사항을 도구에서 활용할 수 있습니다.

**리소스**

* AWS/mParticle 워크숍
    * 실시간 개인화 이벤트: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/1-Personalization/Lab-6-Real-time-events-mParticle.ipynb
    * 고객 데이터 플랫폼과 Personalize: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/6-CustomerDataPlatforms/6.2-mParticle.ipynb

### 분석/측정/실험

**Amplitude**는 AWS 고급 기술 파트너이며 [Digital Customer Experience](https://aws.amazon.com/advertising-marketing/partner-solutions/)(DCX) 컴피턴시를 보유하고 있습니다. 
Amplitude는 다음과 같은 방법으로 Personalize를 지원합니다.

* 제품 인사이트 - 진폭은 정교한 깔때기 분석을 통해 변환으로 이어지는 이벤트 유형에 대한 가시성을 제공합니다. 이를 통해 고객은 이벤트 분류법을 최적화하고 Personalize에서 모델을 훈련할 적절한 이벤트 및 메타데이터 필드를 선택해야 한다는 인사이트를 얻을 수 있습니다.
* A/B 테스트 평가 - 진폭은 Personalize에 의해 제공되는 개인화된 고객 경험으로 나타낼 수 있는 A/B 테스트의 온라인 측정을 제공합니다.

**리소스**

* 워크숍: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.5-Amplitude-Performance-Metrics.ipynb
* 블로그 게시물: https://aws.amazon.com/blogs/apn/measuring-the-effectiveness-of-personalization-with-amplitude-and-amazon-personalize/

**Optimizely**는 시장을 선도하는 A/B 테스트 플랫폼입니다. AWS 고급 기술 파트너이며 [DCX(Digital Customer Experience)](https://aws.amazon.com/advertising-marketing/partner-solutions/) 컴피턴시를 보유하고 있습니다.

Optimizely는 다음과 같은 방법으로 Personalize를 지원합니다.

* A/B 테스트 결과 - Optimizely의 핵심 제품은 개인화 기법과 같은 실험의 측정 및 보고입니다.
* 특성 플래깅 - 개인화된 환경을 활성화/비활성화합니다.

**리소스**

* 워크숍: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.6-Optimizely-AB-Experiment.ipynb

### 메시징

**Braze**는 시장을 선도하는 메시징(이메일, 푸시, SMS) 플랫폼입니다. AWS 고급 기술 파트너이며 [디지털 고객 경험](https://aws.amazon.com/advertising-marketing/partner-solutions/)(DCX) 및 [소매](https://aws.amazon.com/retail/partner-solutions/) 컴피턴시를 보유하고 있습니다.

Braze는 다음과 같은 방법으로 Personalize를 지원합니다.

* 실시간 통합 또는 배치 통합을 통해 적절한 커뮤니케이션 채널에서 고객에게 개인화된 메시지를 전달합니다.

**리소스**

* Braze 설명서: https://www.braze.com/docs/partners/data_augmentation/recommendation/amazon_personalize/
* AWS ML 블로그 게시물: https://aws.amazon.com/blogs/machine-learning/optimizing-your-engagement-marketing-with-personalized-recommendations-using-amazon-personalize-and-braze/
* AWS Media 블로그 게시물: https://aws.amazon.com/blogs/media/speed-relevance-insight-how-streaming-services-can-master-effective-content-discovery-and-engagement/
* 워크숍: https://github.com/aws-samples/retail-demo-store/blob/master/workshop/4-Messaging/4.2-Braze.ipynb

### 직접 통합

**Magento 2**: Magento 2 확장은 Magento와 AWS 파트너인 Customer Paradigm에 의해 개발되었습니다. 이 확장 기능은 Adobe Magento에서 개발하지 않았습니다.

이 확장은 온프레미스, 다른 클라우드 공급자 또는 AWS에서 실행되는 Magento 2 스토어에 쉽게 설치할 수 있습니다. Amazon Personalize는 항상 고객의 AWS 계정에서 액세스합니다.

**리소스**

* 파트너 웹 사이트: https://www.customerparadigm.com/amazon-personalize-magento/
* Magento Marketplace: https://marketplace.magento.com/customerparadigm-amazon-personalize-extension.html


**Shopify:** [Obviyo](https://www.obviyo.com/)(이전 HiConversion) Shopify 스토어프런트에 대한 Personalize와의 관리형 통합을 구축했습니다. 즉, Obviyo는 AWS 환경에서 Personalize를 관리하고 Shopify 상인은 Obviyo에게 Personalize를 통해 제공되는 개인화 기능에 대한 비용을 지불합니다.

**리소스**

* 파트너 웹 사이트: https://www.obviyo.com/

**WooCommerce(베타):** [WP-Engine](https://wpengine.com/)은 몇 번의 클릭만으로 Personalize의 제품 추천을 WooCommerce 사이트에 추가할 수 있는 AWS for WordPress 플러그인에 Personalize 통합 기능을 내장했습니다.

**리소스**

* WP-Engine 리소스 페이지: https://wpengine.com/resources/webinar-amazon-com-personalization-for-your-woocommerce-store/
