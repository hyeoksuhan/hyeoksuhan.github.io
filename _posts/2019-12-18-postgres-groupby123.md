---
title: postgres group by 1,2,3
layout: post
tags: [postgres]
categories: db
---
Postgres는 `group by`와 `order by`에서 sql statement의 column order의 값을 참조할 수 있다.
즉, 일별 가입자수를 카운팅하는 아래와 같은 sql문이 있을때

```sql
SELECT created_at::date, count(*)
FROM "user"
WHERE type = 'email'
GROUP BY created_at::date
ORDER BY created_at::date;
```

statement의 첫번째 coloum order는 `create_at::date`이고 이것을 `group by`와 `order by`에서 참조하여 중복된 쿼리문을 생략해서 아래와 같이 쓸 수 있다.

<!--more-->

```sql
SELECT created_at::date, count(*)
FROM "user"
WHERE type = 'email'
GROUP BY 1
ORDER BY 1
```

쿼리결과
```
created_at | count
------------------
2019-12-16 | 18700
2019-12-17 | 19000
2019-12-18 | 23920
```