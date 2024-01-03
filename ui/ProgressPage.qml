import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id:root
    property alias value : progressBar.value

    signal exportPressed()

    Connections
    {
        target:exportBtn

        function onClicked()
        {
           exportPressed()
        }
    }

    Rectangle
    {
        anchors.fill: parent
        color: "#595454"
        radius: 10

        RowLayout
        {
            anchors.fill: parent
            anchors.centerIn: parent.Center

            Button
            {
                id:exportBtn
                text: "Export"
                Layout.leftMargin: 10

            }


            Text
            {

              Layout.leftMargin: 10
              text: "Processed files: "
              font.bold: true
              color: "white"
              horizontalAlignment: Qt.AlignHCenter
              verticalAlignment: Qt.AlignVCenter
              Layout.bottomMargin: 5

            }
            ProgressBar
            {
                Layout.fillWidth: true
                id:progressBar
                Layout.rightMargin: 10
                //Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                Layout.bottomMargin: 2

            }
        }

    }

}
