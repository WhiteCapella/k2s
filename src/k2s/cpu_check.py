# cpu_check.py
# print and return cpu memory space


import subprocess
import json

def get_cpu_percent():
    """모든 Docker 컨테이너의 CPU 사용량을 반환합니다."""
    try:
        # 실행 중인 모든 컨테이너 이름 가져오기
        r = subprocess.check_output(['docker', 'ps', '--format', '{{.Names}}'], universal_newlines=True)
        container_names = r.splitlines()

        cpu_percentages = {}
        for container_name in container_names:
            # 각 컨테이너의 CPU 사용량 가져오기
            r = subprocess.check_output([
                "docker", "stats", container_name,
                "--no-stream", "--format", "{{json .}}"
            ])
            j = json.loads(r.decode("utf-8"))
            cpu_percent = float(j['CPUPerc'].strip('%'))
            cpu_percentages[container_name] = cpu_percent

        return cpu_percentages  # 컨테이너 이름과 CPU 사용량을 딕셔너리 형태로 반환

    except Exception as e:
        print(f"CPU 사용량을 가져오는 중 오류 발생: {e}")
        return None
