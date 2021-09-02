# ssu-ai-book-helper-server

  

### let's encrypt 발급
```
docker run -it --rm --name certbot \
  -v '/certbot:/etc/letsencrypt' \
  certbot/certbot certonly -d '*.ssuaibook.site' --manual --preferred-challenges dns --server https://acme-v02.api.letsencrypt.org/directory
```

위 명령어를 통해 인증서를 발급받는다.
<br /><br />

```
Please deploy a DNS TXT record under the name:

_acme-challenge.ssuaibook.site.

with the following value:

tgefTx2oraoL_Loh6lClv8HtDb7Sxjxsacgod9rtZGU

Before continuing, verify the TXT record has been deployed. Depending on the DNS
provider, this may take some time, from a few seconds to multiple minutes. You can
check if it has finished deploying with aid of online tools, such as the Google
Admin Toolbox: https://toolbox.googleapps.com/apps/dig/#TXT/_acme-challenge.ssuaibook.site.
Look for one or more bolded line(s) below the line ';ANSWER'. It should show the
value(s) you've just added.
```
도메인 인증으로 토큰value를 도메인 TXT 레코드로 등록하여준다.
그 이후 1-2분 대기후 enter를 눌러 인증을 확인한다.
(만약 에러가 나면 다시 명령어를 쳐서 들어가면 된다)

<hr />

### let's encrypt 인증서 위치

docker를 통해 /certbot 의 위치에 발급 받았으므로 `/certbot/live/ssuaibook.site` 에 위치한다.

이때 live 폴더는 admin권한만 접근가능하므로 `sudo chmod 755 live` 를 통해 권한을 해제한다.

여기서 우리가 필요한 키는 `fullchain.pem` , `privkey.pem` 두 개가 필요하다. 복사해서 프로젝트 폴더에 이름을 맞게 변경 후 넣어준다.

docker compose를 통해 재시작하면 끝난다.