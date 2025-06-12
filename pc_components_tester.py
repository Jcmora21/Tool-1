import os
import sys
import time
import psutil
import numpy as np
import pyautogui
import cv2
from multiprocessing import Process, cpu_count

allocated = []
active_threads = []
gpu_running = False

# Clear terminal

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Show RAM status

def ram_status():
    mem = psutil.virtual_memory()
    total = mem.total / (1024**2)
    used = mem.used / (1024**2)
    percent = mem.percent
    print(f"Total RAM: {total:.2f} MB | Used: {used:.2f} MB ({percent}%)")

# Allocate memory

def consume_ram():
    clear_terminal()
    print("Starting RAM consumption...")
    try:
        while True:
            block = bytearray(10 * 1024 * 1024)  # 10 MB
            allocated.append(block)
            ram_status()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nInterruption detected.")
        resp = input("Do you want to free the allocated memory? (y/n): ")
        if resp.lower() == 'y':
            allocated.clear()
            print("Memory freed.")
        else:
            print("Memory kept allocated.")

# Stress CPU using all cores

def stress_cpu_process():
    while True:
        x = 0
        for i in range(10_000_000):
            x += i**2
        _ = x

def start_cpu_stress():
    clear_terminal()
    print("Starting intensive CPU consumption...")
    for _ in range(cpu_count()):
        p = Process(target=stress_cpu_process)
        p.daemon = True
        p.start()
        active_threads.append(p)

# GPU consumption via rendering

def consume_gpu():
    global gpu_running
    gpu_running = True
    clear_terminal()
    screen_size = pyautogui.size()
    width, height = screen_size.width, screen_size.height
    cv2.namedWindow("GPU Stress", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("GPU Stress", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    try:
        while gpu_running:
            noise = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
            blur = cv2.GaussianBlur(noise, (15, 15), 0)
            combined = cv2.addWeighted(noise, 0.5, blur, 0.5, 0)
            cv2.imshow("GPU Stress", combined)
            if cv2.waitKey(1) == ord('q'):
                break
    except Exception as e:
        print(f"GPU Error: {e}")
    cv2.destroyAllWindows()

# Free RAM

def free_ram():
    allocated.clear()
    print("RAM memory freed.")

# Terminate everything

def terminate_all():
    global gpu_running
    print("Terminating everything...")
    gpu_running = False
    free_ram()
    for p in active_threads:
        p.terminate()
    print("All processes terminated.")

# Menu

def menu():
    options = {
        '1': ("Consume RAM", consume_ram),
        '2': ("Consume CPU", start_cpu_stress),
        '3': ("Consume GPU", consume_gpu),
        '4': ("Free RAM", free_ram),
        '5': ("Terminate All", terminate_all),
        '0': ("Exit", sys.exit)
    }

    while True:
        clear_terminal()
        print("==== PC Components Tester ====")
        for k, v in options.items():
            print(f"[{k}] {v[0]}")
        choice = input("Choose an option: ")
        if choice in options:
            try:
                options[choice][1]()
                input("\nPress Enter to continue...")
            except KeyboardInterrupt:
                print("\nInterrupted.")
                input("Press Enter to continue...")
        else:
            print("Invalid option.")
            time.sleep(1)

if __name__ == "__main__":
    menu()
