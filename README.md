# Runpod ComfyUI Worker

이 프로젝트는 Runpod Serverless에서 실행 가능한 ComfyUI 커스텀 워커입니다.
GitHub에 코드를 올리면 자동으로 빌드되거나, Runpod와 직접 연결하여 사용할 수 있습니다.

## 🚀 배포 방법 1: Runpod GitHub 연결 (직접 Repo 업로드)
Runpod의 **GitHub Integration** 기능을 사용하여 소스 코드를 직접 배포할 수 있습니다.

1. **Runpod 설정**:
   - Runpod Console 로그인.
   - **Settings** > **Connections** > **GitHub**에서 `Connect` 클릭하여 GitHub 계정 연동.
2. **엔드포인트 생성**:
   - **Serverless** 메뉴 > **New Endpoint**.
   - **Github Repo** (또는 Import Git Repository) 선택.
   - 연결된 계정의 이 Repository(`comfy_runpod`) 선택.
3. **설정 입력**:
   - **Branch**: `main`
   - **Dockerfile Path**: `Dockerfile` (루트에 있으므로 그대로)
   - **Container Disk**: 20GB 이상 권장 (모델 다운로드를 위해 넉넉하게)
   - **Volume Disk**: 필요 시 설정
4. **⚠️ 주의사항 (API Token)**:
   - `Dockerfile`에서 Civitai 모델 다운로드를 위해 `CIVITAI_API_TOKEN`을 사용하고 있습니다.
   - Runpod의 웹 빌더가 **Build Arguments**를 지원하는지 확인해야 합니다. 만약 빌드 설정 단계에서 `CIVITAI_API_TOKEN` 값을 넣을 수 없다면, 빌드가 실패할 수 있습니다.
   - 이 경우, **배포 방법 2 (GitHub Actions)**를 사용하세요. 이것이 더 확실한 방법입니다.

---

## 🚀 배포 방법 2: GitHub Actions (권장)
GitHub에 코드를 푸시하면 자동으로 Docker 이미지를 빌드하여 DockerHub에 올리는 방식입니다. Runpod에서는 빌드된 이미지만 가져다 쓰면 되므로 훨씬 안정적입니다.

### 1단계: GitHub 저장소 설정 (Secrets)
GitHub Repository의 **Settings > Secrets and variables > Actions**에 다음 비밀키들을 추가하세요:
- `DOCKER_USERNAME`: 본인의 DockerHub 아이디
- `DOCKER_PASSWORD`: 본인의 DockerHub 비밀번호 (또는 Access Token)
- `CIVITAI_API_TOKEN`: Civitai API 토큰

### 2단계: 코드 푸시
```bash
git add .
git commit -m "Add GitHub Actions"
git push origin main
```
이제 10~20분 정도 기다리면 GitHub Actions가 이미지를 빌드하고 DockerHub에 `본인아이디/comfy-runpod:latest`로 업로드합니다.

### 3단계: Runpod 배포
1. Runpod Console > **Templates** > **New Template**.
2. **Container Image**: `본인아이디/comfy-runpod:latest` 입력.
3. **Environment Variables**: 필요한 경우 설정.
4. 저장 후 **Serverless Endpoint** 생성 시 이 템플릿 사용.

## 📁 주요 파일
- `Dockerfile`: ComfyUI 및 노드 설치, 모델 다운로드 정의.
- `.github/workflows/publish_docker.yml`: GitHub Actions 자동 빌드 스크립트.
