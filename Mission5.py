import tkinter as tk
from tkinter import messagebox

# -----------------------------
# 전역 변수 선언
# -----------------------------
root = tk.Tk()

# 입력 변수
total_amount_var = tk.StringVar()
people_count_var = tk.StringVar()
tip_percent_var = tk.StringVar()

# 결과 변수
per_person_var = tk.StringVar()
total_with_tip_var = tk.StringVar()

# 슬라이더 참조용 (초기 선언)
slider = None


# -----------------------------
# 계산 함수 (콤마 적용)
# -----------------------------
def calculate():
    try:
        total = float(total_amount_var.get())
        people = int(people_count_var.get())
        tip = float(tip_percent_var.get())

        if people == 0:
            messagebox.showerror("오류", "인원 수는 0이 될 수 없습니다.")
            return

        total_with_tip = total * (1 + tip / 100)
        per_person = total_with_tip / people

        per_person_var.set(f"{int(per_person):,}")
        total_with_tip_var.set(f"{int(total_with_tip):,}")

    except:
        messagebox.showerror("입력 오류", "올바른 숫자를 입력하세요.")


# -----------------------------
# 초기화 함수
# -----------------------------
def clear_all():
    total_amount_var.set("")
    people_count_var.set("")
    tip_percent_var.set("")
    per_person_var.set("")
    total_with_tip_var.set("")
    slider.set(0)


# -----------------------------
# 슬라이더 → 입력창
# -----------------------------
def update_tip_from_slider(value):
    tip_percent_var.set(str(int(float(value))))


# -----------------------------
# 입력창 → 슬라이더 (핵심 추가)
# -----------------------------
def update_slider_from_entry(*args):
    try:
        value = int(float(tip_percent_var.get()))

        # 슬라이더 범위 내에서만 반영
        if 0 <= value <= 20:
            slider.set(value)
    except:
        pass  # 숫자가 아닐 때 무시


# trace 등록 (양방향 동기화)
tip_percent_var.trace_add("write", update_slider_from_entry)


# -----------------------------
# 팁 초기화
# -----------------------------
def reset_tip():
    tip_percent_var.set("")
    slider.set(0)


# -----------------------------
# 메인 윈도우
# -----------------------------
root.title("모임 회비 관리 계산기")
root.geometry("600x350")

# 제목
tk.Label(
    root,
    text="모임 회비 관리 계산기",
    font=("맑은 고딕", 16, "bold")
).pack(pady=(10, 5))

# 설명
tk.Label(
    root,
    text="총 금액, 인원 수, 팁 비율을 입력하여 1인당 부담할 금액을 계산합니다."
).pack(pady=(0, 10))

# 메인 프레임
main_frame = tk.Frame(root)
main_frame.pack()

# -----------------------------
# 입력 영역
# -----------------------------
input_frame = tk.Frame(main_frame, bd=1, relief="solid", padx=10, pady=10)
input_frame.grid(row=0, column=0, padx=5)

ENTRY_WIDTH = 20

tk.Label(input_frame, text="총 금액(원)").grid(row=0, column=0, sticky="w")
tk.Entry(input_frame, textvariable=total_amount_var, width=ENTRY_WIDTH) \
    .grid(row=1, column=0, columnspan=2, sticky="w")

tk.Label(input_frame, text="인원 수(명)").grid(row=2, column=0, sticky="w")
tk.Entry(input_frame, textvariable=people_count_var, width=ENTRY_WIDTH) \
    .grid(row=3, column=0, columnspan=2, sticky="w")

tk.Label(input_frame, text="팁/서비스 비율(%)").grid(row=4, column=0, sticky="w")
tk.Entry(input_frame, textvariable=tip_percent_var, width=ENTRY_WIDTH) \
    .grid(row=5, column=0, sticky="w")

# 새로고침 버튼
tk.Button(input_frame, text="↻", command=reset_tip, width=3) \
    .grid(row=5, column=1, padx=5)

# 슬라이더
slider_frame = tk.Frame(input_frame)
slider_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)

tk.Label(slider_frame, text="0").pack(side="left")

slider = tk.Scale(
    slider_frame,
    from_=0,
    to=20,
    orient="horizontal",
    resolution=5,
    showvalue=0,
    command=update_tip_from_slider,
    activebackground="orange",
    highlightbackground="orange"
)
slider.pack(side="left", fill="x", expand=True)

tk.Label(slider_frame, text="20").pack(side="right")

# 버튼
button_frame = tk.Frame(input_frame)
button_frame.grid(row=7, column=0, columnspan=2, pady=5)

tk.Button(button_frame, text="Clear", bg="white", width=10, command=clear_all) \
    .pack(side="left", padx=5)

tk.Button(button_frame, text="Submit", bg="orange", fg="white", width=10, command=calculate) \
    .pack(side="left", padx=5)

# -----------------------------
# 결과 영역
# -----------------------------
result_frame = tk.Frame(main_frame, bd=1, relief="solid", padx=10, pady=10)
result_frame.grid(row=0, column=1, padx=5)

tk.Label(result_frame, text="1인당 금액(원)").grid(row=0, column=0, sticky="w")
tk.Entry(
    result_frame,
    textvariable=per_person_var,
    state="readonly",
    readonlybackground="white",
    width=ENTRY_WIDTH
).grid(row=1, column=0, sticky="w")

tk.Label(result_frame, text="팁 포함 총 금액(B)").grid(row=2, column=0, sticky="w")
tk.Entry(
    result_frame,
    textvariable=total_with_tip_var,
    state="readonly",
    readonlybackground="white",
    width=ENTRY_WIDTH
).grid(row=3, column=0, sticky="w")

# 실행
root.mainloop()