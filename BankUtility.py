import sys,time
def spinner_animation(message,duration=2):
    char=['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time=time.time()+duration
    i=0
    while time.time()<end_time:
        sys.stdout.write(f"\r{message}.. {char[i%len(char)]}       ")
        sys.stdout.flush()
        i = i + 1
        time.sleep(0.08)
    print(f"\r{message} Done!                       ")

def progress_bar(message,duration=1.5):
    char=[".","..","...","...","...."]
    end_time=time.time()+duration
    i=0
    while time.time()<end_time:
        sys.stdout.write(f"\r{message}{char[i%len(char)]}           ")
        sys.stdout.flush()
        i=i+1
        time.sleep(0.2)
    print(f"\r{message} Done!                  ")

def type_effect(message,speed=0.02):
    for i in message:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def loading_bar(message,duration=0.01):
    for i in range(101):
        sys.stdout.write(f"\r{message}..{i}%             ")
        sys.stdout.flush()
        time.sleep(duration)
    print(f"\r{message} Done!             ")
def animation(message,duration=2):
    char=["|","-","/","\\"]
    end_time=time.time()+duration
    i=0
    while time.time()<end_time:
        sys.stdout.write(f"\r{message}..{char[i%len(char)]}              ")
        sys.stdout.flush()
        time.sleep(0.08)
        i=i+1
    print(f"\r{message} Successfully                     ")

