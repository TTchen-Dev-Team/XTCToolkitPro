import re
import argparse
import platform

def v1(code: str, mode: str) -> str:
    try:
        if mode == "adb":
            # 第一段处理
            i1 = int(code[0:2])
            i2 = int(code[2:4])
            i3 = int(code[4:6])
            i4 = int(code[6:8])
            i5 = int(code[8:])
            
            i6 = i5 ^ (i3 + i4)
            i7 = i4 ^ i6
            i8 = i3 ^ i6
            i9 = i1 ^ i6
            i10 = i2 ^ i6
            
            i = ""
            for x in [i9, i10, i8, i7, i6]:
                if len(str(x)) == 1:
                    i += "0" + str(x)
                else:
                    i += str(x)
            
            # 第二段处理
            i1_2 = int(i[0:2])
            i2_2 = int(i[2:4])
            i3_2 = int(i[4:6])
            i4_2 = int(i[6:8])
            i5_2 = int(i[8:])
            
            i6_2 = i4_2 ^ i3_2
            i7_2 = i5_2 ^ i3_2
            i8_2 = i3_2 ^ (i6_2 + i7_2)
            i9_2 = i1_2 ^ i7_2
            i10_2 = i2_2 ^ i7_2
            
            i2_result = ""
            for x in [i9_2, i10_2, i6_2, i7_2, i8_2]:
                if len(str(x)) == 1:
                    i2_result += "0" + str(x)
                else:
                    i2_result += str(x)
            
            return i2_result
            
        elif mode == "zj":
            # 第一段处理
            i1 = int(code[0:2])
            i2 = int(code[2:4])
            i3 = int(code[4:])
            
            i5 = i3 ^ (i1 + i2)
            i6 = i1 ^ i5
            i4 = i2 ^ i5
            
            i = ""
            for x in [i6, i4, i5]:
                if len(str(x)) == 1:
                    i += "0" + str(x)
                else:
                    i += str(x)
            
            # 第二段处理
            i1_2 = int(i[0:2])
            i2_2 = int(i[2:4])
            i3_2 = int(i[4:])
            
            i5_2 = i2_2 ^ i1_2
            i6_2 = i3_2 ^ i1_2
            i4_2 = i1_2 ^ (i5_2 + i6_2)
            
            i2_result = ""
            for x in [i5_2, i6_2, i4_2]:
                if len(str(x)) == 1:
                    i2_result += "0" + str(x)
                else:
                    i2_result += str(x)
            
            return i2_result
            
    except Exception:
        return ""
    
    return ""


def v2(code: str, mode: str, key_id: int) -> str:
    try:
        if mode == "adb":
            num = 2
        else:
            num = 1
        
        if re.match(r"^\d+$", code):
            key = int(code[7]) ^ num
            v7 = (int(code[key]) - key + 10) % 10
            
            result1 = ""
            for i in range(7):
                cur_key = v7
                if i == key:
                    result1 += str(v7)
                else:
                    cur_int = int(code[i])
                    result1 += str((cur_int - cur_key + 10) % 10)
            
            key_value = int(result1[key_id])
            
            result = ""
            for i in range(7):
                if i == key_id:
                    cur_key = key_id
                else:
                    cur_key = key_value
                cur_int = int(result1[i])
                result += str((cur_int + cur_key) % 10)
            
            result += str(num ^ key_id)
            return result
        else:
            return ""
            
    except Exception:
        return ""


def get_code(code: str, mode: str) -> str:
    if len(code) == 8:
        for key_id in range(7):
            result = v2(code, mode, key_id)
            if result != code:
                break
        return result
    else:
        return v1(code, mode)