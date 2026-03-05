# website capability to skill 사용 가이드

[简体中文](./README.md) | [English](./README.en.md) |
[Español](./README.es.md) | [Français](./README.fr.md) |
[Deutsch](./README.de.md) | [日本語](./README.ja.md) | 한국어 |
[Português (Brasil)](./README.pt-BR.md) | [Русский](./README.ru.md)

이 skill은 웹사이트 URL을 받아 브라우저로 사이트 기능을 학습한 뒤,
그 기능을 API-first 방식의 로컬 skill로 변환합니다.

API를 수동으로 정리하거나 인증 복구 흐름을 직접 설계할 필요가 없습니다.

## 작성자

- 작성자: `JasirVoriya`
- 팀: `Infrastructure Storage Team`
- 이메일: `jasirvoriya@gmail.com`
- GitHub: `https://github.com/JasirVoriya`

## 핵심 규칙 (중요)

생성된 skill을 자동화 가능하고 재사용 가능하게 유지하기 위해 기본적으로 아래
규칙을 적용합니다.

- 브라우저는 기능 학습과 인증 복구에만 사용합니다.
- 비즈니스 실행은 웹 버튼이 아닌 API로 처리합니다.
- 인증 파일은 홈 디렉터리의 `~/.<site>-auth.yaml`에 저장합니다.
- 모든 API 세션 전에 인증 파일을 읽습니다.
- 인증 만료/실패 시 브라우저에서 인증을 다시 추출해 저장합니다.
- 인증 파일 권한은 `0600`으로 유지합니다.

## 할 수 있는 일

- 대상 사이트의 노출 기능 탐지
- UI 기능을 API 메서드, 요청/응답 구조로 매핑
- 실행 가능한 사이트 전용 skill 스캐폴드 생성
- 인증 라이프사이클 통합: 읽기, 검증, 복구, 재시도
- 지원/미지원 기능을 포함한 검증 보고서 생성

## 설치 (`npx skills add`)

`npx skills add openclaw/openclaw`처럼 이 skill도 GitHub 저장소에서 직접
설치할 수 있습니다.

### 1) 저장소의 설치 가능한 skill 목록 확인

```bash
npx -y skills add JasirVoriya/voriya-skills --list
```

### 2) Codex에 설치 (전역)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a codex -g -y
```

### 3) Cursor에 설치 (전역)

```bash
npx -y skills add JasirVoriya/voriya-skills --skill website-capability-to-skill -a cursor -g -y
```

### 4) 멀티 skill 저장소 시나리오 (선택)

```bash
npx -y skills add <owner>/<repo> --skill website-capability-to-skill -a codex -g -y
```

설치 후 AI 클라이언트를 재시작해 새 skill을 로드하세요.

## 프롬프트 예시

### 1) 기본 생성

```text
website-capability-to-skill로 https://example.com 을 분석해서,
사이트 기능을 API-first skill로 변환하고,
전체 디렉터리 구조를 출력해줘.
```

### 2) 범위 지정 생성

```text
website-capability-to-skill로 https://example.com 을 분석하고,
"로그인 후 관리자 콘솔 + 게시 흐름"만 포함해.
나머지는 unsupported-via-api로 표시해줘.
```

### 3) 인증 복구 강제

```text
website-capability-to-skill로 skill을 생성하고 API를 검증해.
인증이 실패하면 브라우저에서 cookie/token을 가져와
~/.<site>-auth.yaml에 저장한 뒤 재시도해.
```

### 4) 검증 보고서 출력

```text
website-capability-to-skill 생성 완료 후,
지원 기능, 미지원 기능, 실패 원인,
다음 단계 제안을 포함한 검증 보고서를 만들어줘.
```

## 빠른 명령 (스크립트)

```bash
python3 scripts/bootstrap_site_skill.py --url <target-url> --output-root <skills-root>
python3 scripts/auth_cache.py path --url <target-url>
python3 scripts/auth_cache.py read --url <target-url>
python3 scripts/auth_cache.py is-valid --url <target-url>
```

## 산출물

최소 포함 항목:

- 사이트 전용 `SKILL.md`
- `agents/openai.yaml`
- `scripts/auth_cache.py`
- `references/capability-map.md`
- 검증 결과 (지원/미지원/근거)

## 사전 준비

- 접근 가능한 대상 사이트 URL
- 대상 사이트 접근 및 조작이 가능한 브라우저 세션
- 로컬 Python 3 실행 환경

대상 사이트에 로그인이 필요하면, 인증 복구를 위해 유효한 계정을 미리 준비하세요.
