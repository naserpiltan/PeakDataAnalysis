import QtQuick.Layouts
import QtQuick
import QtQuick.Controls

Item{
    id:root

    Connections
    {
        target:progressPage
        function onExportPressed()
        {
          dropDownPage.startExport()
        }
    }

    ColumnLayout{
        anchors.fill:parent

        DialogPage{
            id:dialogePage
            Layout.fillWidth : true
            Layout.preferredHeight : 70
            Layout.margins: 10
        }

        DropDownsPage
        {
            id:dropDownPage
            Layout.fillWidth : true
            Layout.fillHeight: true
            Layout.leftMargin: 10
            Layout.rightMargin: 10
            Layout.bottomMargin: 20
            Layout.topMargin: 20


        }


        ProgressPage
        {
            id:progressPage
            Layout.fillWidth : true
            Layout.preferredHeight : 33
            Layout.margins: 10
        }


    }
}
