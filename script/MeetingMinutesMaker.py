"""this is the central script"""

import traceback
import os
import UI_App



import pyautogui



EXE_NAME = u"Ennead_MeetingMinute_Maker"


def try_catch_error(func):

    def wrapper(*args, **kwargs):


        try:
 
            out = func(*args, **kwargs)
           
            return out
        except Exception as e:
          
            error = traceback.format_exc()

            error += "\n\n######If you have EnneadTab UI window open, just close the window. Do no more action, otherwise the program might crash.##########\n#########Not sure what to do? Msg Sen Zhang, you have dicovered a important bug and we need to fix it ASAP!!!!!########"
            error_file = "{}\Documents\EnneadTab Settings\Local Copy Dump\error_log.txt".format(
                os.environ["USERPROFILE"])

            with open(error_file, "w") as f:
                f.write(error)
            os.startfile(error_file)

    return wrapper

def is_another_app_running():


    for window in pyautogui.getAllWindows():
        # print window.title
        if window.title == EXE_NAME:
            return True
    return False

@try_catch_error
def main():
    if is_another_app_running():
        return
    app = UI_App.App()
    app.run()


###############################################
if __name__ == "__main__":
    main()
