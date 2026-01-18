# Runpod ComfyUI Worker (All-in-One Version)

이 프로젝트는 사용자의 요청에 따라 **모든 모델을 Docker 이미지에 포함시키는 버전**입니다.
가장 빠르고 간편하게 Serverless를 이용할 수 있지만, 이미지 크기가 매우 커서 GitHub Actions 무료 버전으로는 빌드가 불가능합니다.
따라서 **Runpod의 GPU 인스턴스를 빌려서 빌드**해야 합니다.

## 🚀 배포 방법: Runpod에서 직접 빌드하기

이 방법은 확실하고 강력합니다. 10~20분 정도 소요되며 비용은 몇백 원 정도입니다.

### 1단계: Runpod에서 빌드용 Pod 생성
1. **Runpod Console** > **Pods** > **Deploy**.
2. **GPU 선택**: 아무거나 싼 걸로 고르세요 (RTX 3070, 4090 등).
3. **Template**: `runpod/docker-in-docker` (또는 그냥 `Ubuntu`도 되지만 docker가 있는지 확인 필요)
   - *팁: `runpod/stable-diffusion:comfy-ui` 같은 걸 써도 되지만, Docker가 깔려 있어야 합니다. 그냥 기본 `runpod/base` 추천.*
4. **Volume Disk**: **100GB 이상**으로 설정하세요. (이미지 만들다가 터질 수 있습니다)

### 2단계: 소스 코드 가져오기 및 빌드
Pod가 실행되면 **Connect > Web Terminal** 또는 JupyterLab 터미널을 엽니다.

```bash
# 1. 소스 코드 복제
git clone https://github.com/본인아이디/comfy_runpod.git
cd comfy_runpod

# 2. Docker 로그인 (DockerHub에 올리기 위해)
docker login
# 아이디와 비번을 입력하세요.

# 3. 이미지 빌드 및 푸시
# (Civitai 토큰은 빌드 인자로 넘겨줍니다)
export CIVITAI_TOKEN="본인의_토큰_값"
docker build -t 본인아이디/comfy-runpod:v1 --build-arg CIVITAI_API_TOKEN=$CIVITAI_TOKEN .

# 4. 푸시
docker push 본인아이디/comfy-runpod:v1
```

### 3단계: Serverless Endpoint 생성
빌드가 끝나고 푸시가 완료되면 Pod는 삭제(Terminate)해도 됩니다.

1. **Runpod Serverless** > **New Endpoint**.
2. **Container Image**: 방금 푸시한 이미지 (`본인아이디/comfy-runpod:v1`) 입력.
3. **Container Disk**: 20GB 정도면 충분 (모델이 이미지 안에 있으므로).
4. **Deploy!**

이제 Cold Start가 조금 걸릴 수 있지만(이미지가 커서), 일단 뜨고 나면 모델 다운로드 없이 즉시 실행됩니다.

## 📁 주요 파일
- `Dockerfile`: 모든 모델을 포함하도록 구성됨.
- `handler.py`: Runpod Serverless 요청을 처리하는 파이썬 스크립트.
- `entrypoint.sh`: ComfyUI를 띄우고 핸들러를 실행하는 시작 스크립트.
