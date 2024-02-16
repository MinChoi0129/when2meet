import os
import numpy as np
import cv2


class TableManager:
    MODES_BY_RED = {17: "DARK", 255: "LIGHT"}

    ANDROID_BACKGROUND_COLOR = {"DARK": 17, "LIGHT": 255}
    IPHONE_BACKGROUND_COLOR = {"DARK": 17, "LIGHT": 255}

    ANDROID_LINE_COLOR = {"DARK": 49, "LIGHT": 237}
    ANDROID_PIXEL_ERROR_TOLERANCE = 5

    DATE = {0: "mon", 1: "tue", 2: "wed",
            3: "thu", 4: "fri", 5: "sat", 6: "sun"}
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    EMPTY_TABLE = {
        "mon": dict(),
        "tue": dict(),
        "wed": dict(),
        "thu": dict(),
        "fri": dict(),
        "sat": dict(),
        "sun": dict(),
    }

    @staticmethod
    # file_path는 절대경로
    def getUnavailableDatetime(file_path: str, unavailable_datetimes: dict, user_id):
        # 선분 교차 좌표
        Xs, Ys = [], []

        img_array = np.fromfile(file_path, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        mode = TableManager.MODES_BY_RED[img[16][16][0]]  # DARK, LIGHT
        device_type = "ANDROID" if img[56][60][0] in [17, 255] else "IPHONE"

        if device_type == "ANDROID":
            # 모드별 감지 색상 지정
            LINE_COLOR = TableManager.ANDROID_LINE_COLOR[mode]
            BACKGROUND_COLOR = TableManager.ANDROID_BACKGROUND_COLOR[mode]

            # 가로 선 검출(행)
            for x in range(0, len(img)):
                if img[x][0][0] == LINE_COLOR:
                    if not Xs:
                        Xs.append(x)
                    elif abs(Xs[-1] - x) > TableManager.ANDROID_PIXEL_ERROR_TOLERANCE:
                        Xs.append(x)
            Xs.pop()

            # 세로 선 검출(열)
            for y in range(0, len(img[0])):
                if img[0][y][0] == LINE_COLOR:
                    if not Ys:
                        Ys.append(y)
                    elif abs(Ys[-1] - y) > TableManager.ANDROID_PIXEL_ERROR_TOLERANCE:
                        Ys.append(y)

            # 고정점으로부터 추정점까지의 변위
            x_gap_5 = int((Xs[1] - Xs[0]) * 0.05)
            y_gap_95 = int((Ys[1] - Ys[0]) * 0.95)

            # 추정점 셀 컬러 확인
            for j, y in enumerate(Ys):
                for i, x in enumerate(Xs):
                    search_x, search_y = x + x_gap_5, y + y_gap_95

                    # 범위 내
                    if not (
                        0 <= search_x <= img.shape[0] and 0 <= search_y <= img.shape[1]
                    ):
                        continue

                    cv2.circle(img, (search_y, search_x), 5, (255, 0, 0), 3)

                    # 공강 상태가 아니라면
                    if img[search_x][search_y][0] != BACKGROUND_COLOR:
                        if str(i + 1) not in unavailable_datetimes[TableManager.DATE[j]]:
                            unavailable_datetimes[TableManager.DATE[j]][str(i + 1)] = [
                                user_id
                            ]
                        else:
                            unavailable_datetimes[TableManager.DATE[j]][str(i + 1)].append(
                                user_id
                            )
        elif device_type == "IPHONE":
            day_len = None
            k = img[38][61]
            a = img[38][61+204]
            b = img[38][61+171]
            c = img[38][61+147]

            ra = np.sum((k - a)**2)
            rb = np.sum((k - b)**2)
            rc = np.sum((k - c)**2)
            print(ra, rb, rc)

            if ra == min(ra, rb, rc):
                day_len = '5'
            elif rb == min(ra, rb, rc):
                day_len = '6'
            elif rc == min(ra, rb, rc):
                day_len = '7'
            print(mode, device_type, day_len)

            WIDTH = {'5': 204, '6': 171, '7': 147}
            MAX_WIDTH, MAX_HEIGHT = 1077, img.shape[0]
            current_x, current_y, w, h = 61, 61, WIDTH[day_len], 135

            while True:
                Xs.append(current_x)
                Ys.append(current_y)

                current_x += w
                if current_x > MAX_WIDTH:
                    current_x = 61
                    current_y += h

                if current_y + 0.9 * h > MAX_HEIGHT:
                    break

            d = 18
            classtime = 1
            for i in range(len(Xs)):
                someday = TableManager.DATE[i % int(day_len)]
                # day_len == 5 : 0, 1, 2, 3, 4 : mon, tue, wed, thu, fri
                # day_len == 7 : 0, 1, 2, 3, 4, 5, 6 : mon, tue, wed, thu, fri, sat, sun

                x, y = Xs[i], Ys[i]
                red = img[y+d][x+d][0]
                if red not in [17, 255]:  # 수업 있음
                    if str(classtime) not in unavailable_datetimes[someday]:
                        unavailable_datetimes[someday][str(classtime)] = [
                            user_id]
                    else:
                        unavailable_datetimes[someday][str(
                            classtime)].append(user_id)

                if someday == TableManager.DATE[int(day_len) - 1]:
                    classtime += 1

        sorted_unavailable_datetimes = dict()

        for key in TableManager.DATE.values():
            sorted_unavailable_datetimes[key] = dict()

        for key in TableManager.DATE.values():  # mon, tue, wed, thu, fri, sat, sun
            sorted_keys = map(str, sorted(
                map(int, unavailable_datetimes[key].keys())))

            for sorted_key in sorted_keys:
                sorted_unavailable_datetimes[key][sorted_key] = unavailable_datetimes[
                    key
                ][sorted_key]

        return sorted_unavailable_datetimes

    @staticmethod
    def printTable(table: dict):
        for day in table:
            print("=========================")
            print(f"[{day}]")
            unavailable_classtimes: dict = table[day]
            for classtime in unavailable_classtimes:
                print(classtime, ":", unavailable_classtimes[classtime])

    @staticmethod
    def groupUnavailableDatetimes(user_ids: list[str]):
        unavailable_datetimes = TableManager.EMPTY_TABLE
        for user_id in user_ids:
            img_path = os.path.join(
                TableManager.BASE_PATH, "media", "iphone", f"{user_id}.jpg")  # 여기 경로 세팅 상황에 맞게 변경해야함.
            unavailable_datetimes = TableManager.getUnavailableDatetime(
                img_path, unavailable_datetimes, user_id
            )  # unavailable_datetimes 변수를 return한것을 꼭 재대입하여 '업데이트' 해줘야함.
        return unavailable_datetimes


os.system("cls")
user_ids = ["5_dark", "6_white", "7_white"]
timetable = TableManager.groupUnavailableDatetimes(user_ids)
TableManager.printTable(timetable)
