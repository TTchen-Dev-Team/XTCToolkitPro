import os
import sys
import subprocess
import time
import re
import ctypes
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


# ==================== 配置类 ====================

@dataclass
class ToolPaths:
    """工具路径配置"""
    base_path: Path
    bin_folder: Path
    firmware_281_folder: Path
    tool_folder: Path
    
    # 核心工具
    qsahara_exe: Path
    fh_loader_exe: Path
    firehose_elf: Path
    twrp_img: Path
    dm_zip_path: Path
    
    # 固件配置
    firmware_xml_list: List[str] = None
    patch_xml: str = "patch0.xml"
    max_retry: int = 3
    
    def __post_init__(self):
        if self.firmware_xml_list is None:
            self.firmware_xml_list = ["rawprogram0.xml", "rawprogram1.xml", "rawprogram2.xml"]
        
        # 确保所有路径都是Path对象
        self.base_path = Path(self.base_path)
        self.bin_folder = Path(self.bin_folder)
        self.firmware_281_folder = Path(self.firmware_281_folder)
        self.tool_folder = Path(self.tool_folder)
        self.qsahara_exe = Path(self.qsahara_exe)
        self.fh_loader_exe = Path(self.fh_loader_exe)
        self.firehose_elf = Path(self.firehose_elf)
        self.twrp_img = Path(self.twrp_img)
        self.dm_zip_path = Path(self.dm_zip_path)
    
    @classmethod
    def create_default(cls, base_path: Optional[Path] = None) -> 'ToolPaths':
        """创建默认配置"""
        if base_path is None:
            if getattr(sys, 'frozen', False):
                base_path = Path(sys.executable).parent
            else:
                base_path = Path(__file__).parent
        
        # 修改这里的路径配置
        bin_folder = base_path / "."  # 修改为当前目录
        firmware_281_folder = base_path / "EDL" / "ND03_rooting" / "281"  # 修改为新的281固件路径
        tool_folder = base_path / "EDL" / "ND03_rooting" / "260116"  # 修改为新的工具路径
        
        return cls(
            base_path=base_path,
            bin_folder=bin_folder,
            firmware_281_folder=firmware_281_folder,
            tool_folder=tool_folder,
            qsahara_exe=bin_folder / "QSaharaServer.exe",
            fh_loader_exe=bin_folder / "fh_loader.exe",
            firehose_elf=bin_folder / "prog_firehose_ddr.elf.elf",
            twrp_img=tool_folder / "recovery.img",
            dm_zip_path=tool_folder / "Dm-Verity.zip"
        )


class DeviceMode(Enum):
    """设备模式枚举"""
    UNKNOWN = "unknown"
    EDL = "edl"  # 9008模式
    FASTBOOT = "fastboot"
    ADB = "adb"
    SIDELOAD = "sideload"


# ==================== 异常类 ====================

class RootToolError(Exception):
    """基础异常类"""
    pass


class FileNotFoundError(RootToolError):
    """文件未找到异常"""
    pass


class DeviceNotFoundError(RootToolError):
    """设备未找到异常"""
    pass


class CommandExecutionError(RootToolError):
    """命令执行异常"""
    pass


class PermissionError(RootToolError):
    """权限异常"""
    pass


# ==================== 工具函数 ====================

class CommandRunner:
    """命令执行器"""
    
    def __init__(self, working_dir: Optional[Path] = None, encoding: str = 'gbk'):
        self.working_dir = str(working_dir) if working_dir else None
        self.encoding = encoding
    
    def run(self, cmd: str, timeout: int = 300, show_output: bool = True) -> Tuple[bool, str]:
        """
        执行系统命令
        
        Args:
            cmd: 要执行的命令
            timeout: 超时时间（秒）
            show_output: 是否显示输出
            
        Returns:
            (成功标志, 输出信息)
        """
        if show_output:
            print(f"[执行命令] {cmd}")
        
        try:
            proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding=self.encoding,
                errors='ignore',
                cwd=self.working_dir
            )
            output, _ = proc.communicate(timeout=timeout)
            
            if show_output and output:
                print(output.strip())
            
            return proc.returncode == 0, output
        
        except subprocess.TimeoutExpired:
            error_msg = f"命令执行超时（{timeout}秒）"
            if show_output:
                print(f"❌ {error_msg}")
            return False, error_msg
        
        except Exception as e:
            error_msg = f"命令执行异常：{str(e)}"
            if show_output:
                print(f"❌ {error_msg}")
            return False, error_msg


class DeviceDetector:
    """设备检测器"""
    
    def __init__(self, cmd_runner: CommandRunner):
        self.cmd_runner = cmd_runner
        self.edl_keywords = ["Qualcomm", "HS-USB Diagnostics", "9008", "Diagnostics Port"]
    
    def scan_edl_port(self) -> Optional[str]:
        """扫描EDL(9008)端口"""
        try:
            success, output = self.cmd_runner.run(
                "wmic path Win32_SerialPort get DeviceID,Description", 
                timeout=10, 
                show_output=False
            )
            
            if not success:
                return None
            
            for line in output.splitlines():
                line = line.strip()
                if not line or line.startswith("DeviceID"):
                    continue
                
                parts = line.split()
                if not parts:
                    continue
                
                port = parts[0]
                desc = " ".join(parts[1:])
                
                for keyword in self.edl_keywords:
                    if keyword.lower() in desc.lower():
                        return port
            
            return None
        
        except Exception:
            return None
    
    def wait_for_edl_port(self, timeout: int = 300, check_interval: int = 2) -> Optional[str]:
        """等待EDL端口出现"""
        start_time = time.time()
        print(f"[等待中] 开始循环检测9008端口，超时时间{timeout}秒...")
        
        while True:
            port = self.scan_edl_port()
            if port:
                print(f"✅ 成功识别到9008端口：{port}")
                return port
            
            elapsed = int(time.time() - start_time)
            if elapsed >= timeout:
                print(f"❌ 等待超时，已等待{timeout}秒，未检测到9008端口")
                choice = input("是否继续等待？(y/n)：").strip().lower()
                if choice == 'y':
                    start_time = time.time()
                    print("[继续等待] 重置超时时间，继续检测端口...")
                    continue
                else:
                    print("[用户终止] 停止等待")
                    return None
            
            print(f"[等待中] 已等待{elapsed}秒，未检测到9008端口...")
            time.sleep(check_interval)
    
    def check_fastboot(self) -> bool:
        """检查Fastboot设备"""
        success, output = self.cmd_runner.run("fastboot devices", timeout=10, show_output=False)
        return success and bool(output.strip())
    
    def wait_for_fastboot(self, timeout: int = 300, check_interval: int = 2) -> bool:
        """等待Fastboot设备"""
        start_time = time.time()
        print(f"[等待中] 开始循环检测Fastboot设备，超时时间{timeout}秒...")
        
        while True:
            if self.check_fastboot():
                print("✅ 成功识别到Fastboot设备")
                return True
            
            elapsed = int(time.time() - start_time)
            if elapsed >= timeout:
                print(f"❌ 等待超时，已等待{timeout}秒，未检测到Fastboot设备")
                choice = input("是否继续等待？(y/n)：").strip().lower()
                if choice == 'y':
                    start_time = time.time()
                    print("[继续等待] 重置超时时间，继续检测设备...")
                    continue
                else:
                    print("[用户终止] 停止等待")
                    return False
            
            print(f"[等待中] 已等待{elapsed}秒，未检测到Fastboot设备...")
            time.sleep(check_interval)
    
    def check_adb(self) -> List[str]:
        """检查ADB设备，返回设备列表"""
        success, output = self.cmd_runner.run("adb devices", timeout=10, show_output=False)
        if not success:
            return []
        
        devices = []
        for line in output.splitlines():
            if line.strip() and not line.startswith("List of devices") and "\tdevice" in line:
                devices.append(line.split("\t")[0])
        
        return devices
    
    def check_adb_shell(self) -> bool:
        """检查ADB shell是否可用"""
        success, output = self.cmd_runner.run("adb shell id", timeout=10, show_output=False)
        return success and "uid=" in output
    
    def wait_for_adb(self, timeout: int = 180, check_interval: int = 3) -> bool:
        """等待ADB连接"""
        start_time = time.time()
        print(f"[等待中] 等待ADB连接，超时时间{timeout}秒...")
        
        while True:
            devices = self.check_adb()
            if devices and self.check_adb_shell():
                print(f"✅ ADB连接成功，设备：{', '.join(devices)}")
                return True
            
            elapsed = int(time.time() - start_time)
            if elapsed >= timeout:
                print(f"❌ 等待ADB连接超时（已等待{timeout}秒）")
                choice = input("是否继续等待？(y/n)：").strip().lower()
                if choice == 'y':
                    start_time = time.time()
                    print("[继续等待] 重置超时时间...")
                    continue
                else:
                    return False
            
            print(f"[等待中] 已等待{elapsed}秒，ADB未就绪...")
            time.sleep(check_interval)
    
    def get_device_mode(self) -> DeviceMode:
        """获取当前设备模式"""
        if self.scan_edl_port():
            return DeviceMode.EDL
        if self.check_fastboot():
            return DeviceMode.FASTBOOT
        if self.check_adb():
            return DeviceMode.ADB
        return DeviceMode.UNKNOWN
    
    def print_status(self):
        """打印所有设备状态"""
        print("\n" + "="*70)
        print("设备连接状态检测")
        print("="*70)
        
        print("\n1. 9008模式端口：")
        edl_port = self.scan_edl_port()
        if edl_port:
            print(f"✅ 检测到9008端口：{edl_port}")
        else:
            print("❌ 未检测到9008端口")
        
        print("\n2. Fastboot模式设备：")
        if self.check_fastboot():
            print("✅ 检测到Fastboot设备")
        else:
            print("❌ 未检测到Fastboot设备")
        
        print("\n3. ADB调试设备：")
        devices = self.check_adb()
        if devices:
            print(f"✅ 检测到ADB设备：{', '.join(devices)}")
        else:
            print("❌ 未检测到ADB设备")


# ==================== 文件校验器 ====================

class FileValidator:
    """文件校验器"""
    
    def __init__(self, paths: ToolPaths):
        self.paths = paths
    
    def check_file(self, file_path: Path, description: str) -> bool:
        """检查单个文件是否存在"""
        if not file_path.exists():
            print(f"❌ 文件缺失：{description} - {file_path}")
            return False
        return True
    
    def check_directory(self, dir_path: Path, description: str) -> bool:
        """检查目录是否存在"""
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"❌ 目录缺失：{description} - {dir_path}")
            return False
        return True
    
    def check_core_tools(self) -> Tuple[bool, List[str]]:
        """检查核心工具文件"""
        core_files = [
            (self.paths.qsahara_exe, "QSaharaServer (应放在程序根目录)"),
            (self.paths.fh_loader_exe, "fh_loader (应放在程序根目录)"),
            (self.paths.firehose_elf, "Firehose引导文件 (应放在程序根目录)"),
            (self.paths.bin_folder / "adb.exe", "ADB (应放在程序根目录)"),
            (self.paths.bin_folder / "fastboot.exe", "Fastboot (应放在程序根目录)"),
            (self.paths.bin_folder / "AdbWinApi.dll", "ADB API DLL (应放在程序根目录)"),
            (self.paths.bin_folder / "AdbWinUsbApi.dll", "ADB USB DLL (应放在程序根目录)")
        ]
        
        missing = []
        for file_path, desc in core_files:
            if not self.check_file(file_path, desc):
                missing.append(file_path.name)
        
        return len(missing) == 0, missing

    def check_firmware_files(self) -> Tuple[bool, List[str]]:
        """检查固件文件"""
        if not self.check_directory(self.paths.firmware_281_folder, "281固件目录 (EDL\\ND03_rooting\\281)"):
            return False, ["EDL\\ND03_rooting\\281 文件夹不存在"]
        
        missing = []
        for xml in self.paths.firmware_xml_list + [self.paths.patch_xml]:
            xml_path = self.paths.firmware_281_folder / xml
            if not self.check_file(xml_path, f"固件XML文件 {xml}"):
                missing.append(xml)
        
        return len(missing) == 0, missing

    def check_root_files(self) -> Tuple[bool, List[str]]:
        """检查Root相关文件"""
        root_files = [
            (self.paths.twrp_img, "TWRP镜像 (应放在 EDL\\ND03_rooting\\260116)"),
            (self.paths.dm_zip_path, "Dm-Verity补丁 (应放在 EDL\\ND03_rooting\\260116)")
        ]
        
        missing = []
        for file_path, desc in root_files:
            if not self.check_file(file_path, desc):
                missing.append(file_path.name)
        
        return len(missing) == 0, missing
    
    def check_all(self) -> bool:
        """检查所有必需文件"""
        print("正在检查刷机所需的全部文件...")
        
        core_ok, core_missing = self.check_core_tools()
        fw_ok, fw_missing = self.check_firmware_files()
        root_ok, root_missing = self.check_root_files()
        
        all_missing = []
        if not core_ok:
            all_missing.append(f"根目录缺失核心工具：{', '.join(core_missing)}")
        if not fw_ok:
            all_missing.append(f"EDL/rooting/281文件夹缺失固件文件：{', '.join(fw_missing)}")
        if not root_ok:
            all_missing.append(f"EDL/rooting/260116文件夹缺失ROOT文件：{', '.join(root_missing)}")
        
        if not all_missing:
            print("✅ 所有必备文件校验通过，无缺失")
            return True
        else:
            print("❌ 文件校验失败，以下文件缺失：")
            for item in all_missing:
                print(f"  - {item}")
            return False


# ==================== 权限管理器 ====================

class PermissionManager:
    """权限管理器"""
    
    @staticmethod
    def is_admin() -> bool:
        """检查是否具有管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def setup_environment(paths: ToolPaths):
        """设置运行环境"""
        # 设置控制台编码
        try:
            os.system("chcp 936 >nul 2>&1")
        except:
            pass


# ==================== 固件刷写器 ====================

class FirmwareFlasher:
    """固件刷写器"""
    
    def __init__(self, paths: ToolPaths, cmd_runner: CommandRunner):
        self.paths = paths
        self.cmd_runner = cmd_runner
    
    def load_firehose(self, port: str, max_retry: int = None) -> bool:
        """加载Firehose引导文件"""
        if max_retry is None:
            max_retry = self.paths.max_retry
        
        for retry in range(max_retry):
            print(f"\n加载高通9008引导文件（重试次数：{retry+1}/{max_retry}）...")
            cmd = f'"{self.paths.qsahara_exe}" -p {port} -s 13:"{self.paths.firehose_elf}"'
            success, output = self.cmd_runner.run(cmd, timeout=60)
            
            if success:
                print("✅ Firehose引导文件加载成功")
                return True
            
            print(f"❌ 引导文件加载失败，错误信息：{output}")
            if retry == max_retry - 1:
                choice = input("已达到最大重试次数，是否继续重试？(y/n)：").strip().lower()
                if choice == 'y':
                    retry = -1
                    continue
                else:
                    print("[用户终止] 引导文件加载中断")
                    return False
            time.sleep(1)
        
        return False
    
    def flash_xml(self, xml_name: str, step_num: int, max_retry: int = None) -> bool:
        """刷写单个XML文件"""
        if max_retry is None:
            max_retry = self.paths.max_retry
        
        xml_path = self.paths.firmware_281_folder / xml_name
        
        for retry in range(max_retry):
            print(f"\n[{step_num}] 刷入{xml_name}（重试次数：{retry+1}/{max_retry}）...")
            cmd = (
                f'"{self.paths.fh_loader_exe}" --port={port} --memoryname=EMMC '
                f'--search_path="{self.paths.firmware_281_folder}" --sendxml="{xml_path}" --noprompt'
            )
            success, output = self.cmd_runner.run(cmd, timeout=300)
            
            if success:
                print(f"✅ {xml_name} 刷入完成")
                return True
            
            print(f"❌ {xml_name} 刷入失败，错误信息：{output}")
            if retry == max_retry - 1:
                choice = input("已达到最大重试次数，是否继续重试？(y/n)：").strip().lower()
                if choice == 'y':
                    retry = -1
                    continue
                else:
                    print("[用户终止] 固件刷入中断")
                    return False
            time.sleep(1)
        
        return False
    
    def flash_full_firmware(self, port: str) -> bool:
        """刷写完整固件"""
        print("\n" + "="*70)
        print("【阶段1：刷入Z10 281官方全量固件】")
        print("="*70)
        
        # 1. 加载引导文件
        if not self.load_firehose(port):
            return False
        
        # 2. 刷写所有rawprogram XML
        for idx, xml_name in enumerate(self.paths.firmware_xml_list, start=2):
            if not self.flash_xml(xml_name, idx):
                return False
        
        # 3. 刷写补丁文件
        if not self.flash_xml(self.paths.patch_xml, 5):
            return False
        
        print("\n✅ 【阶段1完成】281全量固件刷入全部成功！")
        return True


# ==================== TWRP操作器 ====================

class TWRPOperator:
    """TWRP操作器"""
    
    def __init__(self, paths: ToolPaths, cmd_runner: CommandRunner, device_detector: DeviceDetector):
        self.paths = paths
        self.cmd_runner = cmd_runner
        self.device_detector = device_detector
    
    def boot_twrp(self, max_retry: int = None) -> bool:
        """启动TWRP镜像"""
        if max_retry is None:
            max_retry = self.paths.max_retry
        
        for retry in range(max_retry):
            print(f"\n临时启动TWRP恢复镜像（重试次数：{retry+1}/{max_retry}）...")
            cmd = f'fastboot boot "{self.paths.twrp_img}"'
            success, output = self.cmd_runner.run(cmd, timeout=60)
            
            if success:
                print("✅ TWRP启动命令已发送，正在等待TWRP系统启动...")
                return True
            
            print(f"❌ TWRP镜像启动失败，错误信息：{output}")
            if retry == max_retry - 1:
                choice = input("已达到最大重试次数，是否继续重试？(y/n)：").strip().lower()
                if choice == 'y':
                    retry = -1
                    continue
                else:
                    print("[用户终止] TWRP启动中断")
                    return False
            time.sleep(1)
        
        return False
    
    def mount_partition(self, partition: str, max_retry: int = None) -> bool:
        """挂载分区"""
        if max_retry is None:
            max_retry = self.paths.max_retry
        
        for retry in range(max_retry):
            cmd = f'adb shell twrp mount {partition}'
            success, output = self.cmd_runner.run(cmd, timeout=30)
            
            if success:
                print(f"✅ {partition}分区挂载成功")
                return True
            
            print(f"❌ {partition}分区挂载失败，重试{retry+1}/{max_retry}，错误：{output}")
            time.sleep(1)
        
        return False
    
    def format_data(self, max_retry: int = None) -> bool:
        """格式化Data分区"""
        if max_retry is None:
            max_retry = self.paths.max_retry
        
        for retry in range(max_retry):
            cmd = 'adb shell twrp format data'
            success, output = self.cmd_runner.run(cmd, timeout=120)
            
            if success:
                print("✅ Data分区格式化完成")
                return True
            
            print(f"❌ Data分区格式化失败，重试{retry+1}/{max_retry}，错误：{output}")
            time.sleep(1)
        
        return False
    
    def enter_sideload(self, max_retry: int = None) -> bool:
        """进入Sideload模式"""
        if max_retry is None:
            max_retry = self.paths.max_retry
        
        for retry in range(max_retry):
            print(f"正在进入Sideload模式（重试{retry+1}/{max_retry}）...")
            cmd = 'adb shell twrp sideload'
            success, output = self.cmd_runner.run(cmd, timeout=30, show_output=False)
            
            time.sleep(3)  # 等待sideload服务启动
            
            # 检测sideload是否就绪
            devices = self.device_detector.check_adb()
            if devices:
                print("✅ 已进入Sideload模式")
                return True
            
            print(f"❌ 进入Sideload模式失败，错误：{output}")
            time.sleep(1)
        
        return False
    
    def sideload_patch(self, max_retry: int = None) -> bool:
        """刷入补丁文件"""
        if max_retry is None:
            max_retry = self.paths.max_retry
        
        percent_re = re.compile(r'\((~?)(\d+)%\)')
        
        for retry in range(max_retry):
            print(f"\n正在刷入Dm-Verity.zip补丁（重试{retry+1}/{max_retry}）...")
            cmd = f'adb sideload "{self.paths.dm_zip_path}"'
            print(f"[执行命令] {cmd}")
            
            try:
                proc = subprocess.Popen(
                    cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding='gbk',
                    errors='ignore',
                    cwd=str(self.paths.base_path),
                    bufsize=1,
                    universal_newlines=True
                )
                
                for line in iter(proc.stdout.readline, ''):
                    if line:
                        line = line.strip()
                        print(line)
                        match = percent_re.search(line)
                        if match:
                            percent = match.group(2)
                            print(f"👉 当前刷入进度：{percent}%")
                
                proc.wait(timeout=180)
                
                if proc.returncode == 0:
                    print("✅ Dm-Verity ROOT补丁刷入完成")
                    return True
                else:
                    print(f"❌ 补丁刷入失败，返回码：{proc.returncode}")
                    
            except Exception as e:
                print(f"❌ 刷入异常：{str(e)}")
            
            if retry < max_retry - 1:
                print("2秒后自动重试...")
                time.sleep(2)
        
        return False
    
    def run_full_root_procedure(self) -> bool:
        """执行完整的TWRP ROOT流程"""
        print("\n" + "="*70)
        print("【阶段2：启动TWRP刷入ROOT补丁】")
        print("="*70)
        
        # 1. 启动TWRP
        if not self.boot_twrp():
            return False
        
        # 2. 等待ADB连接
        print("\n等待TWRP启动，正在检测ADB连接...")
        time.sleep(5)
        if not self.device_detector.wait_for_adb():
            return False
        
        # 3. 挂载vendor
        print("\n挂载vendor分区...")
        if not self.mount_partition("vendor"):
            choice = input("vendor分区挂载失败，是否忽略此步骤继续？(y/n)：").strip().lower()
            if choice != 'y':
                return False
        
        # 4. 挂载system
        print("\n挂载system分区...")
        if not self.mount_partition("system"):
            choice = input("system分区挂载失败，是否忽略此步骤继续？(y/n)：").strip().lower()
            if choice != 'y':
                return False
        
        # 5. 格式化Data
        print("\n执行Data分区格式化...")
        if not self.format_data():
            choice = input("Data分区格式化失败，是否继续后续步骤？(y/n)：").strip().lower()
            if choice != 'y':
                return False
        
        # 6. 挂载Data
        print("\n挂载Data分区...")
        if not self.mount_partition("data"):
            choice = input("Data分区挂载失败，是否继续后续步骤？(y/n)：").strip().lower()
            if choice != 'y':
                return False
        
        # 7. 进入Sideload模式并刷入补丁
        print("\n进入Sideload模式，准备刷入Dm-Verity ROOT补丁...")
        if not self.enter_sideload():
            choice = input("进入Sideload模式失败，是否手动操作后重试？(y/n)：").strip().lower()
            if choice != 'y':
                return False
        
        if not self.sideload_patch():
            return False
        
        print("\n✅ 【阶段2完成】TWRP操作+ROOT补丁刷入全部成功！")
        return True


# ==================== 主控制器 ====================

class RootToolController:
    """主控制器"""
    
    def __init__(self, paths: Optional[ToolPaths] = None):
        self.paths = paths or ToolPaths.create_default()
        self.cmd_runner = CommandRunner(working_dir=self.paths.base_path)
        self.device_detector = DeviceDetector(self.cmd_runner)
        self.file_validator = FileValidator(self.paths)
        self.firmware_flasher = FirmwareFlasher(self.paths, self.cmd_runner)
        self.twrp_operator = TWRPOperator(self.paths, self.cmd_runner, self.device_detector)
        self.permission_manager = PermissionManager()
    
    def initialize(self) -> bool:
        """初始化环境"""
        print("初始化程序环境...")
        
        # 设置环境
        self.permission_manager.setup_environment(self.paths)
        
        print("✅ 程序环境初始化完成")
        return True
    
    def run_one_key_root(self) -> bool:
        """一键全流程ROOT"""
        print("\n" + "="*70)
        print("【一键全流程ROOT】")
        print("本次执行流程：")
        print("1. 9008模式刷入281官方全量固件")
        print("2. 手动重启手表，进入Fastboot模式")
        print("3. 启动TWRP，执行对应操作+刷入Dm-Verity ROOT补丁")
        print("="*70)
        
        # 文件校验
        if not self.file_validator.check_all():
            return False
        
        # 检测9008端口
        print("\n正在检测9008端口...")
        port = self.device_detector.scan_edl_port()
        if not port:
            print("❌ 未自动检测到9008端口")
            port = self.device_detector.wait_for_edl_port()
            if not port:
                return False
        else:
            print(f"✅ 自动识别到9008端口：{port}")
        
        # 刷入固件
        if not self.firmware_flasher.flash_full_firmware(port):
            return False
        
        # 等待Fastboot
        print("\n" + "="*70)
        print("固件刷入完成，准备进入Fastboot环节")
        print("👉 请操作手表：手动重启设备，重启后请进入Fastboot模式")
        print("="*70)
        
        if not self.device_detector.wait_for_fastboot():
            return False
        
        # TWRP操作
        if not self.twrp_operator.run_full_root_procedure():
            return False
        
        # 完成
        print("\n" + "🎉"*30)
        print("✅ 全流程ROOT操作已全部执行完成！")
        print("👉 现在可以手动重启手表，进入系统即可获取ROOT权限")
        print("🎉"*30)
        
        return True
    
    def flash_firmware_only(self) -> bool:
        """仅刷写固件"""
        print("\n" + "="*70)
        print("【单独刷入281全量固件】")
        print("="*70)
        
        # 文件校验
        core_ok, core_missing = self.file_validator.check_core_tools()
        if not core_ok:
            print(f"❌ 核心工具缺失：{', '.join(core_missing)}")
            return False
        
        fw_ok, fw_missing = self.file_validator.check_firmware_files()
        if not fw_ok:
            print(f"❌ 固件文件缺失：{', '.join(fw_missing)}")
            return False
        
        print("✅ 固件文件校验通过")
        
        # 检测9008端口
        port = self.device_detector.scan_edl_port()
        if not port:
            port = self.device_detector.wait_for_edl_port()
            if not port:
                return False
        
        # 刷写固件
        return self.firmware_flasher.flash_full_firmware(port)
    
    def run_twrp_only(self) -> bool:
        """仅执行TWRP操作"""
        print("\n" + "="*70)
        print("【单独执行TWRP操作+刷Dm-Verity ROOT补丁】")
        print("="*70)
        
        # 文件校验
        root_ok, root_missing = self.file_validator.check_root_files()
        if not root_ok:
            print(f"❌ 缺失文件：{', '.join(root_missing)}")
            return False
        
        # 检测Fastboot
        print("正在检测Fastboot设备...")
        if not self.device_detector.check_fastboot():
            print("❌ 未检测到Fastboot设备")
            return False
        
        print("✅ Fastboot设备检测通过")
        
        # TWRP操作
        return self.twrp_operator.run_full_root_procedure()
    
    def check_devices(self):
        """检测设备状态"""
        self.device_detector.print_status()


# ==================== 交互式菜单 ====================

class InteractiveMenu:
    """交互式菜单"""
    
    def __init__(self, controller: RootToolController):
        self.controller = controller
    
    def clear_screen(self):
        """清屏"""
        os.system("cls" if os.name == "nt" else "clear")
    
    def show_main_menu(self):
        """显示主菜单"""
        self.clear_screen()
        print("="*70)
        print("          小天才Z10 Root工具箱 by 雪精灵")
        print("="*70)
        print("1. 一键执行全流程ROOT（推荐）")
        print("2. 单独刷入281全量固件（9008模式）")
        print("3. 单独执行TWRP操作+刷Dm-Verity ROOT补丁")
        print("4. 检测设备连接状态（9008/Fastboot/ADB）")
        print("5. 退出工具")
        print("="*70)
        
        choice = input("请输入功能序号，按回车执行：").strip()
        return choice
    
    def run(self):
        """运行菜单循环"""
        while True:
            choice = self.show_main_menu()
            
            if choice == '1':
                self.controller.run_one_key_root()
                self.pause()
            elif choice == '2':
                self.controller.flash_firmware_only()
                self.pause()
            elif choice == '3':
                self.controller.run_twrp_only()
                self.pause()
            elif choice == '4':
                self.controller.check_devices()
                self.pause()
            elif choice == '5':
                print("感谢使用，退出程序...")
                break
            else:
                print("❌ 输入错误，请输入1-5之间的序号")
                time.sleep(1.5)
    
    def pause(self):
        """暂停"""
        print("\n按任意键返回主菜单...")
        try:
            os.system("pause >nul 2>&1")
        except:
            input()


# ==================== 便捷函数API ====================

def create_controller(base_path: Optional[str] = None) -> RootToolController:
    """
    创建控制器实例
    
    Args:
        base_path: 基础路径，如果为None则使用脚本所在目录
    
    Returns:
        RootToolController实例
    """
    if base_path:
        paths = ToolPaths.create_default(Path(base_path))
        return RootToolController(paths)
    return RootToolController()


def one_key_root(base_path: Optional[str] = None) -> bool:
    """
    一键全流程ROOT
    
    Args:
        base_path: 基础路径
    
    Returns:
        是否成功
    """
    controller = create_controller(base_path)
    if not controller.initialize():
        return False
    return controller.run_one_key_root()


def flash_firmware(base_path: Optional[str] = None) -> bool:
    """
    仅刷写固件
    
    Args:
        base_path: 基础路径
    
    Returns:
        是否成功
    """
    controller = create_controller(base_path)
    if not controller.initialize():
        return False
    return controller.flash_firmware_only()


def run_twrp(base_path: Optional[str] = None) -> bool:
    """
    仅执行TWRP操作
    
    Args:
        base_path: 基础路径
    
    Returns:
        是否成功
    """
    controller = create_controller(base_path)
    if not controller.initialize():
        return False
    return controller.run_twrp_only()


def check_devices(base_path: Optional[str] = None):
    """
    检测设备状态
    
    Args:
        base_path: 基础路径
    """
    controller = create_controller(base_path)
    controller.initialize()
    controller.check_devices()


# ==================== 命令行入口 ====================

def main():
    """命令行入口函数"""
    try:
        controller = create_controller()
        if not controller.initialize():
            print("初始化失败，按任意键退出...")
            os.system("pause >nul 2>&1")
            return 1
        
        menu = InteractiveMenu(controller)
        menu.run()
        
    except KeyboardInterrupt:
        print("\n\n用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序出现未知异常：{str(e)}")
        import traceback
        traceback.print_exc()
        print("\n按任意键退出...")
        os.system("pause >nul 2>&1")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())