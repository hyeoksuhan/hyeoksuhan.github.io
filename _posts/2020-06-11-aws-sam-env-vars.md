---
title: AWS SAM aws-sdk사용시 람다 로컬테스트
layout: post
tags: [aws,sam]
categories: aws
---
[aws-sdk-conf-creds]:https://github.com/aws/aws-sdk-go#configuring-credentials
### 환경
```
$ sam --version
SAM CLI, version 0.52.0
```

<br/>

### Issue
1. 환경변수 로딩
  - 람다의 local invoke를 위해 --env-vars <json file> 옵션을 추가했으나 람다에서 환경변수로 로드되지 않음
2. aws-sdk의 credentials 참조를 위한 코드 구조

<!--more-->
<br/>

### 환경변수 로딩
1. 환경변수는 리소스별로 분리해서 json파일로 설정 가능한데 이때 람다이름이 아닌 리소스명으로 지정해야 함
2. 로딩이 되지 않은 결정적인 이유인데 template의 Environment에 정의되어 있어야지만 overwrite 되어 환경변수로 로드됨

<br/>

### 람다에서 aws-sdk 사용시 로컬테스트
1. RDS API를 쓰므로 기능을 테스트 하기 위해서 실제 테스트 환경의 Aurora를 대상으로 API 테스트
2. 현재상황: test, prod환경의 AWS 계정이 다름. 각 credential은 환경별 profile로 분리되어 있음
3. 람다를 로컬에서 invoke시 로컬의 test profile에 있는 credential key를 사용해야 하는 상황
  - aws-sdk는 credential을 chaining을 통해 정해진 순서대로 로드. [관련내용][aws-sdk-conf-creds]
  - 환경변수 -> ~/.aws/credentials -> assume role
4. profile 옵션없이 sam local invoke를 하면 ~/.aws/credeitnals의 default profile의 key를 aws-sdk에서 참조할 수 있도록 환경변수에 로드해줌
5. test profile을 사용하기 위해 sam local invoke --profile test를 하니 test profile의 credential이 환경변수로 로딩됨을 확인. 운영환경에서는 key가 없으므로 위와 같이 local invoke시에 환경변수로 credentials가 로딩 되지 않는다면 코드 분기를 타서 처리를 하거나 하는 번거로움이 있는데 sam에서 환경변수로 로드해주니까 하나의 코드로 로컬테스트/운영 적용까지 되어서 편리함.
