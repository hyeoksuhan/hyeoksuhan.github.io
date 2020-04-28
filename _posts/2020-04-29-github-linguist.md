---
title: github repo에 사용된 언어 통계 보정
layout: post
tags: [github,linguist]
categories: github 
---
Typescript project의 github 저장소에 아래와 같이 언어 통계가 표시 되었다
![Image Alt](/images/20200429-1.png){: width="50%" height="50%"}

검색해 보니 github의 language stats bar는 github에서 오픈소스로 개발한 [linguist](https://github.com/github/linguist)를 사용해서 통계를 낸다고 한다

언어 통계를 낼 때 파일의 갯수보다는 사이즈 비율로 통계를 내기 때문에 테스트 코드의 데이터 생성을 위한 backup sql의 사이즈가 컸기 때문에 TSQL 프로젝트가 되어버렸던 것이다

이대로 두어도 큰 문제는 없으나 통계가 제대로 되어야
1. 이 프로젝트의 대표 언어를 한눈에 알 수 있고 
2. github 전체 언어 통계와 검색 결과에도 영향을 미칠 수 있어서 (비록 private repo지만) 

<br>언어 통계를 보정해 보기로 했다

먼저 `.gitattributes` 파일을 생성해서 sql을 linguist-vendored로 지정하면 linguist가 통계를 낼 때 무시한다고 한다
(이외에도 여러가지 방법으로 통계 기준을 변경할 수 있음)

아래와 같이 .gitattributes를 생성한다
```bash
cd /path/to/project
vi .gitattributes
```
<!--more-->

**.gitattributes**
```
*.sql linguist-vendored
```

그리고 push를 했더니 적용이 안된다

이래저래 바꿔서 remote branch에 push를 해도 적용이 되지 않는다

계속 remote에 push를 해서 테스트할 수 없어서 linuist를 로컬에 설치해서 테스트 해보았다

1. install dependencies
```bash
brew install cmake pkg-config icu4c
```

2. install linguish
```bash
(sudo) gem install github-linguist
```

2에서 다음과 같은 에러가 나며 설치가 되지 않았다
```
Building native extensions. This could take a while...
ERROR:  Error installing github-linguist:
  ERROR: Failed to build gem native extension.

    current directory: /Library/Ruby/Gems/2.6.0/gems/charlock_holmes-0.7.7/ext/charlock_holmes
/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/bin/ruby -I /System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/lib/ruby/2.6.0 -r ./siteconf20200428-9020-1clljtn.rb extconf.rb
checking for -licui18n... yes
checking for unicode/ucnv.h... yes
checking for -lz... yes
checking for -licuuc... yes
checking for -licudata... yes
creating Makefile

current directory: /Library/Ruby/Gems/2.6.0/gems/charlock_holmes-0.7.7/ext/charlock_holmes
make "DESTDIR=" clean

current directory: /Library/Ruby/Gems/2.6.0/gems/charlock_holmes-0.7.7/ext/charlock_holmes
make "DESTDIR="
compiling converter.c
compiling encoding_detector.c
compiling ext.c
compiling transliterator.cpp
In file included from transliterator.cpp:1:
In file included from ./common.h:9:
In file included from /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/include/ruby-2.6.0/ruby.h:33:
In file included from /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/include/ruby-2.6.0/ruby/ruby.h:24:
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/include/ruby-2.6.0/universal-darwin19/ruby/config.h:413:31: error: invalid suffix on literal; C++11 requires a space between literal and identifier [-Wreserved-user-defined-literal]
#define RUBY_ARCH "universal-"RUBY_PLATFORM_OS
                              ^

/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/include/ruby-2.6.0/universal-darwin19/ruby/config.h:414:35: error: invalid suffix on literal; C++11 requires a space between literal and identifier [-Wreserved-user-defined-literal]
#define RUBY_PLATFORM "universal."RUBY_PLATFORM_CPU"-"RUBY_PLATFORM_OS
                                  ^

/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/include/ruby-2.6.0/universal-darwin19/ruby/config.h:414:55: error: invalid suffix on literal; C++11 requires a space between literal and identifier [-Wreserved-user-defined-literal]
#define RUBY_PLATFORM "universal."RUBY_PLATFORM_CPU"-"RUBY_PLATFORM_OS
                                                      ^

In file included from transliterator.cpp:1:
In file included from ./common.h:9:
In file included from /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/include/ruby-2.6.0/ruby.h:33:
In file included from /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/include/ruby-2.6.0/ruby/ruby.h:2111:
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/include/ruby-2.6.0/ruby/intern.h:56:19: warning: 'register' storage class specifier is deprecated and incompatible with C++17 [-Wdeprecated-register]
void rb_mem_clear(register VALUE*, register long);
                  ^~~~~~~~~
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/include/ruby-2.6.0/ruby/intern.h:56:36: warning: 'register' storage class specifier is deprecated and incompatible with C++17 [-Wdeprecated-register]
void rb_mem_clear(register VALUE*, register long);
                                   ^~~~~~~~~
2 warnings and 3 errors generated.
make: *** [transliterator.o] Error 1

make failed, exit code 2

Gem files will remain installed in /Library/Ruby/Gems/2.6.0/gems/charlock_holmes-0.7.7 for inspection.
Results logged to /Library/Ruby/Gems/2.6.0/extensions/universal-darwin-19/2.6.0/charlock_holmes-0.7.7/gem_make.out
```

에러메시지를 확인해 보니 루비관련.. 헤더파일의 전처리기 정의에 문제가 있어 보였고 검색을 통해 아래와 같이 헤더파일을 직접 수정하여 해결하였다

```bash
sudo vi /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk/System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/include/ruby-2.6.0/universal-darwin19/ruby/config.h
```

413, 414 line의
```c
#define RUBY_ARCH "universal-"RUBY_PLATFORM_OS
#define RUBY_PLATFORM "universal."RUBY_PLATFORM_CPU"-"RUBY_PLATFORM_OS
```
를

```c
#define RUBY_ARCH "universal-" RUBY_PLATFORM_OS
#define RUBY_PLATFORM "universal." RUBY_PLATFORM_CPU "-" RUBY_PLATFORM_OS
```

로 수정하니 설치가 되었다 (just 공백 추가)

위의 config.h의 경로는 os의 버전과 ruby의 버전에 따라 바뀔 수 있으니 적절하게 찾아가서 수정해야 한다

이제 문제의? project repo로 이동해 github-linugist를 실행해 보았다

주의할 점은 현재 파일을 기준으로 통계를 내는 것이 아니라 `git의 HEAD pointer를 기준으로 계산`을 하므로 commit을 하고 실행해야 한다
```bash
cd /path/to/project
github-linguist
```


![Image Alt](/images/20200429-2.png){: width="30%" height="30%"}

해결

된 줄 알았으나

local에서는 잘 적용이 된 것으로 결과가 나왔지만 remote repo는 통계가 그대로 였는데, 낮은 우선순위의 background job으로 등록되어 적용에 시간이 좀 걸린다고 하니 믿고 기다려 보기로 한다

