import wave
import os


def get_l_r(filename: str):
    with wave.open(f"static/audio/" + filename) as f:
        n = f.getnframes()
        w = f.getsampwidth()
        # 전체 데이터
        data = bytearray(f.readframes(n))
        # L 데이터
        l_form = bytearray()
        for i in range(n * w * 2)[:: w * 2]:
            l_form += data[i : i + w]
        l_data = bytes(l_form)
        # R 데이터
        r_form = bytearray()
        for i in range(n * w * 2)[w :: w * 2]:
            r_form += data[i : i + w]
        r_data = bytes(r_form)

    return l_data, r_data, f.getnchannels()


def make_file(l_data, filename):
    # stereo 에서 l, r 데이터 추출
    with wave.open(f"static/audio/" + filename) as f:
        # l 파일 만들기
        with wave.open(f"static/audio/" + filename, "wb") as l_file:
            l_file.setparams(f.getparams())
            l_file.setnchannels(1)
            l_file.writeframes(l_data)

        # r 파일 만들기
        # mono to stereo 에서는 사용 필요 없음
        # with wave.open(filename + "_R.wav", "wb") as r_file:
        #     r_file.setparams(f.getparams())
        #     r_file.setnchannels(1)
        #     r_file.writeframes(r_data)


def stereo_to_mono(filename: str):
    # stereo 에서 l, r 데이터 추출
    l_data, r_data, c = get_l_r(filename)

    print(filename)
    if c == 1:
        # print("mono 파일 입니다")
        pass
    elif l_data != r_data:
        # print("stereo 파일 입니다")
        pass
    else:
        # print("mono-stereo 파일 입니다")
        # print("분리 시작")
        make_file(l_data, filename)
    #     print("분리 완료")
    # print("\n")


def start():
    # print("작업을 시작합니다\n")
    file_list = os.listdir(f"static/audio")
    print(file_list)
    for file_name in file_list:
        if file_name == ".DS_Store":
            pass
        else:
            try:
                stereo_to_mono(file_name)
            except:
                print(file_name)
                # print("잘못된 파일입니다\n")
    # print("작업이 종료되었습니다")
