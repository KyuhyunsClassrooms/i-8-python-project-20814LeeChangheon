import math

# 1. 데이터 클래스
class Chip:
    def __init__(self, x, y, thickness):
        self.x = x
        self.y = y
        self.thickness = thickness
        self.status = "UNKNOWN" 

# 2. 메인 분석 클래스
class WaferAnalyzer:
    def __init__(self, grid_data):
        self.wafer_grid = grid_data
        self.size = len(grid_data)
        self.center_x = self.size // 2
        self.center_y = self.size // 2
        self.total_chips = 0
        self.normal_chips = 0
        self.defect_chips = []

    def evaluate_chips(self, target, tolerance):
        """이중 for문으로 모든 칩의 상태를 판정한다."""
        for y in range(self.size):
            for x in range(self.size):
                chip = self.wafer_grid[y][x]
                
                if chip is None: # 빈 공간 제외
                    continue
                
                self.total_chips += 1
                
                # 정상 범위 판정 (예: 97 ~ 103)
                if abs(chip.thickness - target) <= tolerance:
                    chip.status = "OK"
                    self.normal_chips += 1
                else:
                    if chip.thickness < target - tolerance:
                        chip.status = "OVER"  # 너무 많이 깎임 (-)
                    else:
                        chip.status = "UNDER" # 덜 깎임 (+)
                    self.defect_chips.append(chip)

    def analyze_pattern(self):
        """불량 칩의 위치를 분석하여 패턴을 진단한다."""
        print("\n[결함 패턴 진단]")
        
        if len(self.defect_chips) == 0:
            print("모든 칩이 정상입니다!")
            return

        total_distance = 0
        for chip in self.defect_chips:
            # 중심점과의 거리 계산
            distance = math.sqrt((chip.x - self.center_x)**2 + (chip.y - self.center_y)**2)
            total_distance += distance
        
        avg_distance = total_distance / len(self.defect_chips)
        
        # 거리가 멀면 테두리 불량, 가까우면 가운데 불량
        if avg_distance < 2.5:
            print("-> 진단: '가운데(Center) 불량' 패턴입니다.")
        else:
            print("-> 진단: '테두리(Edge) 불량' 패턴입니다.")

    def print_map(self):
        """웨이퍼 맵을 기호로 출력한다."""
        print("\n[웨이퍼 맵 시각화]")
        for y in range(self.size):
            row_str = ""
            for x in range(self.size):
                chip = self.wafer_grid[y][x]
                if chip is None:
                    row_str += "[   ] "
                elif chip.status == "OK":
                    row_str += "[ O ] "
                elif chip.status == "OVER":
                    row_str += "[ - ] "
                elif chip.status == "UNDER":
                    row_str += "[ + ] "
            print(row_str)


# 3. 가짜 데이터 생성 함수
def create_dummy_wafer():
    raw_data = [
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
    
    wafer_grid = []
    for y in range(9):
        row = []
        for x in range(9):
            if raw_data[y][x] == 0:
                row.append(None)
            else:
                row.append(Chip(x, y, raw_data[y][x]))
        wafer_grid.append(row)
    return wafer_grid


# 4. 메인 실행
def main():
    print("=== 반도체 웨이퍼 식각 결함 진단기 ===")
    wafer_grid = create_dummy_wafer()
    analyzer = WaferAnalyzer(wafer_grid)
    
    target = float(input("목표 두께를 입력하세요 (예: 100): "))
    tolerance = float(input("허용 오차를 입력하세요 (예: 3): "))
    
    analyzer.evaluate_chips(target, tolerance)
    analyzer.print_map()
    
    print(f"\n[검사 결과] 총 {analyzer.total_chips}개 중 정상 {analyzer.normal_chips}개, 불량 {len(analyzer.defect_chips)}개")
    analyzer.analyze_pattern()

if __name__ == "__main__":
    main()