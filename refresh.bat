adb shell monkey -p com.google.android.gm -c android.intent.category.LAUNCHER 1

adb shell am start -n com.example.myapplication/com.example.myapplication.MainActivity --ei initial_pressure 0 --ei pressure 5 --ei period 1000 -e proc_name com.google.android.gm -e output gmail_pss

adb shell monkey -p com.google.android.gm -c android.intent.category.LAUNCHER 1
adb shell i=0; while [ $(($i)) -le 40000 ]; do i=$(($i + 1)); input swipe 588 1080 588 1510 100; done
