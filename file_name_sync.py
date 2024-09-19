import PySimpleGUI as sg
import os
from pathlib import Path
import time
import subprocess

# Define the path to your archive folder
archive_folder_path = Path("/Users/broccoli/Desktop/archive")
archiving_script_path = ""

def main():
    sg.theme("HotDogStand")
    
    layout = [
        [sg.Text("Select the file of your show recording: ", font="Helvetica 20"), sg.FileBrowse(initial_folder="/Users/broccoli/Desktop/archive_temp", file_types=(('MP3s', '*.mp3'),), key="-FILE-", font="Helvetica 20")],
        [sg.Text("What is the name of your show? (as you would like it to appear on the archive)", font="Helvetica 20"), sg.InputText(key="-SHOW_TITLE-", font="Helvetica 20")],
        [sg.Button('Archive!', font="Helvetica 20"), sg.Button('Cancel', font="Helvetica 20")]
    ]

    window = sg.Window('KCHUNG Archiver', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
        
        if event == 'Archive!':
            file = values["-FILE-"]
            show_name = values["-SHOW_TITLE-"]
            if file and show_name:
                try:
                    file_path = Path(file)
                    mtime = os.path.getmtime(file_path)
                    date = time.localtime(mtime)
                    formatted_date = time.strftime("%Y-%m-%d", date)
                    new_file_name = f"{show_name} {formatted_date}.mp3"
                    
                    dated_archive_folder = archive_folder_path / formatted_date
                    if not dated_archive_folder.exists():
                        os.mkdir(dated_archive_folder)

                    new_file_path = dated_archive_folder / new_file_name

                    if new_file_path.exists():
                        name_response = sg.popup_ok_cancel(
                            "A file already exists for this show name and date.\nIf you would like to delete this file select 'Ok' otherwise, select 'Cancel' to restart and select a new name.",
                            font="Helvetica 20"
                        )
                        if name_response == 'OK':
                            os.remove(new_file_path)
                            os.rename(file_path, new_file_path)  # Rename the new file
                            subprocess.run(['bash', archiving_script_path], check=True)
                            sg.popup(
                            f'{file} successfully moved to {new_file_path} and archive workflow successfully kicked off! Your show will be available on the archive in 24 hours.',
                            font="Helvetica 20",
                            keep_on_top=True)
                            break  # Exit the loop after successful operation
                        elif name_response == 'Cancel':
                            # Reset the window inputs
                            window['-FILE-'].update('')
                            window['-SHOW_TITLE-'].update('')
                            continue  # Restart the loop to allow the user to select a new file or name

                    else:
                        # If the file doesn't exist, just proceed with renaming
                        os.rename(file_path, new_file_path)
                        subprocess.run(['bash', archiving_script_path], check=True)
                        sg.popup(
                            f'{file} successfully moved to {new_file_path} and archive workflow successfully kicked off! Your show will be available on the archive in 24 hours.',
                            font="Helvetica 20",
                            keep_on_top=True
                        )
                        break  # Exit the loop after successful operation

                except Exception as e:
                    error_message = str(e)[:100]  # Truncate long messages
                    sg.popup_error(f"Error: {error_message} \n Email brock@warpmail.net with error for assistance.")
            
            else:
                sg.popup_error("No file or show name specified.")

    window.close()

if __name__ == "__main__":
    main()
