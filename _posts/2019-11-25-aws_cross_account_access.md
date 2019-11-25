---
title: AWS Cross-Accounts Access (교차계정접근)
layout: post
tags: [AWS]
categories: AWS
---
인프라의 보안을 위해 서버 환경별(dev, staging, prod등)로 AWS 계정을 분리하는 경우가 있는데, 이때 [AWS Organization][AWS Organizations]을 사용하면 여러 계정들을 쉽게 관리할 수 있다. 마스터 계정을 하나 두고 다른 계정들을 추가하는 형식으로 쉽게 계정을 추가 및 관리가 가능하고 요금도 마스터 계정 한곳에서 계산된다.
계정 추가를 위해서는 각각의 이메일 계정이 필요한데 [Email Alias][Email Alias]로도 가입이 가능하다.

AWS Organization에서 계정을 추가 추가하고, AWS 로그인 콘솔에서 `다른계정으로 로그인` -> `이메일 주소 입력` -> `forgot password` 순으로 진행하여 비밀번호 재설정 절차를 진행하면 새 password 설정 링크가 이메일로 수신된다.

[SCP][SCP](Service Control Policy)를 이용하여 계정 및 각 계정에 포함된 IAM 사용자, OU 단위로 접근할 수 있는 서비스와 작업을 지정해 줄 수 있다. SCP로 권한을 제한하면 영향을 받는 계정의 IAM에서 그 이상의 권한을 줘도 접근이 불가능하다.

이렇게 여러개의 계정을 소유하고 있을때 Cross-Accounts Access(교차계정접근)를 설정하면 사용자는 다른 AWS 계정의 리소스에 액세스하기 위해 한 계정에서 로그아웃하고 다른 계정에 로그인할 필요가 없어진다.
<!--more-->

교차계정접근은 크게 3단계로 이루어진다. 이해를 쉽게 하기 위해 dev환경의 계정으로 AWS 콘솔에 로그인 한 후 prod환경의 계정으로 교차계정접근을 하려고 예를 들어보면,
  1. **policy 생성**: prod에서 dev에게 접근 허용할 리소스에 대한 policy를 생성
  2. **role 생성**: prod에서 dev 계정을 trusted entity로 설정하고 1번에서 만든 policy를 연결
  3. **IAM group에 역할 부여**: dev계정의 IAM group에 2번의 ARN을 inline policy로 등록하여 권한을 부여

1,2,3은 각 환경별 관리자 권한 계정으로 로그인하여 진행해야 한다.

위 내용에 대한 상세 내용은 아래의 공식 문서에 잘 성명되어 있다.

> 공식문서

[자습서: IAM 역할을 사용한 AWS 계정 간 액세스 권한 위임][CAA tutorial]

[AWS 관리 콘솔에서 교차 계정 접근(Cross-Accounts Access) 활용하기][CAA blog]

[AWS Organizations]: https://aws.amazon.com/ko/organizations/
[SCP]: https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scp.html
[Email Alias]: https://www.youtube.com/watch?v=oQt-0qysykQ
[CAA tutorial]: https://docs.aws.amazon.com/ko_kr/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html
[CAA blog]: https://aws.amazon.com/ko/blogs/korea/cross-account-access-in-the-aws-console/
