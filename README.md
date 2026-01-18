# Runpod ComfyUI Worker (Lightweight Version)

이 프로젝트는 거대한 모델 파일들을 이미지에 포함시키지 않는 **경량화된 버전**입니다.
Runpod의 **Network Volume** 기능을 사용하여 모델을 따로 관리하는 것이 효율적입니다.

## 🚀 배포 및 설정 가이드

### 1. GitHub로 코드 업데이트
GitHub Actions 없이 Runpod에서 직접 빌드되도록 변경했습니다. 코드를 푸시하세요.
```bash
git add .
git commit -m "Optimize: Remove heavy models from build"
git push origin main
```

### 2. Runpod 설정 (중요!)

**2-1. Network Volume 생성**
1. Runpod Console > **Network Volume** > **Create**.
2. 이름: `comfy-models` (예시)
3. 크기: **50GB 이상** (모델들이 큽니다)
4. Data Center: Serverless Worker를 실행할 지역과 **동일하게** 선택.

**2-2. 템플릿 생성 (Template)**
1. **Templates** > **New Template**.
2. **Container Image**: Runpod의 Git Import 기능 사용 혹은 (추후 빌드될 이미지 주소).
   - 지금은 "Docker Hub" 이미지가 없으므로, Step 3에서 Serverless 생성 시 **"Import Git Repository"**를 씁니다.
3. **Environment Variables**:
   - `CIVITAI_API_TOKEN`: 본인의 Civitai 토큰 입력.

### 3. 모델 다운로드 (최초 1회만 수행)
Serverless Worker는 켜졌다 꺼지므로, 모델 다운로드를 매번 하면 요금이 많이 나옵니다.
**일반 Pod**를 잠시 띄워서 볼륨에 모델을 받아두는 것을 추천합니다.

1. **Pods** > **Deepploy** (GPU 아무거나, 싼 걸로).
2. **Volume Mount**: 위에서 만든 `comfy-models`를 `/ComfyUI/models` 경로에 마운트합니다. (★ 중요)
   - Mount Path: `/ComfyUI/models`
3. 컨테이너가 뜨면 `Jupyter Lab` 또는 `Web Terminal` 접속.
4. Git Clone 후 다운로드 스크립트 실행:
   ```bash
   cd /
   git clone https://github.com/본인아이디/comfy_runpod.git
   cd comfy_runpod
   export CIVITAI_API_TOKEN=토큰값
   python download_models.py
   ```
   *참고: `/ComfyUI/models`가 볼륨에 연결되어 있으므로, 여기에 다운로드된 파일은 영구 보존됩니다.*
5. 다운로드 완료 후 Pod **삭제 (Terminate)**.

### 4. Serverless 실행
1. **Serverless** > **New Endpoint**.
2. **Import Git Repository**: 이 레포지토리 선택.
3. **Network Volume**: 아까 만든 `comfy-models` 선택.
4. **Mount Path**: `/ComfyUI/models`
5. 배포!

이제 이미지가 가볍기 때문에 빌드가 1~2분 안에 끝나고, 모델은 이미 볼륨에 있으므로 실행 즉시 사용 가능합니다.
