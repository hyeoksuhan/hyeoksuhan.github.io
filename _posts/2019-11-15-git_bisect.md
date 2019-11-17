---
title: git bisect로 문제가 있는 커밋 찾기
layout: post
tags: [git]
categories: git
---
현재 HEAD가 가리키는 커밋에서 typescript build시 문제가 있었다.
최근에 ts-node-dev로 빌드없이 개발을 진행하다보니 언제부터인가 빌드를 해보지 않은 것이 문제였다.

문제가 생긴 커밋을 찾아 변경된 부분이 무엇인지 확인하기 위해 `git bisect`를 사용했다.

`git bisect`는 이진탐색 방법으로 HEAD를 옮겨가며 문제가 발생한 최초 커밋을 찾을 수 있도록 도와주는 유용한 명령어다.
<!--more-->
아래와 같은 순서로 문제의 커밋을 찾았다.
1. `git bisect start`로 탐색 시작을 설정
2. 문제가 있는 커밋으로 HEAD를 이동시킨 후 `git bisect bad`를 실행하여 문제가 있는 커밋을 설정
3. 문제가 없었던 커밋을 찾아 `git bisect good <commit hash>`로 문제가 없는 커밋을 설정. 언제 문제가 발생했는지 기억이 나지 않아서 가장 첫번째 커밋으로 설정
4. 이진탐색이 시작되며 자동으로 checkout 해주는데 문제가 있는지 테스트를 해보고 문제가 있으면 `git bisect bad`, 없으면 `git bisect good`을 실행.
`git bisect bad`를 하면 HEAD가 가리키던 커밋 이전으로 범위를 좁히고 good을 하면 HEAD 커밋이후로 범위를 좁힌다.
bisect의 목적이 처음 문제가 발생한 commit을 찾아준다는 것을 보면 동작방식을 이해할 수 있다.


(위의 1,2,3 절차는 `git bisect start <bad> <good>` 명령 하나로 실행할수도 있다.)

이번에 문제가 생긴경우는 build의 문제라서 checkout 될때마다
```bash
$ rm -rf node_modeuls
$ npm i
$ npm run build
```
를 실행해줬는데 찾아보니 프로젝트가 정상적으로 수행되면 0을 반환하고 문제가 있을 경우 1을 반환하는 스크립트를 만들면 `git bisect` 과정을 완전히 자동화 할 수 있다고 한다.

```bash
$ git bisect start <bad> <good>
$ git bisect run <script>
```
위와 같이 하면 문제가 생긴 첫 커밋을 찾을 때까지 checkout할 때마다 \<script\>를 실행한다.

**test-error.sh**
```bash
#!/bin/bash

rm -rf node_modules
npm i
npm run build
```
`npm run build` 자체가 위에서 설명하는 스크립트의 조건을 만족하므로 위와 같이 스크립트를 실행하고 테스트 해보았다.

이전에 수동으로 문제를 찾은 후 commit을 한 상태라 <bad>에 HEAD^를 넘겨줬다.
```bash
$ git bisect start HEAD^ c4002f1
$ git bisect run ./test-error.sh
```
run parameter로 스크립트 파일을 지정할 때는 반드시 경로를 지정해줘야 한다. 그렇지 않으면 커맨드로 인식하여 정상동작하지 않았다.

위와 같이 실행하니 몇차례 npm install이 실행되더니 수동으로 했을때와 동일한 커밋을 문제의 커밋으로 찾아줬다.

문제가 된 부분은 typeorm을 cli로 설정하면서 package.json에 typescript와 @types/node의 버전이 낮아져서 발생한 문제였다.

테스트용 코드라 신경을 많이 안썼는데 husky와 연동하여 pre-commit시 빌드 적용 같은 개발 보조도구 설정의 중요성을 한번 더 느꼈다.
git bisect는 자주 쓸일은 없겠지만 알아두면 수백, 수천개의 커밋속에서 이슈가 있는 커밋을 쉽게 찾을 수 있을 것이다.
