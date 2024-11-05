import configparser
import subprocess
import json
import cpu_check
import time

def scale_out(service_name, replicas):
    """Docker Compose 서비스의 replica 개수를 늘립니다."""
    try:
        subprocess.call(['sudo docker compose', 'scale', f'{service_name}={replicas}'])
        print(f"스케일 아웃: {service_name} replica 개수를 {replicas}로 늘렸습니다.")
    except Exception as e:
        print(f"스케일 아웃 중 오류 발생: {e}")

def scale_in(service_name, replicas):
    """Docker Compose 서비스의 replica 개수를 줄입니다."""
    try:
        subprocess.call(['sudo docker compose', 'scale', f'{service_name}={replicas}'])
        print(f"스케일 인: {service_name} replica 개수를 {replicas}로 줄였습니다.")
    except Exception as e:
        print(f"스케일 인 중 오류 발생: {e}")

def get_current_replicas(service_name):
    """Docker Compose 서비스의 현재 replica 개수를 반환합니다."""
    try:
        result = subprocess.check_output(['sudo', 'docker', 'compose', 'ps', '--format', 'json'])
        result = result.decode('utf-8')
        containers = json.loads(result)
        return len([c for c in [containers] if c['Service'] == service_name])
    except Exception as e:
        print(f"현재 replica 개수를 가져오는 중 오류 발생: {e}")
        return None



def main():
	# 설정 파일 읽어오기
    stack = 0
    cpu_threshold = 80
    while True:  # 무한 루프
        print(".")
        cpu_percentages = cpu_check.get_cpu_percent()
        if cpu_percentages is not None:
            # 모든 컨테이너의 CPU 사용량 평균 계산
            total_cpu_percent = sum(cpu_percentages.values())
            num_containers = len(cpu_percentages)
            avg_cpu_percent = total_cpu_percent / num_containers if num_containers > 0 else 0

            if avg_cpu_percent > cpu_threshold:
                # 스케일 아웃
                current_replicas = get_current_replicas('blog')
                stack = stack + 1
                if current_replicas is not None and stack == 6:
                    scale_out('blog', current_replicas + 1)
                    stack = 0
            else:
                # 스케일 인
                current_replicas = get_current_replicas('blog')
                if current_replicas is not None and current_replicas > 1:  # 최소 1개의 replica 유지
                    scale_in('blog', current_replicas - 1)

        time.sleep(10)

if __name__ == "__main__":
	main()
    
