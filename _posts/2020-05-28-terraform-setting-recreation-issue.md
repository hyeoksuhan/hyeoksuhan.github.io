---
title: Terraform Elastic Beanstalk setting 매번 재생성 되는 이슈
layout: post
tags: [terraform,elasticbeanstalk]
categories: terraform
---
### 이슈
Terraform으로 Elastic Beanstalk setting이 plan/apply시 변경사항이 없어도 매번 삭제 후 재생성 되는 이슈가 있었다

현재 구축된 Beanstalk의 setting은 ignore 처리되어 있어서 그동안 큰 문제 없이 관리되고 있었는데 플랫폼 자동 업데이트 설정을 위한 ServiceRole을 변경하려고 하면서 다시 이슈가 되었다

### 원인
검색해 보니 terraform 0.12버전의 버그이며 setting을 ignore 처리해서 우회하는 방법을 쓰는 사람들도 있었다.
하지만 지금은 setting의 ServiceRole 변경이 필요했으므로 다른 방법이 필요해서 좀 더 찾아봤다
<!--more-->

### 해결
EB terraform 모듈에 같은 이슈 해결을 위해 [수정된 내용][PR]을 참고해서 수정해서 해결했다. 각 setting에 `resource=""`를 추가하고 list는 sort를 이용해서 정렬되도록 수정했다

어떤 문제인지 느낌은 오는데 정확히 설명이 안된다. 하하


### +
- setting을 ignore 처리한 이유
   - 이미 구축되어 있는 EC2를 EB로 옮기느라 환경변수가 모두 포함되어 있었고 상대적으로 자주 변경 되었기에 모든 개발자가 terraform으로 sync를 맞추는 것보다 웹콘솔로 변경하기로 했기 때문. 게다가 setting으로 설정된 대부분의 내용은 최초 구축 후 변경이 거의 필요없어서.

   - ignore 처리 방법
   ```
   lifecycle {
       ignore_changes=[
          "setting"
       ]
   }
   ```

- 언급된 것처럼 상대적으로 자주 변경되는 환경변수, 자동으로 플랫폼 버전이 업데이트가 되는등 terraform 소스가 유일한 변경점이 되지 않을 때, sync를 맞추기 불합리하다는 생각이 든다. 동시에 EB는 웹콘솔, eb cli등으로 쉽게 구축할 수 있는데 이런 도구를 이용해 관리하는게 맞나라는 생각도 든다

  찾아본 바로는 현재는 클라우드의 인프라의 상태를 가져올 수는 있느나 상태에만 적용이 되고 실제 소스로 가져올 수는 없다. 그러면 plan을 할 때마다 수동으로 terraform 소스를 수정해서 동기화 하는 방법 밖에 없지만 인프라를 코드로 관리한다는 원래 취지를 생각하면 이렇게라도 하면서 더 좋은 방법이 나오기를 기다려 본다.

[PR]:https://github.com/cloudposse/terraform-aws-elastic-beanstalk-environment/pull/114

