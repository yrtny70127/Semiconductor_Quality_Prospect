import os
print(os.getcwd())          # 현재 작업 위치
print(os.listdir("."))      # 현재 폴더 목록



/
['cdrom', 'snap', 'home', 'run', 'opt', 'sbin.usr-is-merged', 'sbin', 'sys', 'lost+found', 'usr', 'lib64', 'proc', 'srv', 'media', 'swap.img', 'dev', 'root', 'bin.usr-is-merged', 'lib', 'tmp', 'mnt', 'boot', 'lib.usr-is-merged', 'bin', 'var', 'etc']

지금 os.listdir(".") 결과가 리눅스 루트(/) 입니다.
즉 팀원 환경의 cwd가 /라서 uci-secom.csv가 당연히 안 보이는 상황이에요.

팀원 쪽에서 레포가 있는 폴더로 cwd를 옮겨야 합니다.

팀원에게 아래를 실행하게 해주세요:

import os
print(os.getcwd())
그리고 레포가 있는 경로로 chdir:

import os
os.chdir("/home/사용자명/Project_Semiconductor")  # 팀원 PC 실제 경로로 변경
그 다음:

df = pd.read_csv("SECOM/uci-secom.csv")
요점
지금은 팀원 환경이 /에서 실행 중이라 파일을 못 찾는 거고,
팀원 PC에 레포를 클론한 위치로 cwd만 맞추면 해결됩니다.

팀원 레포 위치를 알려주면, 정확한 os.chdir(...) 경로로 써줄게요.

C:\
['$Recycle.Bin', '$WINRE_BACKUP_PARTITION.MARKER', '.GamingRoot', 'Adjustment Program', 'AMD', 'CrashRepoterLog.txt', 'Documents and Settings', 'DumpStack.log', 'DumpStack.log.tmp', 'hiberfil.sys', 'inetpub', 'Intel', 'mylog.log', 'Nexon', 'OneDriveTemp', 'pagefile.sys', 'PerfLogs', 'Program Files', 'Program Files (x86)', 'ProgramData', 'Recovery', 'RHDSetup.log', 'Riot Games', 'swapfile.sys', 'System Volume Information', 'Users', 'Windows', 'XboxGames']

아래 코드로 레포 폴더를 찾게 해주세요.

import os

base = r"C:\Users"
for user in os.listdir(base):
    user_dir = os.path.join(base, user)
    if os.path.isdir(user_dir):
        print(user_dir)
레포가 있는 위치(예: C:\Users\0726b\Documents\Project_Semiconductor)를 찾았으면 이동:

import os
os.chdir(r"C:\Users\0726b\Documents\Project_Semiconductor")  # 실제 경로로 교체
print(os.getcwd())
그 다음:

df = pd.read_csv("SECOM/uci-secom.csv")
만약 레포 폴더 이름이 확실하면, 한 번에 찾아주는 코드도 가능:

import os

target = "Project_Semiconductor"  # 실제 폴더명으로 교체
for root, dirs, files in os.walk(r"C:\Users"):
    if target in dirs:
        print("FOUND:", os.path.join(root, target))
        break
찾힌 경로를 알려주면, 팀원용 os.chdir(...) 라인을 정확히 만들어줄게요.



팀원도 레포 루트에 있는 uci-secom.csv 위치에 두면 됩니다.
즉, 팀원 PC에서도 폴더 구조가 아래처럼 동일해야 합니다.

<레포_루트>/
  SECOM/
    uci-secom.csv
예시(Windows):

C:\Users\0726b\Documents\Project_Semiconductor\SECOM\uci-secom.csv
그리고 팀원은 레포 루트에서 노트북을 열고 실행하거나, 아래 한 줄로 cwd를 맞춘 뒤 실행하면 됩니다.

import os
os.chdir(r"C:\Users\0726b\Documents\Project_Semiconductor")  # 팀원 실제 경로
요점: 팀원 PC에도 동일한 레포 구조로 파일이 있어야 합니다. Live Share만으로는 데이터 파일이 공유되지 않습니다.


가능해요. 가장 일반적인 방법은 팀원이 레포를 직접 클론/풀해서 로컬에 똑같이 받는 겁니다.

1) 레포 전체 받기(권장)

git clone <https://github.com/yrtny70127/Semiconductor_Quality_Prospectl>
# 또는 이미 클론했다면
git pull
이렇게 하면 uci-secom.csv도 레포에 커밋돼 있다면 그대로 내려옵니다.