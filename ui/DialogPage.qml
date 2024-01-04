import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import Qt.labs.platform
import QtQuick.Layouts

Item
{
    id:root

    Connections
    {
        target:fileDialogButton
        function onPressed()
        {
           dialogFile.open()
        }
    }

    signal folderPathChanged(string path)

    Rectangle
    {
        anchors.fill:parent
        radius: 5
        color: "#595454"

        FolderDialog {
            id:dialogFile;
            title: "Please select folder which contains positive training data";
            //folder: shortcuts.home;

            onAccepted: {
                //console.log("User has selected " + dialogFile.folder);
                jsonsFolderpathTextInput.text = dialogFile.folder
                folderPathChanged(dialogFile.folder)
            }
        }

        RowLayout
        {
            anchors.fill: parent
            Button
            {
                id:fileDialogButton
                text: "Select the JSON file(s)"
                Layout.leftMargin: 5
            }


            Pane
            {
                Layout.fillWidth: true
                //Layout.verticalCenter: Layout.verticalCenter
                Layout.rightMargin: 5
                Layout.preferredHeight: 30
                //Material.elevation: 10

                background: Rectangle
                {
                    anchors.fill:parent
                    color:"#3b3737"
                }

                TextInput
                {
                    id:jsonsFolderpathTextInput
                    anchors.fill: parent
                    font.pixelSize: 12
                    verticalAlignment: Text.AlignVCenter
                    color: "white"
                    Text
                    {
                        text: "JSON files directory path"
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.horizontalCenter: parent.horizontalCenter
                        visible: !jsonsFolderpathTextInput.text
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        color: "#c9c7c7"
                        
                    }

                }
            }
        }

    }

}
