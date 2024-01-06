import QtQuick.Layouts
import QtQuick
import QtQuick.Controls
import Controller

Item
{
    id:root


    function startExport()
    {
        controller.startExport()
    }

    Connections
    {
        target: daysComboBox

        function onIndexValueChanged(index, checked)
        {
            controller.setDaysState(index, checked)
        }
    }

    Connections
    {
        target: monthsComboBox

        function onIndexValueChanged(index, checked)
        {
            controller.setMonthsState(index, checked)
        }
    }

    Connections
    {
        target: dayTimeComboBox

        function onIndexValueChanged(index, checked)
        {
            controller.setDayTimeState(index, checked)
        }
    }

    Connections
    {
        target: publicHolidaysBomboBox

        function onIndexValueChanged(index, checked)
        {
            controller.setPublicHolidaysState(index, checked)
        }
    }

    Connections
    {
        target: schoolHolidaysComboBox

        function onIndexValueChanged(index, checked)
        {
            controller.setSchoolHolidaysState(index, checked)
        }
    }

    Connections
    {
        target: frcComboBox

        function onIndexValueChanged(index, checked)
        {
            controller.setFRCState(index, checked)
        }
    }


    Connections
    {
        target: sampleSizeTimeSetsComboBoxAM

        function onIndexValueChanged(index, checked)
        {
            controller.setSampleSizeTimeSetStateAM(index, checked)
        }
    }

    Connections
    {
        target: sampleSizeTimeSetsComboBoxPM

        function onIndexValueChanged(index, checked)
        {
            controller.setSampleSizeTimeSetStatePM(index, checked)
        }
    }


    Connections
    {
        target: speedPercentileTimeSetsComboBoxAM

        function onIndexValueChanged(index, checked)
        {
            controller.setSpeedPercentileTimeSetStateAM(index, checked)
        }
    }

    Connections
    {
        target: speedPercentileTimeSetsComboBoxPM

        function onIndexValueChanged(index, checked)
        {
            controller.setSpeedPercentileTimeSetStatePM(index, checked)
        }
    }

    Connections
    {
        target: classificationComboBox

        function onCurrentIndexChanged()
        {
            controller.setClassificationIndex(classificationComboBox.currentIndex)
        }
    }

    Connections
    {
        target: sampleSizeSPin

        function onValueChanged()
        {
            controller.setSampleSize(sampleSizeSPin.value)
        }
    }

    Connections
    {
        target: speedPercentileSPin

        function onValueChanged()
        {
            controller.setSpeedPercentileThreshold(speedPercentileSPin.value)
        }
    }

    Connections
    {
        target: dialogePage
        function onFolderPathChanged(path)
        {
            controller.setJSONSFolderPath(path)
        }
    }

    Connections
    {
        target: sampleSizeCheckCombo
        function onCurrentIndexChanged()
        {
            controller.setSampleSizeCheckIndex(sampleSizeCheckCombo.currentIndex)
        }
    }

    Connections
    {
        target: controller

        function onProcessIsBeingDone(state)
        {
            if(state === true)
            {
                notificationPopup.notificationText = "Process is being done, please wait till in finishes."
                notificationPopup.open()
            }

            else
            {
                notificationPopup.notificationText = "Process just started."
                notificationPopup.open()
            }
        }

        function onProgressValueChanged(value)
        {
           progressPage.value = value
        }

        function onExportFinished()
        {
            notificationPopup.notificationText = "Export is done."
            notificationPopup.open()
        }

        function onUrlIsEmpty()
        {
            notificationPopup.notificationText = "Select the JSON files folder."
            notificationPopup.open()
        }


    }

    Models
    {
        id:models
    }

    Controller
    {
        id:controller
    }

    Rectangle
    {
        anchors.fill: parent
        color: "#595454"
        radius: 10
        ColumnLayout
        {
            anchors.fill: parent

            RowLayout
            {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Item {
                    Layout.fillWidth: true
                }
                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Text {
                        text: qsTr("Select excluded public holidays:")
                        font.bold: true
                        color: "white"
                        Layout.leftMargin: 10

                    }
                    CheckableComboBox
                    {
                        id:publicHolidaysBomboBox
                        model : models.publicHolidayModel
                        Layout.preferredHeight: 40
                        Layout.fillWidth: true
                        Layout.leftMargin: 10
                        currentIndex:2

                    }
                }

                //                ToolSeparator
                //                {
                //                    orientation: Qt.Vertical
                //                    Layout.fillHeight: true
                //                    Layout.margins: 5
                //                }
                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Text {
                        text: qsTr("Select excluded shcool holidays:")
                        font.bold: true
                        color: "white"
                        Layout.fillWidth: true
                        Layout.leftMargin: 10

                    }

                    CheckableComboBox
                    {
                        id:schoolHolidaysComboBox
                        model : models.schoolHolidayModel
                        Layout.preferredHeight: 40
                        //Layout.preferredWidth: 180
                        Layout.fillWidth: true
                        Layout.leftMargin: 10
                        currentIndex:2
                        Layout.rightMargin: 20


                    }
                }
                Item {
                    Layout.fillWidth: true
                }
            }

            ToolSeparator
            {
                width: 1
                Layout.leftMargin: 10
                Layout.rightMargin: 10
                Layout.fillWidth: true
                orientation: Qt.Horizontal
            }

            RowLayout
            {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Item {
                    Layout.fillWidth: true
                }
                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Text {
                        text: qsTr("Select FRC:")
                        font.bold: true
                        color: "white"
                        Layout.leftMargin: 10

                    }

                    CheckableComboBox
                    {
                        id:frcComboBox
                        model : models.frcModel
                        Layout.preferredHeight: 40
                        Layout.preferredWidth: 180
                        Layout.leftMargin: 10
                        currentIndex:2

                    }
                }
                Item {
                    Layout.fillWidth: true
                }


                Item {
                    Layout.fillWidth: true
                }

                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Text {
                        text: qsTr("Classification :")
                        font.bold: true
                        color: "white"
                        Layout.leftMargin: 10

                    }


                    ComboBox
                    {
                        id:classificationComboBox
                        model : models.classificationModel
                        textRole: "text"
                        Layout.preferredHeight: 40
                        Layout.preferredWidth: 180
                        Layout.leftMargin: 10
                        currentIndex:0

                    }
                }
                Item {
                    Layout.fillWidth: true
                }

            }

            ToolSeparator
            {
                width: 1
                Layout.leftMargin: 10
                Layout.rightMargin: 10
                Layout.fillWidth: true
                orientation: Qt.Horizontal
            }

            RowLayout
            {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Item {
                    Layout.fillWidth: true
                }
                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Text {
                        text: qsTr("Select day:")
                        font.bold: true
                        color: "white"
                        Layout.leftMargin: 10

                    }
                    CheckableComboBox
                    {
                        id:daysComboBox
                        model : models.daysModel
                        Layout.preferredHeight: 40
                        Layout.preferredWidth: 120
                        Layout.leftMargin: 10
                        Layout.rightMargin: 20
                        currentIndex:2

                    }
                }

                //                ToolSeparator
                //                {
                //                    orientation: Qt.Vertical
                //                    Layout.fillHeight: true
                //                    Layout.margins: 5
                //                }
                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Text {
                        text: qsTr("Select month:")
                        font.bold: true
                        color: "white"
                        Layout.leftMargin: 10

                    }

                    CheckableComboBox
                    {
                        id:monthsComboBox
                        model : models.monthsModel
                        Layout.preferredHeight: 40
                        Layout.preferredWidth: 120
                        Layout.leftMargin: 10
                        currentIndex:2

                    }
                }

                //                ToolSeparator
                //                {
                //                    orientation: Qt.Vertical
                //                    Layout.fillHeight: true
                //                    Layout.margins: 5
                //                }
                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Text {
                        text: qsTr("Select daytime:")
                        font.bold: true
                        color: "white"
                        Layout.leftMargin: 30

                    }

                    CheckableComboBox
                    {
                        id:dayTimeComboBox
                        model : models.dayTimeModel
                        Layout.preferredHeight: 40
                        Layout.preferredWidth: 120
                        Layout.leftMargin: 30
                        currentIndex:2

                    }
                }
                Item {
                    Layout.fillWidth: true
                }
            }



            ToolSeparator
            {
                width: 1
                Layout.leftMargin: 10
                Layout.rightMargin: 10
                Layout.fillWidth: true
                orientation: Qt.Horizontal
            }


            RowLayout
            {
                Layout.fillWidth: true
                Layout.fillHeight: true

                Item {
                    Layout.fillWidth: true
                }

                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true


                    Text {
                        text: qsTr("Speed percentile diff:")
                        font.bold: true
                        color: "white"
                        //Layout.leftMargin: 50
                        Layout.rightMargin: 30

                    }

                    SpinBox
                    {
                        //Layout.leftMargin: 40
                        id:speedPercentileSPin
                        Layout.preferredHeight: 40
                        font.pixelSize: 15
                        Layout.rightMargin: 30

                    }
                }

                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Text {
                        text: qsTr("Select time sets (AM):")
                        font.bold: true
                        color: "white"
                        Layout.leftMargin: 10

                    }

                    CheckableComboBox
                    {
                        id:speedPercentileTimeSetsComboBoxAM
                        model : models.timeSetsAmModel
                        Layout.preferredHeight: 40
                        Layout.preferredWidth: 120
                        //Layout.leftMargin: 10
                        currentIndex:2
                    }
                }


                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Text {
                        text: qsTr("Select time sets(PM):")
                        font.bold: true
                        color: "white"
                        Layout.leftMargin: 10

                    }

                    CheckableComboBox
                    {
                        id:speedPercentileTimeSetsComboBoxPM
                        model : models.timeSetsPmModel
                        Layout.preferredHeight: 40
                        Layout.preferredWidth: 120
                        Layout.leftMargin: 10
                        currentIndex:2
                    }
                }

                Item {
                    Layout.fillWidth: true
                }

            }

            ToolSeparator
            {
                width: 1
                Layout.leftMargin: 10
                Layout.rightMargin: 10
                Layout.fillWidth: true
                orientation: Qt.Horizontal
            }

            RowLayout
            {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.bottomMargin: 5

                Item {
                    Layout.fillWidth: true
                }

                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true


                    Text {
                        text: qsTr("Set sample size:")
                        font.bold: true
                        color: "white"
                        //Layout.leftMargin: 50
                        Layout.rightMargin: 30

                    }

                    SpinBox
                    {
                        //Layout.leftMargin: 40
                        id:sampleSizeSPin
                        Layout.preferredHeight: 40
                        font.pixelSize: 15
                        Layout.rightMargin: 30

                    }
                }

                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Text {
                        text: qsTr("Select time sets(AM):")
                        font.bold: true
                        color: "white"
                        Layout.leftMargin: 10

                    }

                    CheckableComboBox
                    {
                        id:sampleSizeTimeSetsComboBoxAM
                        model : models.timeSetsAmModel
                        Layout.preferredHeight: 40
                        Layout.preferredWidth: 120
                        Layout.leftMargin: 10
                        currentIndex:2

                    }
                }

                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.preferredWidth: 120

                    Text {
                        text: qsTr("Select time sets(PM):")
                        font.bold: true
                        color: "white"
                        Layout.leftMargin: 10

                    }

                    CheckableComboBox
                    {
                        id:sampleSizeTimeSetsComboBoxPM
                        model : models.timeSetsPmModel
                        Layout.preferredHeight: 40
                        Layout.preferredWidth: 120
                        Layout.leftMargin: 10
                        currentIndex:2

                    }
                }

                ColumnLayout
                {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Text {
                        text: qsTr("Sample size check for:")
                        font.bold: true
                        color: "white"
                        Layout.leftMargin: 10

                    }

                    ComboBox
                    {
                        id:sampleSizeCheckCombo
                        model : models.sampleSizeSearchModel
                        Layout.preferredHeight: 40
                        Layout.preferredWidth: 120
                        Layout.leftMargin: 10
                        currentIndex:0
                        textRole: "text"


                    }
                }

                Item {
                    Layout.fillWidth: true
                }

            }


        }
    }
}
