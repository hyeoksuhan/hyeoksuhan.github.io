---
title: nodejs circular module dependency
layout: post
tags: [nodejs]
categories: nodejs
---
Nodejs로 구현된 서버에 API 추가를 위해 개발을 진행하던 중에 기존 작성된 테스트케이스가 실패했다.

전혀 연관성이 없어 보이는 모듈이 갑자기 빈 object를 반환하여 모듈 참조값이 undefined가 되는것이 원인이었다.

리팩토링이 아닌 상황에 발생해서 의아했다. 물론 개발을 하다보면 기존 기능에 대해 side effect는 충분히 발생할 수 있지만, 전혀 새로운 도메인의 내용을 추가 하는 상황이여서 이해가 되지 않았다. 
에러 메시지를 참조하여 디버깅 해본 결과 nodejs의 circular module dependency(순환 참조?) 문제였다.

즉, a, b, c, d 모듈이 있을 때 `a` -> b -> c -> `a`로 참조가 되어 문제가 발생한 것이었다.

왜 이런 순환참조가 발생한 것일까?
<!--more-->

해당 모듈들을 재검토한 결과 모듈의 관심사가 제대로 분리 되지 않았던 것이 원인이었다고 판단하고 모듈을 리팩토링하여 근본적인 문제를 해결했다.
하지만 어쩔 수 없이 발생할 수도 있을 것이라는 생각도 들고 추후에 개발단계에서 미리 방지하기 위한 학습을 위해 몇가지 테스트를 해봤다.

테스트 전에 직, 간접적으로 아래의 내용을 알아두면 도움이 된다.
1. require는 동기 로직이다.
2. 모듈은 한번 로드가 되면 캐싱된다.
3. module.exports의 기본값은 {} 이다.
4. Nodejs에서는 순환참조를 허용하며 순환참조에 의한 무한호출이 일어나지 않는다.

먼저 아래와 같이 상호 참조를 하는 2개의 모듈을 만든다.

**a.js**
```js
console.log('[a.js] before require b');
const b = require('./b');

console.log('[a.js] after require b:', b);

module.exports = {
  print: msg => {
    console.log(`[a.js] ${msg} in a.js`);
  },
};
console.log('[a.js] after export a.js');
```

**b.js**
```js
console.log('[b.js] before require a');
const a = require('./a');

console.log('[b.js] after require a:', a);

module.exports = {
  print: msg => {
    console.log(`[b.js] ${msg}`);
  },
};
console.log('[b.js] after export b.js');
```

> 실행

```bash
$ node a.js
```
> 결과

```bash
[a.js] before require b
[b.js] before require a
[b.js] after require a: {}
[b.js] after export b.js
[a.js] after require b: { print: [Function] }
[a.js] after export a.js
```

결과를 보면 a모듈에서 b모듈을 로드했고, b모듈에서 a모듈을 로드했으나 a의 모듈은 비어있었다. b모듈의 로드가 끝나고 다시 a모듈이 b모듈을 로드한 다음 로직이 실행이 되었고 a모듈에서는 b모듈이 정상적으로 로드가 된 것을 볼 수 있다.

위 결과를 정리 해보면
1. require의 동작이 동기로 동작했기 때문에 위와 같은 순서로 동작을 했다
2. 모듈이 완전히 로드가 되기전에 require로 모듈로드가 되면 빈 오브젝트를 리턴한다. *(일반적인 상황에서는 require가 동기 로직이기 때문에 발생하지 않을 것이다)*

2번을 되짚어볼 필요가 있는데 모듈이 아직 로드가 되지 않았으므로 (module.exports가 실행되지 않음) 디폴트 값인 {}가 리턴되었고 module.exports가 끝난 후에는 정상적으로 사용이 가능한지 확인해보기 위해 main.js를 추가해서 테스트 해보았다.

**main.js**
```js
const a = require('./a');
const b = require('./b');

console.log({a});
console.log({b});
```

> 실행

```bash
$ node main.js
```

> 결과

```bash
[a.js] before require b
[b.js] before require a
[b.js] after require a: {}
[b.js] after export b.js
[a.js] after require b: { print: [Function] }
[a.js] after export a.js
{ a: { print: [Function] } }
{ b: { print: [Function] } }
```

module.exports가 실행되기전에 해당모듈에 대한 참조가 일어나면 디폴트값이 {}가 리턴되고 module.exports가 완료된 후에는 정상적으로 동작함을 알 수 있었다.
이 결과를 바탕으로 a.js에서 module.export를 먼저 실행하고 b모듈을 로드하도록 아래와 같이 수정하면 문제가 해결할 수도 있다.

**a.js**
```js
module.exports = {
  print: mag => {
    console.log(`[a.js] ${msg} in a.js`);
  },
};
console.log('[a.js] after export a.js');

console.log('[a.js] before require b');
const b = require('./b');

console.log('[a.js] after require b:', b);
```

> 실행

```bash
$ node a.js
```

> 결과

```
[a.js] after export a.js
[a.js] before require b
[b.js] before require a
[b.js] after require a: { print: [Function: print] }
[b.js] after export b.js
[a.js] after require b: { print: [Function: print] }
```

모듈 순환참조에 대한 내용은 [공식문서][official]에서도 확인할 수 있었다.

[official]: https://nodejs.org/api/modules.html#modules_cycles
