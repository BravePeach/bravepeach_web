# bravepeach_web
BravePeach WebServer with Django

## Settings for Developers

### Pre-requisites

```bash
$ sudo apt install build-essential python3-dev python3-pip git git-flow libssl-dev libffi-dev libmysqlclient-dev npm
$ sudo npm install -g less
$ lessc # installation test
```
**Note**
`lessc` 명령어를 입력했을 때 `node` 를 찾을 수 없다는 에러가 발생하면 
`$ sudo vi /usr/local/bin/lessc` 로  lessc 파일을 열어 첫번째 줄의 `node` 를 `nodejs` 로 수정한다.

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
[이곳](https://dayone.me/20Tcz1k) 을 참고해 세팅을 설정하면 된다. [샘플](bravepeach/settings/local.py) 을 제공하고 있으니 복사해 사용하면 편리하다.

기본 세팅파일은 `bravepeach/settings/local.py` 를 이용하도록 되어 있으며,

다른 세팅을 기본으로 이용하려면 [bravepeach/wsgi.py](bravepeach/wsgi.py), [manage.py](manage.py) 를 수정하면 된다.

혹시 Pycharm 에서 직접 서버를 켠다면 Edit Configurations 에 들어가서 Environment variables 도 변경해주어야 에러가 안 난다.
