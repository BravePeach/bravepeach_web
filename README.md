# bravepeach_web
BravePeach WebServer with Django

## Settings for Developers

### Pre-requisites

```bash
$ sudo apt install build-essential python3-dev python3-pip git git-flow libssl-dev libffi-dev libmysqlclient-dev
```

### Instructions

```bash
$ git clone [this repo]
$ cd web
$ git flow init
[Several Enters]
$ virtualenv .venv
$ . .venv/bin/activate
(.venv) $ pip install -r requirements.txt
```

### Django Setting
[이곳](https://dayone.me/20Tcz1k) 을 참고해 세팅을 설정하면 된다. [샘플](bravepeach/settings/example.py) 을 제공하고 있으니 복사해 사용하면 편리하다.

기본 세팅파일은 `bravepeach/settings/local.py` 를 이용하도록 되어 있으며,

다른 세팅을 기본으로 이용하려면 [bravepeach/wsgi.py](bravepeach/wsgi.py), [manage.py](manage.py) 를 수정하면 된다.

혹시 Pycharm 에서 직접 서버를 켠다면 Edit Configurations 에 들어가서 Environment variables 도 변경해주어야 에러가 안 난다.
