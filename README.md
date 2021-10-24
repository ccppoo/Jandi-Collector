# Jandi-Collector

admin user list with Google SpreadSheet

## Discord 명령 목록

명령은 REST API와 유사한 형태를 가지고 만들었습니다.

| Protocol |      |        |     |        |       |
| :------: | :--: | :----: | :-: | :----: | :---: |
|   REST   | POST | DELETE | GET |  PUT   |       |
|  Jandi   | MAKE | REMOVE | GET | UPDATE | BUILD |

BUILD 커맨드는 디스코드 UI가 CMD와 달리 일반 채팅과 같이

봇과 상호작용을 통해, (봇이 state를 임시로 저장하는 형식으로)

한 줄로 명령을 내리는 대신 차례 차례 커맨드를 만들 수 있는(Build)

엔트리 포인트에 진입하는 명령어입니다.

---

### Entry Command, 디스코드 봇 명령어 시작 커맨드

Jandi-Collector는 Discord에서 Jandi-Bot이라는 이름으로 작동하며,

디스코드 내 다른 일반 유저의 채팅과 혼선을 방지하기 위해서

**_!_**, 느낌표를 시작으로 명령을 시작합니다.

명령을 내리기 위해서는 후술할 옵션과 함께 사용되어야 합니다.

#### !make

!make : 맴버(사용자), 이벤트, 등(future : 그룹, ...)

#### !remove

!remove : 맴버(사용자),

#### !get

!get : 맴버(사용자) 정보, 인증 횟수, 등

#### !update

!update : 맴버(사용자) 오늘 인증 횟수 등록

#### !build

!build : 한 줄의 명령어 대신 채팅과 같은 형식으로 옵션을 차례 차례 물어보는 것

---

### Option, 옵션

#### --user || -u : 사용자

list 형태로 복수로 옵션을 지정하거나, 문자열로 지정 가능

Example :

    --user=[nickname, new_user] / --user=nickname

조합 가능 한 옵션 :

    !get
        --user  --commit    --date={value} : 해당 날짜 커밋 여부

        --user  --commit    --date={value} -D : 해당 날짜 ~ +D 일 간 커밋 횟수

#### --event || -e : 이벤트

이벤트 이름, 지정하면 사용 가능,

이벤트 만들기

    --type || -t : Any(아무때나), Annually(매년), 등 ... 추가 예정

이벤트 지정(기본값 : 현재 진행되고 있는 이벤트)

---

#### 추가 옵션

    -count || -c 커밋 인증 횟수 / 커밋 등록 가능

    --date || -d 시작 날짜:
        -d=Today || Tommorow || ISO 8601 Date Format
    --duration || -D 지속 일 수 :
        !make --event=commit --count=3 -d=2021-11-13 -D=8
        == 2021-11-13 ~ 2021-11-20 까지 진행되고, 인증을 3번해야하는 이벤트
