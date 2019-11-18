---
title: terraform 리소스의 count를 줄이면 어떤 리소스가 삭제될까
layout: post
tags: [terraform]
categories: terraform
---
아래와 같이 AWS 인스턴스가 terraform으로 4대가 생성되어 있다.
```hcl
resource "aws_instance" "api_server" {
  ami = "${data.aws_ami.api.id}"
  instance_type = "${var.api_instance_type}"
  tags = {
    Name = "api-${count.index + 1}"
  }
  count = 4
}
```
여기서 tag.Name이 `api-4`인 ec2 instance를 삭제 하려면 어떻게 해야할까?

정답은 count를 4에서 3으로 줄이는 것이고, 3으로 줄이게 되면 마지막 index에 위치한 instance 즉, `aws_instance.api_server[3]`이 삭제가 된다.
<!--more-->

당연하게 보일 수 있겠지만 처음에 `api-4`를 삭제하려고 했을 때 count를 줄이면 AWS auto scaling group의 기본 정책처럼 제일 오래된 인스턴스
를 삭제할것 같다는 생각을 했었다. 하지만 count를 줄였을 때 그냥 logical하게 동작해서 마지막 index의 인스턴스를 삭제가 되었다.
terraform이 AWS만 지원하는것이 아니기도 하고 굳이 그런 정책을 따를 이유가 없다는 생각이 뒤늦게 들었다.

왜 그렇게 작동할까 생각해보다가 state file, plan의 설명을 읽어보았으나 명확히 와닿지 않아서 테스트를 해본 결과를 정리해본다.

state파일은 실제 클라우드에 구성되어 있는 리소스와 .tf파일의 리소스를 맵핑 하는 역할을 하고, sync할 때 중심이 된다.
위 설정파일에서 count가 3이고, 생성 및 sync가 정상적으로 되어 state 파일의 `aws_instance.api_server[0]`, `aws_instance.api_server[1]`, `aws_instance.api_server[2]`이 각각 api-1, api-2, api-3에 맵핑이 되어있을 때,

1. AWS 콘솔에서 instance를 하나 삭제하고 `terraform plan`을 실행하면 state에 관리되고 있는 instance가 삭제된것을 감지하고 새로운 instance를 생성을 계획함

2. `terraform state rm`으로 특정 instance의 state를 삭제하면 거기에 맵핑되어 있던 instance는 더이상 트랙킹 되지 않은 상태가 되고 `terraform plan`시 그 삭제된 state에 맵핑되는 새로운 instance 생성을 계획함

3. 특정 instance의 state를 삭제하고 count도 같이 1만큼 줄이면 코드의 카운트에 맞게 **state의 index를 차례대로 맞추는 작업을 한다.**
 즉, 위 코드에서 count가 4이고 삭제하는 index가 1이고 count를 3으로 줄인 후 plan을 하면 남은 state의 index 0, 2, 3를 순차적으로(0, 1, 2) 맞추기 위해 새로운 인스턴스를 생성하고 `aws_instance.api_server[1]`에 맵핑, `aws_instance.api_server[3]` 삭제를 계획힌다.
 만일 삭제하는 index가 마지막 인덱스 즉, 3이고 count를 하나 줄이고 plan을 했을 때는 `no changes`가 출력되고 plan에 변화가 없다.


위같은 동작 방식 때문에 만약에 삭제하려는 resource가 count의 마지막 index가 아닌 리소스이면 삭제가 어려울 것 같다.
그러므로 count로 여러 리소스를 생성했을때 count를 줄이면 마지막 index의 리소스가 삭제됨을 인지하고 있는 것이 좋다고 생각한다. 어차피 완전 똑같은 리소스가 생성이 되므로 특정 index의 리소스를 삭제할 일은 거의 없을 것이다.

단순하게 생각하면 쉬운 문제였지만 state의 필요성과 동작 방식을 다시 한번 생각해보는 좋은 기회였다.
