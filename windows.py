import PySimpleGUI as sg
import os.path


# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse("Select"),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
file_viewer_column = [
    [sg.Text("Choose a file from list on left:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Button("Start the script", key="-FILE-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(file_viewer_column),
    ]
]

window = sg.Window("TM Cleaner", layout, enable_close_attempted_event=True)

original_tmx_file = ""

# Run the Event Loop
while True:
    event, values = window.read()
    tmx = False

    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".tmx"))
        ]
        window["-FILE LIST-"].update(fnames)
    if event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            path = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            s = values["-FILE LIST-"][0]
            original_tmx_file = s # Attribute name of the TMX

            window["-TOUT-"].update(s, text_color="white")
            assert original_tmx_file.endswith(".tmx") # Check for correct format
              
        except:
            sg.popup_ok("This program only accepts .tmx files", title="Error") # Error message when selecting non .tmx file
            window["-TOUT-"].update(s, text_color="red")   
            
    if event == "-FILE-": # Click button to execute script
        try:
            with open("update_tmx.py") as f:
                exec(f.read())
        except:
            pass
            
    if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT and sg.popup_yes_no("Do you really want to exit?") == "Yes": # Confirm exiting program
        break
            
window.close()