from machine import Pin, I2C, RTC
from ina219 import INA219
from logging import INFO
import time
import _thread
import os

SHUNT_OHMS = 0.1

# Initialize I2C
i2c = I2C(1, scl=Pin(22), sda=Pin(21))

# Initialize INA219
ina = INA219(SHUNT_OHMS, i2c, log_level=INFO)

# Configure INA219
try:
    ina.configure()
    print("INA219 configured")
except Exception as e:
    print(f"Error configuring INA219: {e}")

time_interval = 5
cumulative_energy_file = 'cumulative_energy.txt'

remaining_battery_percentage = 100


# ファイルの存在を確認
def file_exists(filename):
    try:
        # ファイルのステータスを取得
        os.stat(filename)
        return True
    except OSError:
        return False

# 累積消費電力量をファイルから読み込む
if file_exists(cumulative_energy_file):
    with open(cumulative_energy_file, 'r') as f:
        cumulative_energy_consumed_Wh = float(f.read().strip())
else:
    cumulative_energy_consumed_Wh = 0

battery_capacity_mAh = 1000  # バッテリー容量設定
battery_capacity_Wh = (battery_capacity_mAh * 5.0) / 1000  # ESP32の定格電圧5.0V

# ファイルのヘッダー書き込み
if not file_exists('remaining_battery.csv'):
    with open('remaining_battery.csv', 'w') as f:
        f.write('Time,Remaining Battery Percentage\n')  # 新規ファイルの場合のみヘッダーを追加

def get_info():
    try:
        voltage = ina.voltage()
        current = ina.current()
        power = ina.power()
        return voltage, current, power
    except Exception as e:
        print(f"Error getting INA219 data: {e}")
        return None, None, None

def exec():
    global cumulative_energy_consumed_Wh, remaining_battery_percentage
    
    voltage, current, power = get_info()
    print(f"{voltage:.2f}V, {current:.2f}mA, {power:.2f}mW")

    while True:
        voltage, current, power = get_info()
        power_W = power / 1000  # 消費電力をWに変換

        time_diff_hours = time_interval / 3600.0  # 計測間隔をhoursに変換

        energy_consumed_Wh = power_W * time_diff_hours  # 消費電力量(Wh)を計算

        cumulative_energy_consumed_Wh += energy_consumed_Wh  # 累計消費電力量を計算

        # エネルギー消費量をファイルに保存
        with open(cumulative_energy_file, 'w') as f:
            f.write(f"{cumulative_energy_consumed_Wh}")

        remaining_energy_Wh = battery_capacity_Wh - cumulative_energy_consumed_Wh  # バッテリーの残量を計算(Wh)

        remaining_battery_percentage = (remaining_energy_Wh / battery_capacity_Wh) * 100  # バッテリーの残量を計算(%)

        print(f"Remaining Battery: {remaining_battery_percentage:.2f}%")

        # CSVファイルに時間と残量を書き込む
        current_time = time.time()
        with open('remaining_battery.csv', 'a') as f:
            f.write(f"{current_time},{remaining_battery_percentage:.2f}\n")
            f.flush()  # データを即座にディスクに書き込む

        time.sleep(time_interval)

if __name__ == '__main__':
    _thread.start_new_thread(exec, ())