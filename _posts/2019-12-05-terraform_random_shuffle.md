---
title: terraform random_shuffle로 랜덤하게 리소스 가져오기
layout: post
tags: [terraform]
categories: terraform
---
다음과 같이 리소스가 정의되어 있을 때

```hcl
resource "aws_subnet" "public" {
  count = "${length(var.subnets_public_cidr)}"
  vpc_id = "${aws_vpc.main.id}"
  cidr_block = "${element(var.subnets_public_cidr, count.index)}"
  availability_zone = "${element(var.azs, count.index)}"
  map_public_ip_on_launch = true
  tags = {
    Name = "public-${element(var.azs, count.index)}"
  }
}

resource "aws_instance" "bastion" {
  key_name = "${var.key_pair_name}"
  ami = "${var.bastion_ami}"
  instance_type = "${var.bastion_instance_type}"
  tags = {
    Name = "bastion"
  }
  vpc_security_group_ids = ["${aws_security_group.bastion.id}"]
  subnet_id = "${aws_subnet.public.0.id}"
}
```

bastion ec2의 서브넷을 index를 지정하여 하나를 선택했는데 0으로만 지정하면 하나의 서브넷에 몰리고 다른 숫자로 하려니 subnet count에 따라 유연하게 설정이 가능하지 않았다.
이럴때 [random_shuffle][random_shuffle official]을 사용하면 생성된 subnet중에 하나를 랜덤하게 설정할 수 있다.

<!--more-->

```hcl
# random_shuffle resource 생성
resource "random_shuffle" "public_subnet" {
  input = "${tolist(aws_subnet.public.*.id)}"
  result_count = 1
}

# subnet_id 부분에서 random_shuffle을 사용하도록 수정
resource "aws_instance" "bastion" {
  # 생략..
  subnet_id = "${element(random_shuffle.public_subnet.result, 0)}"
}
```

`random_suffle`의 `input`은 string list를 전달해야 하므로 `tolist`를 사용하고 input 중에 하나만 선택하므로 `result_count`를 1로 설정한다.
결과는 `result`로 가져올 수 있고 `result`는 결과가 1개라도 list형태로 리턴이 되므로 subnet_id로 지정할 때는 `element`를 사용해야 한다.

[random_shuffle official]: https://www.terraform.io/docs/providers/random/r/shuffle.html
