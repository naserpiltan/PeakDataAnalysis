import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0


Rectangle
{
    property alias text: label.text
    property alias checked: checkbox.checked
    property int index: 0 // To track the index of the item
    color: "#575a5c"
    border.color: "#f77a40"
    border.width: 1
    RowLayout {
        id:root

        anchors.fill: parent
        CheckBox {
            id: checkbox
            onCheckedChanged: {
                //controller.sendValues(controller.labelName, checked)
                // Emit a signal or call a function when checked state changes
                indexValueChanged(index,checked)

            }
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignCenter

        }

        Label {
            id: label
            elide: Text.ElideRight
            Layout.fillHeight: true
            Layout.fillWidth: true
            horizontalAlignment: Qt.AlignHCenter
            verticalAlignment: Qt.AlignVCenter
            color: "white"
            font.bold: true
        }
    }
}
