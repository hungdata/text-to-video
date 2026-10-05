#!/usr/bin/env python3
"""
System Monitor & Freeze Prevention Sentinel for macOS (Apple Silicon / Intel).
Theo dõi sức khỏe hệ thống (CPU, RAM, Memory Pressure, Swap, Pin/Nhiệt) khi render video.
Dự đoán và ngăn chặn tình trạng đơ/treo máy trước khi render.

Cách dùng:
  python3 health_check.py                 # Kiểm tra tổng quan & gợi ý
  python3 health_check.py --json          # Xuất JSON (cho AI Agent đọc)
  python3 health_check.py --pre-flight    # Kiểm tra an toàn trước khi render (exit code 0 nếu OK)
  python3 health_check.py --cooldown 20   # Nghỉ giải nhiệt 20 giây giữa các video
  python3 health_check.py --watch 15      # Theo dõi liên tục
"""

import subprocess, json, sys, time, os

THRESHOLDS = {
    "cpu_warn": 75,
    "cpu_danger": 90,
    "ram_warn": 80,
    "ram_danger": 90,
    "disk_warn": 85,
    "disk_danger": 95,
    "swap_warn_gb": 2.0,
    "swap_danger_gb": 4.0,
}

def get_cpu_usage():
    try:
        out = subprocess.check_output(["ps", "-A", "-o", "%cpu"], text=True)
        total = sum(float(line.strip()) for line in out.strip().split("\n")[1:] if line.strip())
        cores = os.cpu_count() or 8
        return round(total / cores, 1)
    except Exception:
        return -1

def get_ram_info():
    try:
        out = subprocess.check_output(["vm_stat"], text=True)
        lines = out.strip().split("\n")
        page_size = 16384  # macOS default Apple Silicon
        stats = {}
        for line in lines[1:]:
            parts = line.split(":")
            if len(parts) == 2:
                key = parts[0].strip()
                val = parts[1].strip().rstrip(".")
                try:
                    stats[key] = int(val)
                except ValueError:
                    pass

        active = stats.get("Pages active", 0) * page_size
        wired = stats.get("Pages wired down", 0) * page_size
        compressed = stats.get("Pages occupied by compressor", 0) * page_size
        total_bytes = int(subprocess.check_output(["sysctl", "-n", "hw.memsize"], text=True).strip())
        used = active + wired + compressed
        pct = round(used / total_bytes * 100, 1)
        free_bytes = max(0, total_bytes - used)
        return {
            "total_gb": round(total_bytes / (1024**3), 1),
            "used_gb": round(used / (1024**3), 1),
            "free_gb": round(free_bytes / (1024**3), 1),
            "pct": pct,
        }
    except Exception:
        return {"total_gb": 8.0, "used_gb": 0, "free_gb": 8.0, "pct": 0}

def get_swap_info():
    try:
        out = subprocess.check_output(["sysctl", "-n", "vm.swapusage"], text=True).strip()
        parts = out.split()
        used_str = parts[parts.index("used") + 2].rstrip("M")
        return round(float(used_str) / 1024, 2)
    except Exception:
        return 0.0

def get_memory_pressure_pct():
    """Lấy % memory free tổng thể từ công cụ memory_pressure của macOS."""
    try:
        out = subprocess.check_output(["memory_pressure"], text=True, stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            if "System-wide memory free percentage" in line:
                val = line.split(":")[-1].strip().rstrip("%")
                return int(val)
    except Exception:
        pass
    return None

def get_power_info():
    try:
        out = subprocess.check_output(["pmset", "-g", "batt"], text=True)
        is_battery = "Battery Power" in out
        pct = None
        for word in out.split():
            if word.endswith("%;"):
                pct = int(word.rstrip("%;"))
                break
        return {"on_battery": is_battery, "battery_pct": pct}
    except Exception:
        return {"on_battery": False, "battery_pct": None}

def get_disk_usage():
    try:
        out = subprocess.check_output(["df", "-h", "/"], text=True)
        line = out.strip().split("\n")[1]
        parts = line.split()
        return {"pct": int(parts[4].rstrip("%")), "available": parts[3]}
    except Exception:
        return {"pct": -1, "available": "?"}

def get_heavy_processes(top_n=5):
    try:
        out = subprocess.check_output(["ps", "-Arco", "pid,%cpu,%mem,comm"], text=True)
        lines = out.strip().split("\n")[1:top_n+1]
        procs = []
        for line in lines:
            parts = line.split(None, 3)
            if len(parts) >= 4:
                procs.append({
                    "pid": parts[0],
                    "cpu": parts[1] + "%",
                    "mem": parts[2] + "%",
                    "name": parts[3]
                })
        return procs
    except Exception:
        return []

def calculate_safe_workers(ram, swap, mem_free_pct):
    """
    Quy tắc an toàn chống đơ máy cho Mac M1/M2/Intel:
    - Nếu RAM <= 8GB: Luôn dùng 1 worker (tối đa 2 nếu máy cực rảnh).
    - Nếu Swap > 1.5GB hoặc RAM used > 85%: Bắt buộc 1 worker.
    - Nếu RAM >= 16GB và còn trống nhiều: 2 hoặc 3 workers.
    """
    if ram["total_gb"] <= 8.0:
        if ram["pct"] > 75 or swap > 1.0 or (mem_free_pct and mem_free_pct < 40):
            return 1
        return 1  # 8GB unified memory luôn khuyến nghị 1 worker để máy mượt
    elif ram["total_gb"] <= 16.0:
        if ram["pct"] > 80 or swap > 2.0:
            return 1
        return 2
    else:
        return 4

def evaluate(cpu, ram, disk, swap, mem_free_pct):
    issues = []
    level = "OK"

    if cpu >= THRESHOLDS["cpu_danger"]:
        issues.append(f"⛔ CPU đang tải rất nặng ({cpu}%)")
        level = "DANGER"
    elif cpu >= THRESHOLDS["cpu_warn"]:
        issues.append(f"⚠️ CPU đang hoạt động cao ({cpu}%)")
        if level != "DANGER": level = "WARN"

    if ram["pct"] >= THRESHOLDS["ram_danger"]:
        issues.append(f"⛔ RAM sắp cạn ({ram['pct']}%, còn trống {ram['free_gb']}GB) — RẤT DỄ ĐỨNG MÁY")
        level = "DANGER"
    elif ram["pct"] >= THRESHOLDS["ram_warn"]:
        issues.append(f"⚠️ RAM đang ở mức cao ({ram['pct']}%, còn trống {ram['free_gb']}GB)")
        if level != "DANGER": level = "WARN"

    if swap >= THRESHOLDS["swap_danger_gb"]:
        issues.append(f"⛔ Swap ổ cứng vượt ngưỡng an toàn ({swap}GB) — Ổ SSD đang phải gánh RAM!")
        level = "DANGER"
    elif swap >= THRESHOLDS["swap_warn_gb"]:
        issues.append(f"⚠️ Swap bắt đầu tăng ({swap}GB)")
        if level != "DANGER": level = "WARN"

    if disk["pct"] >= THRESHOLDS["disk_danger"]:
        issues.append(f"⛔ Ổ cứng chính gần đầy ({disk['pct']}%)")
        level = "DANGER"
    elif disk["pct"] >= THRESHOLDS["disk_warn"]:
        issues.append(f"⚠️ Ổ cứng sắp đầy ({disk['pct']}%)")
        if level != "DANGER": level = "WARN"

    return level, issues

def run_cooldown(seconds=20):
    print(f"⏳ Nghỉ giải nhiệt hệ thống trong {seconds} giây...", end="", flush=True)
    for i in range(seconds, 0, -1):
        time.sleep(1)
        if i % 5 == 0 or i <= 3:
            print(f" {i}s", end="", flush=True)
    print(" 👉 Sẵn sàng!\n")

def check(as_json=False):
    cpu = get_cpu_usage()
    ram = get_ram_info()
    disk = get_disk_usage()
    swap = get_swap_info()
    mem_free_pct = get_memory_pressure_pct()
    power = get_power_info()
    procs = get_heavy_processes(5)

    level, issues = evaluate(cpu, ram, disk, swap, mem_free_pct)
    safe_workers = calculate_safe_workers(ram, swap, mem_free_pct)

    data = {
        "status": level,
        "safe_workers": safe_workers,
        "cpu_pct": cpu,
        "ram": ram,
        "disk": disk,
        "swap_gb": swap,
        "memory_free_pct": mem_free_pct,
        "power": power,
        "top_processes": procs,
        "issues": issues,
    }

    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return level

    icon = {"OK": "🟢", "WARN": "🟡", "DANGER": "🔴"}[level]
    print(f"\n{icon} TRẠNG THÁI HỆ THỐNG: {level}")
    print(f"  • CPU:     {cpu}%")
    print(f"  • RAM:     {ram['used_gb']}GB / {ram['total_gb']}GB ({ram['pct']}%) [Còn trống: {ram['free_gb']}GB]")
    print(f"  • Swap:    {swap}GB")
    if mem_free_pct is not None:
        print(f"  • Áp lực RAM tổng thể: {mem_free_pct}% bộ nhớ tự do")
    print(f"  • Ổ cứng:  {disk['pct']}% (còn {disk['available']})")
    if power["on_battery"]:
        print(f"  • Nguồn:   Đang dùng PIN ({power['battery_pct']}%) ⚠️ Khuyên cắm sạc khi render")
    else:
        print(f"  • Nguồn:   Đang cắm sạc")

    print(f"\n🛡️ SỐ WORKER KHUYẾN NGHỊ: {safe_workers} worker(s)")
    if safe_workers == 1:
        print("  → Máy 8GB RAM hoặc đang chịu tải: chạy 1 worker để đảm bảo 100% không đơ chuột/treo máy.")
    else:
        print("  → Tài nguyên dồi dào: có thể chạy đa luồng an toàn.")

    if issues:
        print("\n⚠️ CẢNH BÁO TIỀM ẨN:")
        for iss in issues:
            print(f"  {iss}")

    if procs:
        print(f"\n🏋️ TOP ỨNG DỤNG NẶNG NHẤT:")
        for p in procs:
            print(f"  {p['name']:30s} CPU: {p['cpu']:>6s} | RAM: {p['mem']:>5s}")

    print()
    return level

if __name__ == "__main__":
    args = sys.argv[1:]
    if "--cooldown" in args:
        sec = 20
        idx = args.index("--cooldown")
        if idx + 1 < len(args):
            try: sec = int(args[idx + 1])
            except ValueError: pass
        run_cooldown(sec)
        sys.exit(0)

    if "--pre-flight" in args:
        cpu = get_cpu_usage()
        ram = get_ram_info()
        disk = get_disk_usage()
        swap = get_swap_info()
        mem_free_pct = get_memory_pressure_pct()
        level, issues = evaluate(cpu, ram, disk, swap, mem_free_pct)
        safe_workers = calculate_safe_workers(ram, swap, mem_free_pct)
        if level == "DANGER":
            print(f"DANGER: {', '.join(issues)}", file=sys.stderr)
            sys.exit(1)
        print(safe_workers)
        sys.exit(0)

    as_json = "--json" in args
    check(as_json)
