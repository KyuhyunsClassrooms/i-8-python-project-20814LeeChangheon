# 1. 데이터 생성 함수 (입력)
def create_wafer_data(): 
    """9x9 크기의 웨이퍼 2차원 리스트를 반환합니다. (0은 빈 공간, 숫자는 두께)"""
    
    # 웨이퍼의 둥근 형태를 표현하기 위해 모서리는 0(빈 공간)으로 두고, 나머지는 식각 두께 수치를 입력합니다.
    wafer_grid = [
        [0, 0, 0, 94, 93, 94, 0, 0, 0],
        [0, 0, 96, 98, 99, 98, 96, 0, 0],
        [0, 96, 100, 101, 100, 101, 96, 0, 0],
        [94, 98, 101, 105, 106, 105, 101, 98, 94],
        [93, 99, 100, 106, 108, 106, 100, 99, 93],
        [94, 98, 101, 105, 106, 105, 101, 98, 94],
        [0, 96, 100, 101, 100, 101, 96, 0, 0],
        [0, 0, 96, 98, 99, 98, 96, 0, 0],
        [0, 0, 0, 94, 93, 94, 0, 0, 0]
    ]
    # 생성된 2차원 리스트 데이터를 반환합니다.
    return wafer_grid 

# 2. 상태 판정 및 맵 출력 함수 (처리 및 출력)
def print_and_evaluate_map(wafer, target, tolerance):
    """웨이퍼를 검사하여 맵을 기호로 출력하고, 불량 칩의 좌표를 찾아냅니다."""
    
    # 웨이퍼의 가로/세로 길이를 구합니다 (여기서는 9).
    size = len(wafer) 
    total_chips = 0
    normal_chips = 0
    
    # 불량으로 판정된 칩의 (x, y) 좌표를 저장할 빈 리스트를 준비합니다.
    defect_chips = [] 

    print("\n[웨이퍼 맵 시각화]")
    
    # 이중 for문을 사용하여 웨이퍼의 모든 Y좌표(행)와 X좌표(열)를 순차적으로 탐색합니다.
    for y in range(size):
        row_str = ""
        for x in range(size):
            # 현재 좌표(x, y)에 있는 칩의 식각 두께 값을 가져옵니다.
            thickness = wafer[y][x] 
            
            # 두께가 0인 곳은 칩이 없는 빈 공간이므로 검사에서 제외하고 빈칸 기호를 출력합니다.
            if thickness == 0: 
                row_str += "[   ] "
            else:
                total_chips += 1
                
                # 칩의 두께와 목표 두께의 차이가 허용 오차 이내인지 확인하여 정상(OK) 판정을 내립니다.
                if abs(thickness - target) <= tolerance: 
                    row_str += "[ O ] "
                    normal_chips += 1
                elif thickness < target - tolerance:
                    row_str += "[ - ] " # 너무 많이 깎인 불량 (OVER)
                    
                    # 불량 칩으로 판정되었으므로, 해당 칩의 좌표를 불량 리스트에 추가합니다.
                    defect_chips.append((x, y)) 
                else:
                    row_str += "[ + ] " # 덜 깎인 불량 (UNDER)
                    defect_chips.append((x, y)) # 불량 좌표 저장
        print(row_str)
        
    return total_chips, normal_chips, defect_chips

# 3. 결함 패턴 분석 함수 (처리 및 출력)
def analyze_pattern(defect_chips, size):
    """불량 칩의 위치를 분석하여 패턴을 진단합니다."""
    print("\n[결함 패턴 진단]")
    
    if len(defect_chips) == 0:
        print("모든 칩이 정상입니다!")
        return

    # 웨이퍼의 정중앙 좌표를 구합니다 (9x9의 경우 중심은 4, 4).
    center_x = size // 2 
    center_y = size // 2
    total_distance = 0
    
    # 저장해둔 불량 칩들의 좌표를 하나씩 꺼내서 중심점과의 거리를 계산합니다.
    for x, y in defect_chips:
        # 피타고라스의 정리를 이용하여 현재 불량 칩과 웨이퍼 중심점 사이의 직선 거리를 측정합니다.
        # (** 0.5 는 파이썬에서 루트(제곱근)를 계산하는 방식입니다.)
        distance = ((x - center_x)**2 + (y - center_y)**2) ** 0.5
        total_distance += distance
        
    # 계산된 거리들을 모두 더한 후 불량 칩의 개수로 나누어 '평균 거리'를 구합니다.
    avg_distance = total_distance / len(defect_chips)
    
    # 평균 거리가 짧으면 가운데 쪽에 불량이 몰려있고, 멀면 테두리 쪽에 불량이 몰려있다고 진단합니다.
    if avg_distance < 2.5:
        print("-> 진단: '가운데(Center) 불량' 패턴입니다.")
    else:
        print("-> 진단: '테두리(Edge) 불량' 패턴입니다.")

# 4. 메인 실행 함수
def main():
    print("=== 반도체 웨이퍼 식각 결함 진단기 ===")
    
    # 1. 데이터 준비
    wafer_grid = create_wafer_data()
    size = len(wafer_grid)
    
# 2. 사용자 입력 및 예외 처리
    # 사용자가 문자를 입력할 경우 프로그램이 멈추지 않도록 예외 처리(try-except)를 적용합니다.
    try:
        target = float(input("목표 두께를 입력하세요 (예: 100): "))
        tolerance = float(input("허용 오차를 입력하세요 (예: 3): "))
    except ValueError:
        print("오류: 숫자만 입력해야 합니다. 프로그램을 종료합니다.")
        return
    
    # 3. 검사 및 맵 출력
    total, normal, defects = print_and_evaluate_map(wafer_grid, target, tolerance)
    
    # 4. 결과 요약 및 패턴 분석
    # 전체 검사 결과를 요약하여 출력합니다.
    print(f"\n[검사 결과] 총 {total}개 중 정상 {normal}개, 불량 {len(defects)}개")
    analyze_pattern(defects, size)

# 프로그램 시작점
# 프로그램이 직접 실행될 때만 main() 함수를 호출하여 작동을 시작합니다.
if __name__ == "__main__":
    main()